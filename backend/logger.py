import sys
import logging
from pathlib import Path
from backend.database import save_log

APP_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = APP_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "radheai.log"

# Set up logging to file and stream
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)


def log(message: str, level: str = "INFO"):
    """Log a message with a specific log level and write it to the db logs."""
    lvl = level.upper()
    if lvl == "DEBUG":
        logging.debug(message)
    elif lvl == "WARNING":
        logging.warning(message)
    elif lvl == "ERROR":
        logging.error(message)
    elif lvl == "CRITICAL":
        logging.critical(message)
    else:
        logging.info(message)

    # Save directly to the DB logs
    save_log(lvl, message)