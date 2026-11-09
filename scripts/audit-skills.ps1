# Static health audit for the skills hub (skills/) against skills-lock.json.
# Usage:
#   powershell -File scripts\audit-skills.ps1                 # audit every skill
#   powershell -File scripts\audit-skills.ps1 -Skill <name>   # audit one skill (adds platform-marker check)
#   powershell -File scripts\audit-skills.ps1 -Inventory      # print name :: lock-status :: description
# Exit code 0 = no FAIL, 1 = at least one FAIL (CI-friendly).
param(
    [string]$Skill = "",
    [switch]$Inventory
)

$ErrorActionPreference = 'Stop'
$root      = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$skillsDir = Join-Path $root 'skills'
$lockPath  = Join-Path $root 'skills-lock.json'

$fail = 0; $warn = 0; $pass = 0

$lock = @{}
if (Test-Path $lockPath) {
    try {
        $json = Get-Content $lockPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($json.skills) {
            foreach ($p in $json.skills.PSObject.Properties) { $lock[$p.Name] = $p.Value }
        }
    } catch {
        Write-Output "[FAIL] skills-lock.json unreadable: $($_.Exception.Message)"; $fail++
    }
} else {
    Write-Output "[FAIL] skills-lock.json not found"; $fail++
}

$dirs = Get-ChildItem $skillsDir -Directory | Sort-Object Name
if ($Skill -ne "") { $dirs = $dirs | Where-Object { $_.Name -eq $Skill } }
if (-not $dirs) { Write-Output "[FAIL] skill '$Skill' not found"; exit 1 }

if ($Inventory) {
    foreach ($d in $dirs) {
        $md = Join-Path $d.FullName 'SKILL.md'
        $desc = ''
        if (Test-Path $md) {
            $raw = Get-Content $md -Raw -Encoding UTF8
            if ($raw -match '(?m)^\s*description:\s*(.+)$') { $desc = $Matches[1].Trim() }
            if ($desc.Length -gt 110) { $desc = $desc.Substring(0, 110) + '...' }
        }
        $status = 'UNLOCKED-MISSING'
        if ($lock.ContainsKey($d.Name)) {
            if ([string]$lock[$d.Name].source -match '^local') { $status = 'local' } else { $status = 'upstream' }
        }
        Write-Output ("{0} :: {1} :: {2}" -f $d.Name, $status, $desc)
    }
    exit 0
}

foreach ($d in $dirs) {
    $name = $d.Name
    $md = Join-Path $d.FullName 'SKILL.md'
    $checks = @()

    if (-not (Test-Path $md)) {
        Write-Output "== $name =="; Write-Output "  [FAIL] SKILL.md missing"; $fail++; continue
    }
    $raw = Get-Content $md -Raw -Encoding UTF8

    # frontmatter: name + description required
    $hasFm = $raw.StartsWith('---')
    $fmName = ''; $fmDesc = ''
    if ($hasFm) {
        $endIdx = $raw.IndexOf('---', 3)
        if ($endIdx -gt 0) {
            $fm = $raw.Substring(3, $endIdx - 3)
            if ($fm -match '(?m)^\s*name:\s*(.+)$')         { $fmName = $Matches[1].Trim() }
            if ($fm -match '(?m)^\s*description:\s*(.+)$')  { $fmDesc = $Matches[1].Trim() }
        }
    }
    if (-not $hasFm)        { $checks += "[FAIL] no frontmatter"; $fail++ }
    elseif ($fmName -eq '') { $checks += "[FAIL] frontmatter missing 'name:'"; $fail++ }
    elseif ($fmDesc -eq '') { $checks += "[FAIL] frontmatter missing 'description:'"; $fail++ }
    else {
        if ($fmName -ne $name) { $checks += "[WARN] name '$fmName' != folder '$name'"; $warn++ }
        else                   { $checks += "[PASS] frontmatter"; $pass++ }
    }

    # dead relative markdown links
    $missingLinks = @()
    foreach ($m in [regex]::Matches($raw, '\[[^\]]+\]\(([^)\s]+)\)')) {
        $t = $m.Groups[1].Value.Trim()
        if ($t -match '^(https?://|mailto:|#)') { continue }
        $t = ($t -split '#')[0]
        if ($t -eq '') { continue }
        # Template placeholders such as [paper](URL) or [ref](<path>) are not links:
        # only targets that look like a path ('.', '/' or '\') are checked.
        if ($t -match '[<>]' -or $t -notmatch '[./\\]') { continue }
        if (-not (Test-Path (Join-Path $d.FullName $t))) { $missingLinks += $t }
    }
    if ($missingLinks.Count -gt 0) { $checks += "[FAIL] dead link: $($missingLinks -join ', ')"; $fail++ }
    else                           { $checks += "[PASS] links"; $pass++ }

    # lock entry + hash
    if ($lock.ContainsKey($name)) {
        $isLocal = ([string]$lock[$name].source -match '^local')
        $hashOk = $true
        $expected = [string]$lock[$name].computedHash
        if ($expected -ne '') {
            # canonical hash: sha256-lf (see scripts/rebash-lock.ps1 + docs/agents/skills.md)
            $rawBytes = [System.IO.File]::ReadAllBytes($md)
            $rawText = [System.Text.Encoding]::UTF8.GetString($rawBytes)
            if ($rawText.Length -gt 0 -and $rawText[0] -eq [char]0xFEFF) { $rawText = $rawText.Substring(1) }
            $canonical = $rawText -replace "`r`n", "`n" -replace "`r", "`n"
            $sha = [System.Security.Cryptography.SHA256]::Create()
            try {
                $actual = ([System.BitConverter]::ToString($sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($canonical))) -replace '-', '').ToLower()
            } finally {
                $sha.Dispose()
            }
            if ($actual -ne $expected.ToLower()) { $hashOk = $false }
        }
        if (-not $hashOk)   { $checks += "[FAIL] computedHash mismatch vs skills-lock.json"; $fail++ }
        elseif ($isLocal)   { $checks += "[PASS] lock: local"; $pass++ }
        else                { $checks += "[PASS] lock: upstream-locked (do not edit locally)"; $pass++ }
    } else {
        $checks += "[FAIL] no entry in skills-lock.json"; $fail++
    }

    # thin body
    $lineCount = ($raw -split "`n").Count
    if ($lineCount -lt 15) { $checks += "[WARN] unusually thin body ($lineCount lines)"; $warn++ }

    # platform marker (single-skill mode only, keeps all-hub runs quiet)
    if ($Skill -ne "" -and -not (Test-Path (Join-Path $d.FullName 'agents\openai.yaml'))) {
        $checks += "[WARN] no agents/openai.yaml platform marker"; $warn++
    }

    Write-Output "== $name =="
    foreach ($c in $checks) { Write-Output "  $c" }
}

Write-Output ""
Write-Output "Summary: $pass pass, $warn warn, $fail fail"
if ($fail -gt 0) { exit 1 }
exit 0
