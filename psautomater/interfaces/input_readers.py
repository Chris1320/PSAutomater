from abc import abstractmethod
from pathlib import Path
from typing import Protocol

from psautomater.models import InputData


class InputReader(Protocol):
    """A protocol for reading input files."""

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
    def read(self) -> InputData: ...
