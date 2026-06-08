param(
    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 6)]
    [int]$Stage
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$StageName = "stage-{0:D2}" -f $Stage
$Src = Join-Path $Root "git-stages\$StageName"

if (-not (Test-Path $Src)) {
    Write-Error "Folder not found: $Src. Run: powershell -File scripts/build-git-stages.ps1"
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Apply $StageName -> project" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Get-ChildItem $Src -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($Src.Length + 1)
    $dst = Join-Path $Root $rel
    $dstDir = Split-Path $dst -Parent
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
    Copy-Item $_.FullName $dst -Force
    Write-Host "  + $rel"
}

$CommitFile = Join-Path $Root "git-stages\$StageName\COMMIT.txt"
if (Test-Path $CommitFile) {
    Write-Host ""
    Write-Host "--- Suggested commit message ---" -ForegroundColor Green
    Get-Content $CommitFile
    Write-Host "--------------------------------" -ForegroundColor Green
    Write-Host ""
}

Write-Host "Next:"
Write-Host "  git add -A"
Write-Host "  git commit -F git-stages/$StageName/COMMIT.txt --date=`"YYYY-MM-DDTHH:MM:SS`""
