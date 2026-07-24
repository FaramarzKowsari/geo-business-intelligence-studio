$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]" "pyinstaller>=6.12,<7"
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean geobusiness_windows.spec

$hash = (Get-FileHash "dist\GeoBusiness-Intelligence-Studio.exe" -Algorithm SHA256).Hash.ToLower()
"$hash  GeoBusiness-Intelligence-Studio.exe" | Set-Content "dist\GeoBusiness-Intelligence-Studio.exe.sha256"
Write-Host "Windows build created in dist\." -ForegroundColor Green
