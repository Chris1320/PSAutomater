from pathlib import Path
from typing import Any, Final, Generator

from PySide6 import QtWidgets

from psautomater.interfaces.input_readers import InputReader, InputReaderNode
from psautomater.models import NodeKind, Row

UID: Final[str] = "chris1320.template_plugin"
NAME: Final[str] = "Input Reader Template"
VERSION: Final[str] = "1.0.0"
KIND: Final[NodeKind] = NodeKind.INPUT_READER


class InputReaderPlugin(InputReader):
    """Template input reader plugin."""

    HEADERS: Final[list[str]] = ["Column1", "Column2", "Column3"]
    SAMPLE_DATA: Final[list[list[str]]] = [
        ["Data 1-1", "Data 1-2", "Data 1-3"],
        ["Data 2-1", "Data 2-2", "Data 2-3"],
        ["Data 3-1", "Data 3-2", "Data 3-3"],
        ["Data 4-1", "Data 4-2", "Data 4-3"],
        ["Data 5-1", "Data 5-2", "Data 5-3"],
    ]

    def __init__(self, filepath: Path):
        super().__init__()
        self.curr_idx = 0
        self._filepath = filepath

    @property
    def filepath(self) -> Path:
        return self._filepath

    def get_column_names(self) -> list[str]:
        return self.HEADERS

    def get_next_row(self) -> Generator[Row, Any, Any]:
        for row_data in self.SAMPLE_DATA:
            yield Row(
                index=self.curr_idx,
                data=dict(zip(self.HEADERS, row_data)),
            )
            self.curr_idx += 1

    def get_previous_row(self) -> Row:
        if self.curr_idx > 0:
            self.curr_idx -= 1
            row_data = self.SAMPLE_DATA[self.curr_idx]
            return Row(
                index=self.curr_idx,
                data=dict(zip(self.HEADERS, row_data)),
            )

        else:
            raise IndexError("No previous row available.")

    def get_row(self, idx: int) -> Row:
        if 0 <= idx < len(self.SAMPLE_DATA):
            row_data = self.SAMPLE_DATA[idx]
            return Row(
                index=idx,
                data=dict(zip(self.HEADERS, row_data)),
            )

        else:
            raise IndexError("Row index out of range.")

    def has_next_row(self) -> bool:
        return self.curr_idx < len(self.SAMPLE_DATA)

    def has_previous_row(self) -> bool:
        return self.curr_idx > 0


class InputReaderPluginNode(InputReaderNode):
    """Template input reader plugin node."""

    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout(self.widget)

        self.filepath_label = QtWidgets.QLabel("File Path:")
        self.filepath_input = QtWidgets.QLineEdit()

        self.layout.addWidget(self.filepath_label)
        self.layout.addWidget(self.filepath_input)
        self.widget.setLayout(self.layout)

    def show_initial_configuration_dialog(self) -> QtWidgets.QWidget:
        return self.widget

    def show_configuration_dialog(self) -> QtWidgets.QWidget:
        return self.widget

    def node_summary_widget(self) -> QtWidgets.QWidget:
        summary_widget = QtWidgets.QWidget()
        summary_layout = QtWidgets.QVBoxLayout(summary_widget)

        name_label = QtWidgets.QLabel(f"Plugin: {NAME}")
        version_label = QtWidgets.QLabel(f"Version: {VERSION}")

        summary_layout.addWidget(name_label)
        summary_layout.addWidget(version_label)
        summary_widget.setLayout(summary_layout)

        return summary_widget

    def get_input_reader(self) -> InputReaderPlugin:
        return InputReaderPlugin(Path(self.filepath_input.text()))
