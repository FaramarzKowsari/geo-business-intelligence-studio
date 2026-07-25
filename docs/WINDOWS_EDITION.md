# Windows edition

## Official download

The verified Windows edition is distributed as an official GitHub Release asset:

- [Download GeoBusiness Intelligence Studio EXE](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases/latest/download/GeoBusiness-Intelligence-Studio.exe)
- [Download SHA-256 checksum](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases/latest/download/GeoBusiness-Intelligence-Studio.exe.sha256)
- [View all releases](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases)

The executable is self-contained. Users do not need Python, PowerShell, pip, Git, or a virtual environment.

## Run the application

1. Download `GeoBusiness-Intelligence-Studio.exe`.
2. Keep the accompanying `.sha256` file when verification is required.
3. Double-click the EXE.
4. Keep the application process open while using the browser dashboard.

The program starts a localhost-only FastAPI server on an available port and opens the default browser. It does not expose the local service to other computers.

## Verification

The Windows executable is built, started, and health-checked automatically on a GitHub-hosted Windows runner before publication. Compare the SHA-256 hash with:

`GeoBusiness-Intelligence-Studio.exe.sha256`

## Windows security notice

The project is open source, but the executable is not Authenticode-signed. Windows SmartScreen may show an unfamiliar-publisher warning until a code-signing certificate and reputation are established.

## Build workflow

The **Build Windows Edition** workflow:

1. installs the application and PyInstaller;
2. runs Ruff and the test suite;
3. builds a one-file executable;
4. launches the packaged application;
5. checks `/api/health`;
6. creates a SHA-256 checksum;
7. publishes an Actions artifact;
8. attaches the EXE and checksum to a published GitHub Release.

Workflow: https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/build-windows.yml
