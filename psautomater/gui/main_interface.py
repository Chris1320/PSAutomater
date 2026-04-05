from pathlib import Path
from time import asctime

from loguru import logger
from PySide6 import QtCore, QtGui, QtWidgets

from psautomater.core import info, pyside6_types, resources
from psautomater.core.data_reader.spreadsheet import SpreadsheetReader
from psautomater.core.models import EditingStrategy, GenerationConfig
from psautomater.gui.layer_selection import LayerSelectionDialog
from psautomater.gui.sheet_selection import SheetSelectionDialog


class MainInterface(QtWidgets.QMainWindow):
    """The main widget of the program."""

    def __init__(self):
        logger.info("Initializing MainInterface...")
        super().__init__()

        editing_strategies = list(map(lambda x: x.value, EditingStrategy))

        self.resource_manager = resources.ImageManager()

        self.spreadsheet_txt = QtWidgets.QLineEdit()
        self.sheet_combo = QtWidgets.QComboBox()
        self.template_txt = QtWidgets.QLineEdit()
        self.output_dir_txt = QtWidgets.QLineEdit()

        self.auto_center_chk = QtWidgets.QCheckBox("Auto-Center Image")
        self.auto_crop_chk = QtWidgets.QCheckBox("Auto-Crop Image")
        self.remove_bg_chk = QtWidgets.QCheckBox("Remove Background")
        self.editing_strategy_combo = QtWidgets.QComboBox()
        self.editing_strategy_combo.addItems(editing_strategies)

        self.auto_center_chk.setChecked(True)
        self.auto_crop_chk.setChecked(True)
        self.remove_bg_chk.setChecked(True)
        self.editing_strategy_combo.setCurrentText(editing_strategies[0])

        self.layer_templates: dict[str, str] = {}

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

        self.main_layout.addLayout(self.add_header_layout())
        self.main_layout.addLayout(self.add_content_layout())
        self.main_layout.addLayout(self.add_footer_layout())

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
        sheet_layout = QtWidgets.QHBoxLayout()
        template_layout = QtWidgets.QHBoxLayout()
        output_dir_layout = QtWidgets.QHBoxLayout()

        spreadsheet_lbl = QtWidgets.QLabel("Spreadsheet File: ")
        self.spreadsheet_txt.setReadOnly(True)
        self.spreadsheet_txt.setPlaceholderText("spreadsheet.xlsx")
        spreadsheet_btn = pyside6_types.QPushButton("Browse...")
        spreadsheet_btn.setIcon(self.resource_manager["xlsx"])
        spreadsheet_btn.clicked.connect(self.choose_spreadsheet_file)

        sheet_lbl = QtWidgets.QLabel("Sheet: ")
        self.sheet_combo.setToolTip("Select the sheet to use")
        self.sheet_combo.currentTextChanged.connect(self.on_sheet_changed)
        sheet_layout.addWidget(sheet_lbl)
        sheet_layout.addWidget(self.sheet_combo)

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

        output_dir_lbl = QtWidgets.QLabel("Output Directory: ")
        self.output_dir_txt.setReadOnly(True)
        self.output_dir_txt.setPlaceholderText("Select output folder...")
        output_dir_btn = pyside6_types.QPushButton("Browse...")
        output_dir_btn.setIcon(self.resource_manager["output"])
        output_dir_btn.clicked.connect(self.choose_output_directory)
        output_dir_layout.addWidget(output_dir_lbl)
        output_dir_layout.addWidget(output_dir_btn)

        options_layout = QtWidgets.QHBoxLayout()
        options_layout.addWidget(self.auto_center_chk)
        options_layout.addWidget(self.auto_crop_chk)
        options_layout.addWidget(self.remove_bg_chk)

        strategy_layout = QtWidgets.QHBoxLayout()
        strategy_lbl = QtWidgets.QLabel("Editing Strategy: ")
        strategy_layout.addWidget(strategy_lbl)
        strategy_layout.addWidget(self.editing_strategy_combo)

        start_button = pyside6_types.QPushButton("Start Generation")
        start_button.setIcon(self.resource_manager["start"])
        start_button.clicked.connect(self.start_process)

        main_pane_layout.addLayout(spreadsheet_layout)
        main_pane_layout.addWidget(self.spreadsheet_txt)
        main_pane_layout.addSpacing(10)
        main_pane_layout.addLayout(sheet_layout)
        main_pane_layout.addSpacing(30)
        main_pane_layout.addLayout(template_layout)
        main_pane_layout.addWidget(self.template_txt)
        main_pane_layout.addSpacing(30)
        main_pane_layout.addLayout(output_dir_layout)
        main_pane_layout.addWidget(self.output_dir_txt)
        main_pane_layout.addSpacing(30)
        main_pane_layout.addLayout(options_layout)
        main_pane_layout.addSpacing(10)
        main_pane_layout.addLayout(strategy_layout)
        main_pane_layout.addSpacing(100)
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
            self.output_pane.append(
                f"Selected spreadsheet: {dialog.selectedFiles()[0]}"
            )
            try:
                spreadsheet_reader = SpreadsheetReader(dialog.selectedFiles()[0])
                sheets = spreadsheet_reader.get_data()
                # Ask the user which sheet to use, if there are multiple sheets in the spreadsheet.
                selection_dialog = SheetSelectionDialog(sheets, self)

                selected_sheet = None
                if selection_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    selected_sheet = selection_dialog.get_selected_sheet()
                else:
                    logger.info("Sheet selection cancelled by user.")
                    return

                # Update the combobox with available sheets
                self.sheet_combo.clear()
                self.sheet_combo.addItems(list(sheets.keys()))

                if selected_sheet:
                    logger.info(f"Selected sheet: {selected_sheet}")
                    self.sheet_combo.setCurrentText(selected_sheet)

            except Exception as e:
                logger.error("Error reading spreadsheet: {0}", e)
                return

            self.spreadsheet_txt.setText(dialog.selectedFiles()[0])

    def on_sheet_changed(self, text: str) -> None:
        """Log the sheet change to the output pane."""

        if text:
            logger.info(f"Target sheet changed to: {text}")
            self.output_pane.append(f"Target sheet changed to: {text}")

    def choose_template_file(self) -> None:
        """Ask the user for the template file."""

        if not self.spreadsheet_txt.text() or not self.sheet_combo.currentText():
            logger.error("Spreadsheet and target sheet not selected before template.")
            QtWidgets.QMessageBox.critical(
                self,
                "Spreadsheet Required",
                "Please select a spreadsheet file and a target sheet before choosing a template.",
            )
            return

        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle("Choose Template File")
        dialog.setNameFilter("Photoshop Files (*.psd)")
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        logger.info("Asking user for template location...")
        result = dialog.exec()

        if result == dialog.DialogCode.Accepted:
            logger.debug("Template filepath: {0}", dialog.selectedFiles()[0])
            template_path = dialog.selectedFiles()[0]
            self.template_txt.setText(template_path)
            self.output_pane.append(f"Selected template: {template_path}")

            try:
                # Read spreadsheet to extract columns for templating
                spreadsheet_reader = SpreadsheetReader(self.spreadsheet_txt.text())
                sheets = spreadsheet_reader.get_data()
                target_sheet = self.sheet_combo.currentText()
                columns = list(sheets[target_sheet].columns)

                layer_dialog = LayerSelectionDialog(template_path, columns, self)
                if layer_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    self.layer_templates = layer_dialog.get_layer_templates()
                    logger.info("Layer templates configured successfully.")
                    self.output_pane.append(
                        f"Mapped {len(self.layer_templates)} template(s)."
                    )
                else:
                    logger.info("Layer selection cancelled by user.")

            except Exception as e:
                logger.error(f"Error reading PSD layers: {e}")

    def choose_output_directory(self) -> None:
        """Ask the user for the output directory."""

        logger.info("Asking user for output directory...")
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose Output Directory"
        )

        if directory:
            logger.debug(f"Output directory: {directory}")
            self.output_dir_txt.setText(directory)
            self.output_pane.append(f"Selected output directory: {directory}")

    def prepare_inputs(self) -> GenerationConfig:
        """Prepare the inputs for the generation process.

        Returns:
            The configuration for the generation process.

        Raises:
            ValueError: If any of the required inputs are missing.
        """

        logger.info("Preparing inputs for generation process...")
        if not self.spreadsheet_txt.text():
            logger.error("No spreadsheet file selected.")
            QtWidgets.QMessageBox.critical(
                self,
                "Spreadsheet File Required",
                "Please select a spreadsheet file before starting the generation process.",
            )
            raise ValueError("No spreadsheet file selected.")

        if not self.sheet_combo.currentText():
            logger.error("No target sheet selected.")
            QtWidgets.QMessageBox.critical(
                self,
                "Target Sheet Required",
                "Please select a target sheet before starting the generation process.",
            )
            raise ValueError("No target sheet selected.")

        if not self.template_txt.text():
            logger.error("No template file selected.")
            QtWidgets.QMessageBox.critical(
                self,
                "Template File Required",
                "Please select a template file before starting the generation process.",
            )
            raise ValueError("No template file selected.")

        if not self.output_dir_txt.text():
            logger.error("No output directory selected.")
            QtWidgets.QMessageBox.critical(
                self,
                "Output Directory Required",
                "Please select an output directory before starting the generation process.",
            )
            raise ValueError("No output directory selected.")

        generation_config = GenerationConfig(
            spreadsheet_path=Path(self.spreadsheet_txt.text()),
            target_sheet=self.sheet_combo.currentText(),
            template_path=Path(self.template_txt.text()),
            output_dir=Path(self.output_dir_txt.text()),
            layer_templates=self.layer_templates,
            feature_auto_crop_image=self.auto_crop_chk.isChecked(),
            feature_auto_center_image=self.auto_center_chk.isChecked(),
            feature_remove_background=self.remove_bg_chk.isChecked(),
            editing_strategy=EditingStrategy(self.editing_strategy_combo.currentText()),
        )

        return generation_config

    def start_process(self) -> None:
        """Start the generation of images."""

        # Check for required inputs
        try:
            generation_config: GenerationConfig = self.prepare_inputs()

            self.output_pane.append("Configuration:")
            self.output_pane.append(
                f"    - Spreadsheet: {generation_config.spreadsheet_path}"
            )
            self.output_pane.append(
                f"    - Target Sheet: {generation_config.target_sheet}"
            )
            self.output_pane.append(
                f"    - Template: {generation_config.template_path}"
            )
            self.output_pane.append(
                f"    - Output Directory: {generation_config.output_dir}"
            )
            self.output_pane.append(
                f"    - Editing Strategy: {generation_config.editing_strategy.value}"
            )

            self.output_pane.append("\nFeatures:")
            auto_center_image_enabled = (
                "Yes" if generation_config.feature_auto_center_image else "No"
            )
            auto_crop_image_enabled = (
                "Yes" if generation_config.feature_auto_crop_image else "No"
            )
            remove_background_enabled = (
                "Yes" if generation_config.feature_remove_background else "No"
            )
            self.output_pane.append(
                f"    - Auto-Center Image: {auto_center_image_enabled}"
            )
            self.output_pane.append(f"    - Auto-Crop Image: {auto_crop_image_enabled}")
            self.output_pane.append(
                f"    - Remove Background: {remove_background_enabled}"
            )

            self.start_time_lbl.setText(asctime())
            logger.info("Generation started...")
            self.output_pane.append("Generation started...")

        except ValueError as e:
            logger.error(f"Error starting generation process: {e}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self.output_pane.append(f"Unexpected error: {e}")
