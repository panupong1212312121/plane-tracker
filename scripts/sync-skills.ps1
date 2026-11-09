# Propagate skills/ into every agent directory (.agents/skills, .claude/skills).
# Usage:
#   powershell -File scripts\sync-skills.ps1            # mirror skills/ to targets
#   powershell -File scripts\sync-skills.ps1 -Prune     # also remove target-only skill dirs
param([switch]$Prune)

$ErrorActionPreference = 'Stop'
$root      = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$skillsDir = Join-Path $root 'skills'
$targets   = @('.agents', '.claude', '.kilo')

function Get-Signature([string]$path) {
    $files = Get-ChildItem $path -Recurse -File
    $count = @($files).Count
    $size = ($files | Measure-Object -Property Length -Sum).Sum
    $md = Join-Path $path 'SKILL.md'
    $mdHash = if (Test-Path $md) { (Get-FileHash $md -Algorithm SHA256).Hash } else { 'NO-MD' }
    return "$count|$size|$mdHash"
}

$copied = 0; $upToDate = 0; $pruned = 0
foreach ($t in $targets) {
    $targetRoot = Join-Path $root (Join-Path $t 'skills')
    New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

    $sources = Get-ChildItem $skillsDir -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }
    foreach ($s in $sources) {
        $dest = Join-Path $targetRoot $s.Name
        if ((Test-Path $dest) -and ((Get-Signature $s.FullName) -eq (Get-Signature $dest))) {
            $upToDate++
            continue
        }
        if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
        Copy-Item $s.FullName $dest -Recurse -Force
        Write-Output ("[SYNC] {0}/skills/{1}" -f $t, $s.Name)
        $copied++
    }

    $stale = Get-ChildItem $targetRoot -Directory | Where-Object { -not (Test-Path (Join-Path $skillsDir $_.Name)) }
    foreach ($st in $stale) {
        if ($Prune) {
            Remove-Item $st.FullName -Recurse -Force
            Write-Output ("[PRUNE] {0}/skills/{1}" -f $t, $st.Name)
            $pruned++
        } else {
            Write-Output ("[STALE] {0}/skills/{1} (not in skills/ - use -Prune to remove)" -f $t, $st.Name)
        }
    }
}
Write-Output ""
Write-Output ("Done: synced {0} / up-to-date {1} / pruned {2}" -f $copied, $upToDate, $pruned)
