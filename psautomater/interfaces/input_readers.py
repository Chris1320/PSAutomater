from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generator

from NodeGraphQt import BaseNode  # pyright: ignore[reportMissingTypeStubs]
from PySide6.QtWidgets import QWidget

from psautomater.models import Row


class InputReader(ABC):
    """A plugin protocol for reading input files."""

    def __init__(self):
        pass

    @property
    @abstractmethod
    def filepath(self) -> Path: ...

    @abstractmethod
    def get_column_names(self) -> list[str]:
        """Returns a list of column names from the input file."""

    @abstractmethod
    def get_next_row(self) -> Generator[Row, Any, Any]:
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


class InputReaderNodeView(ABC, BaseNode):
    """The UI node for the InputReader plugin protocol."""

    def __init__(self):
        """Initializes the InputReaderNodeView."""
        super().__init__()  # pyright: ignore[reportUnknownMemberType]

    @abstractmethod
    def show_initial_configuration_dialog(self) -> QWidget:
        """Returns the QWidget dialog to be shown for the initial configuration of the plugin."""

    @abstractmethod
    def show_configuration_dialog(self) -> QWidget:
        """Returns the QWidget dialog to be shown for the configuration of the plugin."""

    @abstractmethod
    def node_summary_widget(self) -> QWidget:
        """Returns the QWidget that shows in the node graph."""

    @abstractmethod
    def get_input_reader(self) -> InputReader:
        """Returns an instance of the InputReader plugin."""
