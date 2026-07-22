from loguru import logger
from NodeGraphQt import NodeGraph  # pyright: ignore[reportMissingTypeStubs]
from PySide6 import QtCore, QtGui, QtWidgets

from psautomater.controllers import info, resource_manager


class MainView(QtWidgets.QMainWindow):
    resource_manager = resource_manager.ImageManager()

    def __init__(self):
        logger.info("Initializing MainView...")
        super().__init__()  # pyright: ignore[reportUnknownMemberType]
        self.graph_controller = NodeGraph()

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
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.graph_controller.widget)
        return layout

    def add_footer_layout(self) -> QtWidgets.QLayout:
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.process_progress_bar)
        return layout
