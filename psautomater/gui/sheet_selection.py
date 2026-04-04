from loguru import logger
from polars import DataFrame
from PySide6 import QtCore, QtWidgets


class SheetSelectionDialog(QtWidgets.QDialog):
    """Dialog to select a sheet from a spreadsheet and preview its contents."""

    def __init__(
        self,
        sheets: dict[str, DataFrame],
        parent: QtWidgets.QMainWindow | None = None,
    ):
        """Initialize the dialog.

        Args:
            sheets: A dictionary mapping sheet names to their corresponding DataFrames.
            parent: The parent widget of the dialog.
        """

        super().__init__(parent)
        self.sheets = sheets
        self.selected_sheet = None

        self.setWindowTitle("Select Sheet")
        self.resize(800, 600)

        self.setup_ui()
        self.populate_sheets()

    def setup_ui(self):
        """Set up the user interface of the dialog."""

        main_layout = QtWidgets.QVBoxLayout(self)

        # Splitter for left/right panels
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)

        # Left panel (list of sheets)
        self.sheet_list = QtWidgets.QListWidget()
        self.sheet_list.currentItemChanged.connect(self.on_sheet_selected)
        splitter.addWidget(self.sheet_list)

        # Right panel (table preview)
        self.preview_table = QtWidgets.QTableWidget()
        self.preview_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        splitter.addWidget(self.preview_table)

        # Give more space to the table
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        main_layout.addWidget(splitter)

        # Dialog buttons (OK / Cancel)
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def populate_sheets(self):
        """Populate the list widget with the sheet names."""

        for sheet_name in self.sheets.keys():
            self.sheet_list.addItem(sheet_name)

        if self.sheet_list.count() > 0:
            self.sheet_list.setCurrentRow(0)

    def on_sheet_selected(
        self,
        current: QtWidgets.QListWidgetItem,
        previous: QtWidgets.QListWidgetItem,  # pylint: disable=unused-argument
    ):
        """Update the preview table when a new sheet is selected.

        Args:
            current: The currently selected item in the sheet list.
            previous: The previously selected item in the sheet list.
        """

        if not current:
            return

        sheet_name = current.text()
        self.selected_sheet = sheet_name
        df: DataFrame = self.sheets[sheet_name]

        self.update_preview(df)

    def update_preview(self, df: DataFrame, max_rows: int = 100):
        """Update the preview table with the contents of the selected sheet.

        Args:
            df: The DataFrame containing the data to preview.
        """

        preview_df = df.head(max_rows)

        columns = preview_df.columns
        rows = preview_df.iter_rows()

        self.preview_table.clear()
        self.preview_table.setRowCount(preview_df.height)
        self.preview_table.setColumnCount(len(columns))
        self.preview_table.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.preview_table.setItem(row_idx, col_idx, item)

    def get_selected_sheet(self) -> str | None:
        """Return the name of the selected sheet.

        Returns:
            The name of the selected sheet, or None if no sheet is selected.
        """

        return self.selected_sheet

    def accept(self) -> None:
        """Log the selection before accepting and closing the dialog."""

        if self.selected_sheet:
            logger.info(f"User confirmed sheet selection: {self.selected_sheet}")
            logger.debug(
                f"There are a total of {self.sheets[self.selected_sheet].height} rows in the selected sheet."
            )
        else:
            logger.warning("User accepted the dialog but no sheet is selected.")

        super().accept()
