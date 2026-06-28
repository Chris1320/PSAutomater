from pathlib import Path
from typing import Any, Callable

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
            engine = self.load_engine()

            # Start processing rows
            if self.target_df is None or self.total_rows is None:
                logger.error("Spreadsheet data not loaded properly.")
                raise ValueError("Spreadsheet data not loaded properly.")

            logger.debug(f"Starting row processing loop for {self.total_rows} rows...")
            for idx, row in enumerate(self.target_df.iter_rows(named=True)):
                logger.info(f"Processing row {idx + 1} of {self.total_rows}")
                logger.debug(f"Row data: {row}")
                result: tuple[int, bool] = self.process_row(idx, row)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"Error during generation: {e}")
            self.__error.emit(str(e))

        finally:
            if engine:
                logger.debug("Closing Photoshop engine...")
                engine.close()

            logger.debug("Emitting finished signal...")
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

    def load_engine(self) -> PhotoshopComAPI:
        """Load the Photoshop editing engine."""

        logger.debug(f"Selected engine: {self.config.editing_strategy}")
        if self.config.editing_strategy == EditingStrategy.COM:
            self.__log_updated.emit("Initializing Photoshop COM API...")
            engine = PhotoshopComAPI(Path(self.config.template_path))

        else:
            logger.error(
                f"Unsupported editing strategy: {self.config.editing_strategy}"
            )
            raise ValueError("Only 'PhotoshopComAPI' engine is supported currently.")

        return engine

    def process_row(self, idx: int, row: dict[str, Any]) -> tuple[int, bool]:
        """Process a single row of the spreadsheet data.

        Returns:
            A tuple containing the current row index and a boolean indicating success.
        """

        current_count = idx + 1
        logger.info(f"Processing row {current_count}/{self.total_rows}")
        self.__log_updated.emit(f"Processing row {current_count}/{self.total_rows}...")

        # Format the output filename using the current row data
        try:
            output_filename = self.config.output_filename_format.format(**row)

        except KeyError as e:
            msg = f"Error: Missing column in filename format {e}. Skipping row..."
            logger.error(msg)
            self.__log_updated.emit(msg)
            self.__progress_updated.emit(current_count, self.total_rows)
            return (idx, False)

        output_path = Path(self.config.output_dir) / output_filename
        logger.debug(f"Target output path: {output_path}")

        # Replace content of layers based on the current row data
        for layer_name, template_val in self.config.layer_templates.items():
            if not template_val:
                logger.debug(
                    f"No template value provided for layer '{layer_name}'. Skipping..."
                )
                continue

            # TODO: determine layer type first, then proceed with replacement.
            # This will require a rewrite of the current PhotoshopComAPI engine.
            try:
                evaluated_val = str(template_val).format(**row)

            except KeyError as e:
                logger.warning(
                    f"Key error {e} replacing layer '{layer_name}'. Value not modified..."
                )
                evaluated_val = str(template_val)

        return (idx, True)
