# pylint: disable=line-too-long

from loguru import logger
from PIL.ImageQt import ImageQt
from psd_tools import PSDImage
from psd_tools.api.layers import Layer
from PySide6 import QtCore, QtGui, QtWidgets


class LayerSelectionDialog(QtWidgets.QDialog):
    """Dialog to template layers from a PSD file."""

    def __init__(
        self,
        psd_path: str,
        spreadsheet_columns: list[str],
        parent: QtWidgets.QMainWindow | None = None,
    ):
        super().__init__(parent)
        self.psd_path = psd_path
        self.spreadsheet_columns = spreadsheet_columns
        self.layer_templates: dict[str, str] = {}

        self.setWindowTitle("Template Layers")
        self.resize(1000, 600)

        # Load PSD
        logger.info(f"Loading PSD for layer selection: {self.psd_path}")
        self.psd = PSDImage.open(  # pyright: ignore[reportUnknownMemberType]
            self.psd_path
        )
        # Flatten all layers into a list for easy access
        self.layers = list(self.psd.descendants())
        logger.info(f"Found {len(self.layers)} layers in the PSD.")

        self.setup_ui()
        self.populate_layers()

    def setup_ui(self):
        """Set up the dialog's UI components."""

        main_layout = QtWidgets.QVBoxLayout(self)

        # Splitter for left/middle/right panels
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)

        # Left panel (list of layers)
        self.layer_list = QtWidgets.QListWidget()
        self.layer_list.currentItemChanged.connect(self.on_layer_selected)
        splitter.addWidget(self.layer_list)

        # Middle panel (templater)
        middle_widget = QtWidgets.QWidget()
        middle_layout = QtWidgets.QVBoxLayout(middle_widget)
        self.templater_label = QtWidgets.QLabel("Select a layer to template")
        self.templater_input = QtWidgets.QTextEdit()
        self.templater_input.textChanged.connect(self.on_template_text_changed)
        self.templater_input.setEnabled(False)

        self.templater_combo = QtWidgets.QComboBox()
        self.templater_combo.addItems(
            ["-- Do not template --"] + self.spreadsheet_columns
        )
        self.templater_combo.currentTextChanged.connect(self.on_template_combo_changed)
        self.templater_combo.setVisible(False)

        middle_layout.addWidget(self.templater_label)
        middle_layout.addWidget(self.templater_input)
        middle_layout.addWidget(self.templater_combo)
        middle_layout.addStretch()
        splitter.addWidget(middle_widget)

        # Right panel (preview image)
        self.preview_label = QtWidgets.QLabel("Preview")
        self.preview_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: #333; color: white;")
        splitter.addWidget(self.preview_label)

        # Ratios for splitter panels
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 2)

        main_layout.addWidget(splitter)

        # Dialog buttons (OK / Cancel)
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def populate_layers(self):
        """Populate the layer list with names and store references for templating."""

        for layer in self.layers:
            if layer.kind not in ("pixel", "type"):
                logger.debug(
                    f"Skipping layer `{layer.name}` of unsupported type `{layer.kind}`"
                )
                continue

            # Use data role to store layer index/reference
            item = QtWidgets.QListWidgetItem(f"{layer.name} ({layer.kind})")
            # Store layer object reference in item data
            item.setData(QtCore.Qt.ItemDataRole.UserRole, layer)
            self.layer_list.addItem(item)

            # Initialize empty templates for type layers
            if layer.kind == "type":
                logger.debug(f"Adding layer `{layer.name}` to templating options.")
                self.layer_templates[layer.name] = (
                    layer.text  # pyright: ignore[reportUnknownMemberType,reportAttributeAccessIssue]
                )
            elif layer.kind == "pixel":
                logger.debug(f"Adding layer `{layer.name}` to templating options.")
                self.layer_templates[layer.name] = ""

        logger.info(
            f"Added {self.layer_list.count()} templatable layers out of {len(self.layers)} total layers to the list."
        )
        if self.layer_list.count() > 0:
            self.layer_list.setCurrentRow(0)

    def on_layer_selected(
        self,
        current: QtWidgets.QListWidgetItem,
        previous: QtWidgets.QListWidgetItem,  # pylint: disable=unused-argument
    ):
        if not current:
            return

        layer = current.data(QtCore.Qt.ItemDataRole.UserRole)

        # Update templater
        if layer.kind == "type":
            self.templater_label.setText("Text Template:")
            self.templater_input.setVisible(True)
            self.templater_combo.setVisible(False)
            self.templater_input.setEnabled(True)
            # Load existing template if it was modified, else the layer's original text
            current_text = self.layer_templates.get(layer.name, layer.text)
            self.templater_input.blockSignals(True)
            self.templater_input.setText(current_text)
            self.templater_input.blockSignals(False)
        elif layer.kind == "pixel":
            self.templater_label.setText("Image Source Column:")
            self.templater_input.setVisible(False)
            self.templater_combo.setVisible(True)
            current_val = self.layer_templates.get(layer.name, "")
            self.templater_combo.blockSignals(True)
            if not current_val:
                self.templater_combo.setCurrentIndex(0)
            else:
                # current_val is expected to be in formatted style, e.g. "{column_name}"
                col_name = current_val.strip("{}")
                self.templater_combo.setCurrentText(col_name)
            self.templater_combo.blockSignals(False)
        else:
            self.templater_label.setText("Image templating is unsupported.")
            self.templater_input.setVisible(True)
            self.templater_combo.setVisible(False)
            self.templater_input.setEnabled(False)
            self.templater_input.blockSignals(True)
            self.templater_input.clear()
            self.templater_input.blockSignals(False)

        # Update preview
        self.update_preview(layer)

    def on_template_text_changed(self):
        current_item = self.layer_list.currentItem()
        if not current_item:
            return

        layer = current_item.data(QtCore.Qt.ItemDataRole.UserRole)
        if layer.kind == "type":
            self.layer_templates[layer.name] = self.templater_input.toPlainText()

    def on_template_combo_changed(self, text: str):
        current_item = self.layer_list.currentItem()
        if not current_item:
            return

        layer = current_item.data(QtCore.Qt.ItemDataRole.UserRole)
        if layer.kind == "pixel":
            if text == "-- Do not template --":
                self.layer_templates[layer.name] = ""
            else:
                # Store the template variable name directly, e.g. {column}
                self.layer_templates[layer.name] = "{" + text + "}"

    def update_preview(self, layer: Layer) -> None:
        """Generate and display a PIL image for the layer."""

        self.preview_label.setText("Loading preview...")

        # NOTE: Process the image in the main thread (might be slow for large PSDs, but acceptable for now)
        try:
            pil_image = layer.topil()
            if pil_image is None:
                self.preview_label.setText("No preview available")
                return

            # Convert PIL image to QPixmap
            # Ensure image is RGBA
            if pil_image.mode != "RGBA":
                pil_image = pil_image.convert("RGBA")

            qimage = ImageQt(pil_image)
            pixmap = QtGui.QPixmap.fromImage(qimage)

            # Scale to fit label
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            self.preview_label.setPixmap(scaled_pixmap)

        except Exception as e:
            logger.error(f"Failed to generate preview: {e}")
            self.preview_label.setText("Preview error")

    def resizeEvent(self, event: QtGui.QResizeEvent):  # pylint: disable=invalid-name
        super().resizeEvent(event)
        # Re-scale preview when dialog resizes
        current_item = self.layer_list.currentItem()
        if current_item:
            layer = current_item.data(QtCore.Qt.ItemDataRole.UserRole)
            self.update_preview(layer)

    def get_layer_templates(self) -> dict[str, str]:
        """Return the user-defined templates."""

        return self.layer_templates
