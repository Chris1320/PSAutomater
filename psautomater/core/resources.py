import os
from pathlib import Path

from loguru import logger
from PySide6.QtGui import QPixmap


class ImageManager:
    """This class handles the lazy-loading and management of resources."""

    resources_path = Path("data", "resources")

    __init: bool = False
    __images: dict[str, list[Path | QPixmap | None]] = {}

    def __init__(self):
        if not self.__init:
            logger.debug(
                "ImageManager has not been initialized. Checking for resources."
            )
            for resource in os.listdir(
                os.path.join(os.getcwd(), "data", "resources", "icons")
            ):
                # Link all images in the `data/resources/icons` directory.
                if resource.endswith(".png"):
                    self.add_image(
                        resource[::-1].partition(".")[2][::-1],
                        Path(os.getcwd(), "data", "resources", "icons", resource),
                    )

    def __getitem__(self, image_name: str) -> QPixmap:
        """Get an image.

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
