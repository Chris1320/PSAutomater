from time import asctime

from loguru import logger
from PySide6 import QtCore, QtGui, QtWidgets

from psautomater.core import info, pyside6_types, resources


class MainInterface(QtWidgets.QMainWindow):
    """The main widget of the program."""

    def __init__(self):
        logger.info("Initializing MainInterface...")
        super().__init__()

        self.resource_manager = resources.ImageManager()

        # The program output will be shown here.
        self.spreadsheet_txt = QtWidgets.QLineEdit()
        self.template_txt = QtWidgets.QLineEdit()
        self.process_progress_bar = QtWidgets.QProgressBar()
        self.start_time_lbl = QtWidgets.QLabel()
        self.end_time_lbl = QtWidgets.QLabel()
        self.total_time_lbl = QtWidgets.QLabel()
        self.output_pane = QtWidgets.QTextEdit()
        self.output_pane.setToolTip("You will see the program output here.")
        self.output_pane.setReadOnly(True)

        # Initialize main container and layout.
        self.main_container = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.add_header_layout())  # Add the header layout.
        self.main_layout.addLayout(self.add_content_layout())  # Add the main contents.
        self.main_layout.addLayout(self.add_footer_layout())  # Add the footer layout.

        self.main_container.setLayout(self.main_layout)
        self.setWindowTitle(info.NAME)
        self.setWindowIcon(self.resource_manager["icon"])
        self.setCentralWidget(self.main_container)
        logger.info("MainInterface initialization done.")

    def add_header_layout(self) -> QtWidgets.QLayout:
        """Add the program header to the main layout."""

        layout = QtWidgets.QHBoxLayout()

        icon = QtWidgets.QLabel()
        icon.setPixmap(
            self.resource_manager["icon"].scaled(
                50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
        )
        icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        title = QtWidgets.QLabel(info.NAME)
        title.setFont(QtGui.QFont("Arial", 38))
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(icon)
        layout.addWidget(title)

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        return layout

    def add_footer_layout(self) -> QtWidgets.QLayout:
        """Add the footer widgets."""

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.process_progress_bar)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        return layout

    def add_content_layout(self) -> QtWidgets.QLayout:
        """Return the layout that contains widgets of the main program."""

        main_content_layout = QtWidgets.QHBoxLayout()
        left_pane_layout = self.create_left_content_pane()
        right_pane_layout = self.create_right_content_pane()

        main_content_layout.addLayout(left_pane_layout)
        main_content_layout.addLayout(right_pane_layout)
        main_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        return main_content_layout

    def create_right_content_pane(self) -> QtWidgets.QLayout:
        """Return the right side of the main content pane."""

        pane_layout = QtWidgets.QVBoxLayout()
        start_time_layout = QtWidgets.QHBoxLayout()
        end_time_layout = QtWidgets.QHBoxLayout()
        total_time_layout = QtWidgets.QHBoxLayout()

        start_time_lbl = QtWidgets.QLabel("Start Time: ")
        start_time_layout.addWidget(start_time_lbl)
        start_time_layout.addWidget(self.start_time_lbl)
        start_time_layout.setContentsMargins(50, 0, 50, 0)
        start_time_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        end_time_lbl = QtWidgets.QLabel("End Time: ")
        end_time_layout.addWidget(end_time_lbl)
        end_time_layout.addWidget(self.end_time_lbl)
        end_time_layout.setContentsMargins(50, 0, 50, 0)
        end_time_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        total_time_lbl = QtWidgets.QLabel("Total Time: ")
        total_time_layout.addWidget(total_time_lbl)
        total_time_layout.addWidget(self.total_time_lbl)
        total_time_layout.setContentsMargins(50, 0, 50, 0)
        total_time_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        pane_layout.addWidget(self.output_pane)
        pane_layout.addLayout(start_time_layout)
        pane_layout.addLayout(end_time_layout)
        pane_layout.addLayout(total_time_layout)

        return pane_layout

    def create_left_content_pane(self) -> QtWidgets.QLayout:
        """Return the left side of the main content pane."""

        main_pane_layout = QtWidgets.QVBoxLayout()
        spreadsheet_layout = QtWidgets.QHBoxLayout()
        template_layout = QtWidgets.QHBoxLayout()

        spreadsheet_lbl = QtWidgets.QLabel("Spreadsheet File: ")
        self.spreadsheet_txt.setReadOnly(True)
        self.spreadsheet_txt.setPlaceholderText("spreadsheet.xlsx")
        spreadsheet_btn = pyside6_types.QPushButton("Browse...")
        spreadsheet_btn.setIcon(self.resource_manager["xlsx"])
        spreadsheet_btn.clicked.connect(self.choose_spreadsheet_file)

        template_lbl = QtWidgets.QLabel("Template File: ")
        self.template_txt.setReadOnly(True)
        self.template_txt.setPlaceholderText("template.psd")
        template_btn = pyside6_types.QPushButton("Browse...")
        template_btn.setIcon(self.resource_manager["psd"])
        template_btn.clicked.connect(self.choose_template_file)

        spreadsheet_layout.addWidget(spreadsheet_lbl)
        spreadsheet_layout.addWidget(spreadsheet_btn)
        template_layout.addWidget(template_lbl)
        template_layout.addWidget(template_btn)

        start_button = pyside6_types.QPushButton("Start Generation")
        start_button.setIcon(self.resource_manager["start"])
        start_button.clicked.connect(self.start_process)

        main_pane_layout.addLayout(spreadsheet_layout)
        main_pane_layout.addWidget(self.spreadsheet_txt)
        main_pane_layout.addSpacing(50)
        main_pane_layout.addLayout(template_layout)
        main_pane_layout.addWidget(self.template_txt)
        main_pane_layout.addSpacing(200)
        main_pane_layout.addWidget(start_button)
        return main_pane_layout

    def choose_spreadsheet_file(self) -> None:
        """Ask the user for the spreadsheet file."""

        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle("Choose Spreadsheet File")
        dialog.setNameFilter("Spreadsheet Files (*.xlsx)")
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        logger.info("Asking user for spreadsheet location...")
        result = dialog.exec()

        if result == dialog.DialogCode.Accepted:
            logger.debug("Spreadsheet filepath: {0}", dialog.selectedFiles()[0])
            self.spreadsheet_txt.setText(dialog.selectedFiles()[0])

    def choose_template_file(self) -> None:
        """Ask the user for the template file."""

        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle("Choose Template File")
        dialog.setNameFilter("Photoshop Files (*.psd)")
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        logger.info("Asking user for template location...")
        result = dialog.exec()

        if result == dialog.DialogCode.Accepted:
            logger.debug("Template filepath: {0}", dialog.selectedFiles()[0])
            self.template_txt.setText(dialog.selectedFiles()[0])

    def start_process(self) -> None:
        """Start the generation of images."""

        # TODO: Continue this.

        self.start_time_lbl.setText(asctime())
        logger.info("Generation started...")
        self.output_pane.setText("Generation started...")
