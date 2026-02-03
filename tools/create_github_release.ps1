<#
Create a GitHub release and upload all files from `dist/` as release assets.

Usage (PowerShell):
  .\tools\create_github_release.ps1 -Tag v1.0.0 -Title "My Release"

Requirements:
  - Install GitHub CLI: https://github.com/cli/cli
  - Authenticate: `gh auth login`
  - Ensure `dist/` contains your built executables
#>

[param(
  [string]$Tag = "v1.0.0",
  [string]$Title = "Genius 3D Chess & Autonomous Diary v1.0.0",
  [string]$NotesFile = "docs/RELEASE_DRAFT.md"
)]

function Fail([string]$msg){ Write-Host $msg -ForegroundColor Red; exit 1 }

if (-not (Get-Command gh -ErrorAction SilentlyContinue)){
  Fail "gh CLI not found. Install it from https://github.com/cli/cli and run `gh auth login`."
}

if (-not (Test-Path "dist")){
  Fail "dist/ directory not found. Build or copy your .exe files into dist/ before running this script."
}

$assets = Get-ChildItem -Path .\dist\* -File | ForEach-Object { $_.FullName }
if ($assets.Count -eq 0){ Fail "No files found in dist/. Nothing to upload." }

# Build the gh command string with properly-quoted asset paths
$assetArgs = $assets | ForEach-Object { '"' + ($_ -replace '"','\"') + '"' } -join ' '
$notesArg = if (Test-Path $NotesFile) { ' --notes-file "' + (Resolve-Path $NotesFile) + '"' } else { '' }
$cmd = "gh release create $Tag $assetArgs --title \"$Title\"$notesArg"

Write-Host "Running: $cmd" -ForegroundColor Cyan

# Execute the command
$exit = Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0){
  Write-Host "Release created/updated with tag $Tag" -ForegroundColor Green
} else {
  Fail "gh command failed with exit code $LASTEXITCODE"
}
