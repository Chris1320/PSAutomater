from typing import Callable

from loguru import logger
from PySide6 import QtCore

from psautomater.core.models import GenerationConfig


class OutputGenerator(QtCore.QThread):
    """
    Thread to run the generation process in the background
    without freezing the main GUI.
    """

    __progress_updated = QtCore.Signal(int, int)  # current, total
    __log_updated = QtCore.Signal(str)  # log message
    __finished = QtCore.Signal()  # emitted when generation is complete
    __error = QtCore.Signal(str)  # emitted when an error occurs

    def __init__(
        self,
        config: GenerationConfig,
        progress_updated_hooks: list[Callable[[int, int], None]] | None = None,
        log_updated_hooks: list[Callable[[str], None]] | None = None,
        finished_hooks: list[Callable[[], None]] | None = None,
        error_hooks: list[Callable[[str], None]] | None = None,
        parent: QtCore.QObject | None = None,
    ):
        logger.debug("Initializing Generator thread...")
        super().__init__(parent)
        self.config = config

        logger.info("Connecting `progress_updated` hooks...")
        for hook in progress_updated_hooks or []:
            logger.debug(f"Connecting hook: {hook}")
            self.__progress_updated.connect(hook)

        logger.info("Connecting `log_updated` hooks...")
        for hook in log_updated_hooks or []:
            logger.debug(f"Connecting hook: {hook}")
            self.__log_updated.connect(hook)

        logger.info("Connecting `finished` hooks...")
        for hook in finished_hooks or []:
            logger.debug(f"Connecting hook: {hook}")
            self.__finished.connect(hook)

        logger.info("Connecting `error` hooks...")
        for hook in error_hooks or []:
            logger.debug(f"Connecting hook: {hook}")
            self.__error.connect(hook)
