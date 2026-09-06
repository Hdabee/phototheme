$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Environnement .venv absent. Lancez d'abord .\start.ps1" -ForegroundColor Yellow
    exit 1
}

& .\.venv\Scripts\python.exe -m pytest -q
