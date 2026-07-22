from abc import abstractmethod
from pathlib import Path
from typing import Protocol

from psautomater.models import Row


class InputReader(Protocol):
    """A plugin protocol for reading input files."""

    __filepath: Path

    def __init__(self, filepath: Path):
        """Initialize the InputReader with a file path.

        Args:
            filepath: The path to the input file.
        """

        self.__filepath = filepath

    @property
    def filepath(self) -> Path:
        return self.__filepath

    @abstractmethod
    def get_column_names(self) -> list[str]:
        """Returns a list of column names from the input file."""

    @abstractmethod
    def get_next_row(self) -> Row:
        """Yields the next row of data as a Row object."""

    @abstractmethod
    def get_previous_row(self) -> Row:
        """Returns the previous row of data from the input file."""

    @abstractmethod
    def get_row(self, idx: int) -> Row:
        """Returns the row of data at the specified index from the input file."""

    @abstractmethod
    def has_next_row(self) -> bool:
        """Returns True if there are more rows to read from the input file, False otherwise."""

    @abstractmethod
    def has_previous_row(self) -> bool:
        """Returns True if there are previous rows to read from the input file, False otherwise."""
