import argparse
import sys

import darkdetect  # pyright: ignore[reportMissingTypeStubs]
import qdarktheme  # pyright: ignore[reportMissingTypeStubs]
from loguru import logger
from PySide6.QtWidgets import QApplication

from psautomater.controllers import info
from psautomater.controllers.resource_manager import StyleManager
from psautomater.models.style import Theme
from psautomater.views import main_view


def main(theme: Theme, debug_mode: bool) -> int:
    """
    Args:
        debug_mode: Whether to enable debug mode for more detailed logging.

    Returns:
        The error code of the program.
    """

    logger.add(
        info.LOGFILE_PATH,
        format=info.LOGFILE_FORMAT,
        backtrace=True,
        level=(info.LOGGING_DEBUG_MODE if debug_mode else info.LOGGING_RELEASE_MODE),
    )
    logger.info("The program has started.")
    logger.debug("args: ({0})", ", ".join(sys.argv))

    app = QApplication(sys.argv)
    logger.debug("Minimum Window Size: {0}", info.WINDOW_SIZE["min"])
    logger.debug("Maximum Window Size: {0}", info.WINDOW_SIZE["max"])
    logger.debug(
        "User Screen Size: {0}x{1} ({2}x{3})",
        app.primaryScreen().availableGeometry().width(),
        app.primaryScreen().availableGeometry().height(),
        app.primaryScreen().size().width(),
        app.primaryScreen().size().height(),
    )

    logger.debug("Applying default style...")
    style_manager = StyleManager()
    default_style = style_manager.get_style("default")
    qdarktheme.setup_theme(
        theme.value, custom_colors=style_manager.style_to_dict(default_style)
    )

    logger.debug("Creating main view...")
    widget = main_view.MainView()
    widget.setMinimumSize(info.WINDOW_SIZE["min"][0], info.WINDOW_SIZE["min"][1])
    widget.setMaximumSize(info.WINDOW_SIZE["max"][0], info.WINDOW_SIZE["max"][1])
    widget.show()

    logger.debug("Applying default style to NodeGraphQt...")
    StyleManager.update_nodegraph_theme(widget.graph_controller, default_style, theme)

    logger.info("Running main event loop.")
    ret_code = app.exec()
    logger.info("The application exited with error code {0}.", ret_code)
    return ret_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A Photoshop Editing Automation Tool for bulk editing."
    )
    parser.add_argument(
        "--theme",
        choices=["auto", "light", "dark"],
        default="auto",
        help="Force the application to use a specific theme.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode.",
    )
    args = parser.parse_args()

    __theme = Theme.DARK if darkdetect.isDark() else Theme.LIGHT
    match args.theme:
        case "auto":
            pass

        case "light":
            __theme = Theme.LIGHT

        case "dark":
            __theme = Theme.DARK

        case _:
            pass

    __debug_mode = args.debug
    sys.exit(main(__theme, __debug_mode))
