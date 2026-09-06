$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creation de l'environnement virtuel .venv..." -ForegroundColor Cyan
    py -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
Write-Host "Demarrage de PhotoTheme API sur http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Documentation interactive : http://127.0.0.1:8000/docs" -ForegroundColor Green
& .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
