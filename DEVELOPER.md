# DEVELOPER.md

## Setup for Data Projects

1. Fork the repo.
2. Clone your fork and open it in VS Code.
3. Open a terminal (examples below use PowerShell on Windows).

```
git clone https://github.com/civic-interconnect/civic-data-boundaries-us-forests.git
cd civic-data-boundaries-us-forests
.\setup.ps1 -Editable
civic-dev prep-code
civic-dev publish-api
mkdocs serve
```

Visit local API docs at: <http://localhost:8000>

## Before Starting Changes, Verify

```shell
git pull
civic-usa fetch
civic-usa export
civic-usa index
civic-usa cleanup
```

## Releasing New Version

Before publishing a new version, delete .venv. and recreate and activate.
Run pre-release preparation, installing and upgrading without the -e editable flag.
Verify all tests pass. Run prep-code (twice if needed).
Verify the docs are generated and appear correctly.

```powershell
git pull
deactivate
Remove-Item -Recurse -Force .venv
.\setup.ps1
pytest tests
civic-dev prep-code
civic-dev publish-api
mkdocs serve
```

After verifying changes:

```powershell
civic-dev bump-version 0.0.1 0.0.2
civic-dev release
```
