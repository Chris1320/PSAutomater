"""Application entry point for launching the PSAutomater GUI."""

import sys
from loguru import logger
from PySide6.QtWidgets import QApplication

from psautomater.core import info
from psautomater.gui import main_interface


def main() -> int:
    """The main entry point of the program.

    Returns:
        The error code of the program.
    """

    logger.add(
        info.logfile_path,
        format=info.LOGFILE_FORMAT,
        backtrace=True,
        level=(
            info.LOGGING_DEBUG_MODE
            if "--debug" in sys.argv
            else info.LOGGING_RELEASE_MODE
        ),
    )
    logger.info("The program has started.")
    logger.debug("args: ({0})", ", ".join(sys.argv))

    app = QApplication(sys.argv)
    logger.debug("Minimum Window Size: {0}", info.WINDOW_SIZE["min"])
    logger.debug("Maximum Window Size: {0}", info.WINDOW_SIZE["max"])
    logger.debug(
        "User Screen Size: {0}x{1} ({2}x{3})",
        app.primaryScreen().availableGeometry().width(),
        app.primaryScreen().availableGeometry().height(),
        app.primaryScreen().size().width(),
        app.primaryScreen().size().height(),
    )

    widget = main_interface.MainInterface()
    widget.setMinimumSize(info.WINDOW_SIZE["min"][0], info.WINDOW_SIZE["min"][1])
    widget.setMaximumSize(info.WINDOW_SIZE["max"][0], info.WINDOW_SIZE["max"][1])
    widget.show()

    logger.info("Running main event loop.")
    ret_code = app.exec()
    logger.info("The application exited with error code {0}.", ret_code)
    return ret_code


if __name__ == "__main__":
    sys.exit(main())
