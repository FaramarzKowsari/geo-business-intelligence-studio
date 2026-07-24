# Windows edition

The repository can produce `GeoBusiness-Intelligence-Studio.exe`, a one-file Windows application that does not require the user to install Python or type PowerShell commands.

## Build from GitHub Actions

1. Open the repository's **Actions** tab.
2. Select **Build Windows Edition**.
3. Choose **Run workflow**.
4. When the workflow finishes, download the `GeoBusiness-Intelligence-Studio-Windows` artifact.

The artifact contains:

- `GeoBusiness-Intelligence-Studio.exe`
- `GeoBusiness-Intelligence-Studio.exe.sha256`

Double-clicking the EXE starts a localhost-only FastAPI server on an available port and opens the browser automatically. Closing the application process stops the local server.

## Release attachment

When a GitHub Release is published, the same workflow builds and smoke-tests the Windows application, then attaches the EXE and SHA-256 file to that Release.

## Windows security notice

The application is open source but is not Authenticode-signed. Windows SmartScreen may display an unfamiliar-publisher warning until a code-signing certificate is added and reputation is established.

## Local build

A Windows developer can build it with:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-desktop.txt
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean geobusiness_windows.spec
```

PyInstaller is not a cross-compiler, so the Windows binary must be produced on Windows. The GitHub Actions job uses `windows-latest` for that reason.
