import json
import os
from pathlib import Path
from typing import Final

from loguru import logger
from NodeGraphQt import NodeGraph  # pyright: ignore[reportMissingTypeStubs]
from PySide6.QtGui import QPixmap

from psautomater.controllers import info
from psautomater.models.style import Colors, Style, Theme

HEX_CHARS: Final[str] = "0123456789abcdefABCDEF"
RESOURCES_PATH: Final[Path] = Path(os.getcwd(), "data", "resources")


class ImageManager:
    """This class handles the lazy-loading and management of resources."""

    __init: bool = False
    __images: dict[str, list[Path | QPixmap | None]] = {}

    def __init__(self):
        """Initialize the ImageManager and store all icon paths into memory."""

        if not self.__init:
            logger.debug(
                "ImageManager has not been initialized. Checking for resources."
            )
            for resource in (RESOURCES_PATH / "icons").glob("*.png"):
                # Link all images in the `data/resources/icons` directory.
                self.add_image(
                    resource.stem,
                    RESOURCES_PATH / "icons" / resource,
                )

    def __getitem__(self, image_name: str) -> QPixmap:
        """Get an image from the image list. If the image has not been loaded yet,
        it will be loaded to memory.

        Args:
            image_name: The image to get.

        Returns:
            The QPixmap data if it exists.
        """

        if image_name not in self.__images:
            logger.exception("Unknown resource name.")
            raise ValueError("Unknown resource name.")

        pixmap = self.__images[image_name][1]
        if pixmap is None:
            logger.debug(
                "The image {0} has not been loaded yet. Loading it to memory now.",
                image_name,
            )
            pixmap = QPixmap(str(self.__images[image_name][0]))
            self.__images[image_name][1] = pixmap

        if not isinstance(pixmap, QPixmap):
            raise TypeError("Cached resource is not a QPixmap.")

        logger.debug("Returning {0} QPixmap object.", image_name)
        return pixmap

    def add_image(
        self,
        image_name: str,
        image_path: str | Path,
        overwrite: bool = False,
        load: bool = False,
    ) -> None:
        """Add a new image in the image manager.

        Args:
            image_name: The given name to the image.
            image_path: The filepath of the image.
            overwrite: If True, overwrite the contents of the `image_name` key if it exists.
            load: If True, load the image to memory.
        """

        if image_name in self.__images and not overwrite:
            logger.exception("{0} already exists in the image manager.", image_name)
            raise ValueError(f"{image_name} already exists in the image manager.")

        logger.debug("Adding image {0} to ImageManager.", image_name)
        self.__images[image_name] = []
        self.__images[image_name].append(
            image_path if isinstance(image_path, Path) else Path(image_path)
        )
        self.__images[image_name].append(
            QPixmap(str(self.__images[image_name][0])) if load else None
        )


class StyleManager:
    """This class handles the management of styles and themes."""

    __init: bool = False
    __styles: list[str] = []

    def __init__(self):
        if not self.__init:
            logger.debug("StyleManager has not been initialized. Checking for styles.")
            self.reload()
            self.__init = True

    def reload(self) -> None:
        """Reload the available styles list."""

        self.__styles: list[str] = []

        for style in (RESOURCES_PATH / "styles").glob("*.json"):
            if style.stem in self.__styles:
                logger.warning(
                    "Style {0} already exists in the style manager. Overwriting.",
                    style.stem,
                )

            self.__styles.append(style.stem)
            logger.debug(f"Added '{style.stem}' to available styles.")

        logger.debug("Found {0} styles in the style manager.", len(self.__styles))

    @staticmethod
    def hex_to_rgb(hex_value: str) -> tuple[int, ...]:
        """Convert a hex string to an RGB tuple.

        Args:
            hex_value: The hex string (`#RRGGBB`) to convert.

        Returns:
            A tuple of three integers representing the RGB values.
        """

        if hex_value.startswith("#"):
            hex_value = hex_value[1:]

        if len(hex_value) != 6 or not all(c in HEX_CHARS for c in hex_value):
            raise ValueError("Invalid hex string.")

        return tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def update_nodegraph_theme(graph: NodeGraph, style: Style, theme: Theme) -> None:
        """Manually overrides the NodeGraphQt canvas and nodes to match the active theme.

        Args:
            graph: The NodeGraphQt graph to sync.
            style: The Style object to use for the theme.
            theme: The Theme to apply to the graph.
        """

        bg_color = StyleManager.hex_to_rgb(
            style.light.background if theme == Theme.LIGHT else style.dark.background
        )
        grid_color = StyleManager.hex_to_rgb(
            style.light.border if theme == Theme.LIGHT else style.dark.border
        )
        node_color = StyleManager.hex_to_rgb(
            style.light.foreground if theme == Theme.LIGHT else style.dark.foreground
        )
        text_color = StyleManager.hex_to_rgb(
            style.light.primary if theme == Theme.LIGHT else style.dark.primary
        )

        # Repaint the Background Canvas
        graph.set_background_color(  # pyright: ignore[reportUnknownMemberType]
            *bg_color
        )
        graph.set_grid_color(*grid_color)  # pyright: ignore[reportUnknownMemberType]

        # Repaint any nodes that are currently on the screen
        for node in graph.all_nodes():  # pyright: ignore[reportUnknownVariableType]
            node.set_color(*node_color)  # pyright: ignore[reportUnknownMemberType]
            node.set_text_color(*text_color)  # pyright: ignore[reportUnknownMemberType]

    @staticmethod
    def style_to_dict(style: Style) -> dict[str, str | dict[str, str]]:
        """Convert a Style object to a dictionary. This is used by qdarktheme
        to apply the style to the application.

        Args:
            style: The Style object to convert.

        Returns:
            A dictionary version of the style.
        """

        return {
            "[light]": {
                "background": style.light.background,
                "border": style.light.border,
                "foreground": style.light.foreground,
                "primary": style.light.primary,
            },
            "[dark]": {
                "background": style.dark.background,
                "border": style.dark.border,
                "foreground": style.dark.foreground,
                "primary": style.dark.primary,
            },
        }

    def get_available_styles(self) -> list[str]:
        """Get a list of available styles.

        Returns:
            A list of available styles.
        """

        return list(self.__styles)

    def get_style(self, style_name: str) -> Style:
        """Get a style from the available styles.

        Args:
            style_name: The name of the style to get.

        Returns:
            The contents of the style file.
        """

        if style_name not in self.__styles:
            logger.exception("Unknown style name.")
            raise ValueError("Unknown style name.")

        with open(
            RESOURCES_PATH / "styles" / f"{style_name}.json",
            "r",
            encoding=info.DEFAULT_ENCODING,
        ) as f:
            style = json.load(f)

        return Style(
            name=style_name,
            light=Colors(
                background=style["light"]["background"],
                border=style["light"]["border"],
                foreground=style["light"]["foreground"],
                primary=style["light"]["primary"],
            ),
            dark=Colors(
                background=style["dark"]["background"],
                border=style["dark"]["border"],
                foreground=style["dark"]["foreground"],
                primary=style["dark"]["primary"],
            ),
        )
