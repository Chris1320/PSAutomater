from pathlib import Path
from time import strftime

NAME: str = "PSAutomater"
VERSION: tuple[int, int, int] = (0, 2, 0)
TITLE: str = f"{NAME} v{'.'.join(map(str, VERSION))}"

WINDOW_SIZE: dict[str, tuple[int, int]] = {  # (w, h)
    "min": (640, 540),
    "max": (1920, 1080),
}

logfile_path = Path("data", "logs", f"log_{strftime('%Y-%m-%d')}.txt")
LOGFILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
LOGGING_DEBUG_MODE = "DEBUG"
LOGGING_RELEASE_MODE = "INFO"
