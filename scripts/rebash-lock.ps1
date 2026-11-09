<#
.SYNOPSIS
  Re-baseline computes skills-lock.json computedHash from the canonical local
  SKILL.md files, using the documented sha256-lf algorithm.

.DESCRIPTION
  Canonical hash = SHA-256 over the UTF-8 text of skills/<name>/SKILL.md with
  CRLF/CR normalised to LF and a leading BOM stripped. This is the scheme
  scripts/audit-skills.ps1 and scripts/verify-upstream-skills.ps1 use, so the
  three tools always agree.

  Any entry whose stored hash differs is re-baselined, and the previous value is
  preserved as `importHash` (provenance of the original importer, kept as an
  audit trail because it is not reproducible). Use -Check to report only.

.EXAMPLE
  powershell -File scripts\rebash-lock.ps1 -Check
  powershell -File scripts\rebash-lock.ps1
#>
param(
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$lockPath = Join-Path $root 'skills-lock.json'

function Get-CanonicalHash([string]$Path) {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) { $text = $text.Substring(1) }
    $text = $text -replace "`r`n", "`n" -replace "`r", "`n"
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hash = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($text))
    } finally {
        $sha.Dispose()
    }
    return ([System.BitConverter]::ToString($hash) -replace '-', '').ToLower()
}

$lock = Get-Content $lockPath -Raw | ConvertFrom-Json
$changed = 0
$ok = 0

foreach ($name in ($lock.skills.PSObject.Properties.Name | Sort-Object)) {
    $entry = $lock.skills.$name
    $md = Join-Path (Join-Path $root 'skills') "$name\SKILL.md"
    if (-not (Test-Path $md)) {
        Write-Host ("[MISS] {0} - no skills/{0}/SKILL.md" -f $name)
        continue
    }
    $canonical = Get-CanonicalHash $md
    $stored = ([string]$entry.computedHash).ToLower()

    if ($canonical -eq $stored) { $ok++; continue }

    if ($Check) {
        Write-Host ("[DRIFT] {0}  stored={1}  canonical={2}" -f $name, $stored, $canonical)
        $changed++
        continue
    }

    $entry | Add-Member -NotePropertyName importHash -NotePropertyValue $stored -Force
    $entry.computedHash = $canonical
    Write-Host ("[REBASELINED] {0}  importHash={1}  computedHash={2}" -f $name, $stored, $canonical)
    $changed++
}

if ($Check) {
    Write-Host ""
    Write-Host ("Summary: {0} match, {1} drift (run without -Check to re-baseline)" -f $ok, $changed)
    if ($changed -gt 0) { exit 1 }
    exit 0
}

$lock | ConvertTo-Json -Depth 6 | Set-Content -Path $lockPath -Encoding UTF8
Write-Host ""
Write-Host ("Summary: {0} already current, {1} re-baselined -> skills-lock.json" -f $ok, $changed)