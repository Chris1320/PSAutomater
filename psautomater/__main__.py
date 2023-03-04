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

import sys

from loguru import logger
from PySide6.QtWidgets import QApplication

from psautomater.core import info
from psautomater.gui import mainInterface


def main() -> int:
    """
    The main function of the program.

    :returns: The error code of the program.
    """

    logger.add(
        info.logfile_path,
        format=info.LOGFILE_FORMAT,
        backtrace=True,
        level=info.LOGGING_DEBUG_MODE
        if "--debug" in sys.argv
        else info.LOGGING_RELEASE_MODE
    )
    logger.info("The program has started.")
    logger.debug("args: ({0})", ', '.join(sys.argv))

    app = QApplication(sys.argv)
    logger.debug("Minimum Window Size: {0}", info.WINDOW_SIZE["min"])
    logger.debug("Maximum Window Size: {0}", info.WINDOW_SIZE["max"])
    logger.debug(
        "User Screen Size: {0}x{1} ({2}x{3})",
        app.primaryScreen().availableGeometry().width(),
        app.primaryScreen().availableGeometry().height(),
        app.primaryScreen().size().width(),
        app.primaryScreen().size().height()
    )

    widget = mainInterface.MainInterface()
    widget.setMinimumSize(info.WINDOW_SIZE["min"][0], info.WINDOW_SIZE["min"][1])
    widget.setMaximumSize(info.WINDOW_SIZE["max"][0], info.WINDOW_SIZE["max"][1])
    widget.show()

    logger.info("Running main event loop.")
    ret_code = app.exec()
    logger.info("The application exited with error code {0}.", ret_code)
    return ret_code


if __name__ == "__main__":
    sys.exit(main())
