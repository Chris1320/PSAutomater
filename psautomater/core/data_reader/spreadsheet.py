from loguru import logger
from polars import DataFrame, read_excel


class SpreadsheetReader:
    """A class to read data from a spreadsheet file."""

    def __init__(self, file_path: str):
        """
        Args:
            file_path: The path to the spreadsheet file.
        """

        logger.debug(f"Initializing SpreadsheetReader with file path: {file_path}")
        self.file_path = file_path

    def get_data(self) -> dict[str, DataFrame]:
        """Return a the contents of the spreadsheet file.

        Returns:
            A dictionary with sheet names as the key to their corresponding `DataFrames`.
        """

        logger.info(f"Fetching sheet information from: {self.file_path}")
        sheets: dict[str, DataFrame] = read_excel(self.file_path, sheet_id=0)
        logger.debug(f"Retrieved sheets: {', '.join(list(sheets.keys()))}")
        return sheets
