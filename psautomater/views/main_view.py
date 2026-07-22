from loguru import logger
from NodeGraphQt import NodeGraph  # pyright: ignore[reportMissingTypeStubs]
from PySide6 import QtCore, QtGui, QtWidgets

from psautomater.controllers import info, plugin_manager, resource_manager
from psautomater.models import NodeKind

NODE_CATEGORIES: list[tuple[NodeKind, str]] = [
    (NodeKind.INPUT_READER, "Input Readers"),
    (NodeKind.HOOK, "Hooks"),
    (NodeKind.OUTPUT_GENERATOR, "Output Generators"),
]


class MainView(QtWidgets.QMainWindow):
    resource_manager = resource_manager.ImageManager()
    plugin_manager = plugin_manager.PluginManager()

    def __init__(self):
        logger.info("Initializing MainView...")
        super().__init__()  # pyright: ignore[reportUnknownMemberType]
        self.graph_controller = NodeGraph()
        self.selected_kind: NodeKind | None = NodeKind.INPUT_READER

        self.process_progress_bar = QtWidgets.QProgressBar()
        self.process_progress_bar.setFormat("%v/%m")
        self.start_time_lbl = QtWidgets.QLabel()
        self.end_time_lbl = QtWidgets.QLabel()
        self.total_time_lbl = QtWidgets.QLabel()

        self.start_button = QtWidgets.QPushButton("Start Generation")
        self.start_button.setIcon(self.resource_manager["start"])
        # self.start_button.clicked.connect(self.start_process)

        self.start_time: float | None = None
        self.end_time: float | None = None

        # Initialize main container and layout.
        self.main_container = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()

        # TODO: re-add UI content
        self.main_layout.addLayout(self.add_header_layout())
        self.main_layout.addLayout(self.add_content_layout())
        self.main_layout.addLayout(self.add_footer_layout())

        self.main_container.setLayout(self.main_layout)
        self.setWindowTitle(info.NAME)
        self.setWindowIcon(self.resource_manager["icon"])
        self.setCentralWidget(self.main_container)
        logger.info("MainInterface initialization done.")

    def add_header_layout(self) -> QtWidgets.QLayout:
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
        title.setFont(QtGui.QFont("Inter", 38))
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(icon)
        layout.addWidget(title)

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        return layout

    def add_content_layout(self) -> QtWidgets.QLayout:
        def on_category_changed(idx: int) -> None:
            self.update_nodes_list(NODE_CATEGORIES[idx][0])

        top_buttons_size = QtCore.QSize(25, 25)
        layout = QtWidgets.QHBoxLayout()

        sidebar = QtWidgets.QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QtWidgets.QVBoxLayout()

        # top buttons
        top_buttons_layout = QtWidgets.QHBoxLayout()
        top_buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        add_node_button = QtWidgets.QPushButton()
        recipes_button = QtWidgets.QPushButton()
        process_button = QtWidgets.QPushButton()
        settings_button = QtWidgets.QPushButton()
        add_node_button.setIcon(self.resource_manager["add"])
        recipes_button.setIcon(self.resource_manager["recipe"])
        process_button.setIcon(self.resource_manager["start"])
        settings_button.setIcon(self.resource_manager["settings"])
        add_node_button.setIconSize(top_buttons_size)
        recipes_button.setIconSize(top_buttons_size)
        process_button.setIconSize(top_buttons_size)
        settings_button.setIconSize(top_buttons_size)
        add_node_button.setToolTip("Add Selected Node")
        recipes_button.setToolTip("Manage Recipes")
        process_button.setToolTip("Start Process")
        settings_button.setToolTip("Settings")
        top_buttons_layout.addWidget(add_node_button)
        top_buttons_layout.addWidget(recipes_button)
        top_buttons_layout.addWidget(process_button)
        top_buttons_layout.addWidget(settings_button)

        # node selection
        node_selection_layout = QtWidgets.QVBoxLayout()
        node_category_label = QtWidgets.QLabel("Node Category")
        node_category_combo = QtWidgets.QComboBox()
        self.nodes_list = QtWidgets.QListWidget()
        node_category_combo.addItems([category for _, category in NODE_CATEGORIES])
        node_category_combo.setCurrentIndex(
            node_category_combo.findText("Input Readers")
        )
        node_category_combo.currentIndexChanged.connect(  # pyright: ignore[reportUnknownMemberType]
            on_category_changed
        )
        node_selection_layout.addWidget(node_category_label)
        node_selection_layout.addWidget(node_category_combo)
        self.nodes_list.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.update_nodes_list(NODE_CATEGORIES[node_category_combo.currentIndex()][0])

        sidebar_layout.addLayout(top_buttons_layout)
        sidebar_layout.addLayout(node_selection_layout)
        sidebar_layout.addWidget(self.nodes_list)
        sidebar.setLayout(sidebar_layout)

        layout.addWidget(sidebar)
        layout.addWidget(self.graph_controller.widget)
        return layout

    def add_footer_layout(self) -> QtWidgets.QLayout:
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.process_progress_bar)
        return layout

    def update_nodes_list(self, kind: NodeKind) -> None:
        """Update the nodes list based on the selected kind.

        Args:
            kind: The kind of node to display.
        """

        self.selected_kind = kind
        self.nodes_list.clear()
        self.nodes_list.addItems(
            [
                node.name
                for node in self.plugin_manager.get_all_plugin_metadata(kind=kind)
            ]
        )
