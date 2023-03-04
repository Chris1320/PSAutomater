"""
MIT License

Copyright (c) 2023 Chris1320

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from time import strftime
from pathlib import Path

NAME: str = "PSAutomater"
VERSION: tuple[int, int, int] = (0, 1, 1)
TITLE: str = f"{NAME} v{'.'.join(map(str, VERSION))}"

WINDOW_SIZE: dict[str, tuple[int, int]] = {  # (w, h)
    "min": (640, 540),
    "max": (1280, 1080)
}

logfile_path = Path("data", "logs", f"log_{strftime('%Y-%m-%d')}.txt")
LOGFILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
LOGGING_DEBUG_MODE = "DEBUG"
LOGGING_RELEASE_MODE = "INFO"
