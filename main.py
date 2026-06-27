import argparse
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Add project root to python path for backend imports.
APP_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_ROOT))

from backend.database import init_database
from backend.settings import load_settings
from web_server import run_web_server


def _is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def _available_port(preferred_port: int) -> int:
    if _is_port_free(preferred_port):
        return preferred_port

    for port in range(preferred_port + 1, preferred_port + 100):
        if _is_port_free(port):
            return port

    raise RuntimeError("No free port found for the RadheAI web app.")


def _bootstrap_storage():
    init_database()
    load_settings()


def run_web_app(port: int = 8000, open_browser: bool = True):
    _bootstrap_storage()

    actual_port = _available_port(port)
    server_thread = threading.Thread(target=run_web_server, args=(actual_port,), daemon=True)
    server_thread.start()

    time.sleep(1.0)
    url = f"http://localhost:{actual_port}"
    print("=" * 50)
    print(f" RadheAI Web App: {url}")
    print(" Press Ctrl + C to stop.")
    print("=" * 50)

    if open_browser:
        webbrowser.open(url)

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nShutting down RadheAI Web App.")


def run_desktop_app():
    from main_desktop import main as desktop_main

    desktop_main()


def parse_args():
    parser = argparse.ArgumentParser(description="RadheAI desktop and web app launcher")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=("web", "desktop"),
        default="web",
        help="Launch the browser-based web app or the native PyQt desktop app.",
    )
    parser.add_argument("--port", type=int, default=8000, help="Preferred web app port.")
    parser.add_argument("--no-browser", action="store_true", help="Start web mode without opening a browser.")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.mode == "desktop":
        run_desktop_app()
    else:
        run_web_app(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
