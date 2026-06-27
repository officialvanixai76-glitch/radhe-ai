RadheAI
=======

RadheAI is available in two app modes:

- Web app: a local browser dashboard backed by the Python API server.
- Desktop app: a native PyQt6 desktop assistant.

Setup
-----

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r RadheAI\requirements.txt
cd RadheAI
```

Run The Web App
---------------

```powershell
python main.py web
```

The launcher opens the app in your default browser at `http://localhost:8000`. If port `8000` is busy, it automatically picks the next free port.

Optional:

```powershell
python main.py web --port 8010
python main.py web --no-browser
```

Run The Desktop App
-------------------

```powershell
python main.py desktop
```

Default login:

- Username: `admin`
- Password: `admin`

Windows Shortcuts
-----------------

From the repository root, double-click:

- `Start RadheAI Web App.bat`
- `Start RadheAI Desktop App.bat`

Files
-----

- `main.py`: unified launcher for web and desktop modes.
- `main_desktop.py`: native PyQt6 desktop shell.
- `web_server.py`: local HTTP API and static web app server.
- `web/`: HTML, CSS, and JavaScript frontend.

AI Model
--------

Chat replies are routed through OpenRouter by default:

- Provider: `openrouter`
- Model: `google/gemma-4-31b-it:free`

The API key is read from `RadheAI/config/settings.json` or the `RADHEAI_OPENROUTER_API_KEY` environment variable. Do not commit real API keys to a public repository.
