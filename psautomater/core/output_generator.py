from pathlib import Path
from typing import Callable

from loguru import logger
from polars import DataFrame
from PySide6 import QtCore

from psautomater.core.data_reader.spreadsheet import SpreadsheetReader
from psautomater.core.models import EditingStrategy, GenerationConfig
from psautomater.core.psd_engines.photoshop_com_api import PhotoshopComAPI


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
        """
        Args:
            config: GenerationConfig object containing all generation settings.
            progress_updated_hooks: List of callables to connect to progress updates.
            log_updated_hooks: List of callables to connect to log updates.
            finished_hooks: List of callables to connect to finished signal.
            error_hooks: List of callables to connect to error signal.
            parent: Optional parent QObject for the thread.
        """

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

        self.target_df: DataFrame | None = None
        self.total_rows: int | None = None

    def run(self) -> None:
        engine: PhotoshopComAPI | None = None
        try:
            self.__log_updated.emit("Generation started...")
            logger.info("Generation started from worker thread...")

            # Load spreadsheet data
            self.load_data()
            self.__progress_updated.emit(0, self.total_rows)

            # Load Photoshop engine
            if self.config.editing_strategy == EditingStrategy.COM:
                self.__log_updated.emit("Initializing Photoshop COM API...")
                engine = PhotoshopComAPI(Path(self.config.template_path))

            else:
                raise ValueError(
                    "Only 'PhotoshopComAPI' engine is supported currently."
                )

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"Error during generation: {e}")
            self.__error.emit(str(e))

        finally:
            if engine:
                engine.close()

            self.__finished.emit()

    def load_data(self) -> None:
        """Load the spreadsheet data.

        Raises:
            ValueError: If the target sheet is not found in the spreadsheet.
        """

        self.__log_updated.emit("Loading sheet data...")
        spreadsheet_reader = SpreadsheetReader(self.config.spreadsheet_path)
        sheets = spreadsheet_reader.get_data()

        logger.debug(f"Available sheets in spreadsheet: {list(sheets.keys())}")
        if self.config.target_sheet not in sheets:
            m = f"Target sheet '{self.config.target_sheet}' not found in spreadsheet."
            logger.error(m)
            # we don't add a `self.__error.emit(m)` here because the caller will catch
            # this exception and emit the error signal with the exception message,
            # so emitting here would cause duplicate error signals.
            raise ValueError(m)

        self.target_df = sheets[self.config.target_sheet]
        self.total_rows = self.target_df.height
        logger.debug(
            f"Loaded data from sheet `{self.config.target_sheet}`. ({self.total_rows} rows)"
        )
