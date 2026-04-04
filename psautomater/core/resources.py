import os
from pathlib import Path

from loguru import logger
from PySide6.QtGui import QPixmap


class ImageManager:
    """
    This class handles the lazy-loading and management of resources.
    """

    resources_path = Path("data", "resources")

    __init: bool = False
    __images: dict[str, list[Path | QPixmap | None]] = {}

    def __init__(self):
        if not self.__init:
            logger.debug("ImageManager has not been initialized. Checking for resources.")
            for resource in os.listdir(os.path.join(os.getcwd(), "data", "resources", "icons")):
                # Link all images in the `data/resources/icons` directory.
                if resource.endswith(".png"):
                    self.addImage(
                        resource[::-1].partition('.')[2][::-1],
                        Path(os.getcwd(), "data", "resources", "icons", resource)
                    )

    def __getitem__(self, image_name: str) -> QPixmap:
        """
        Get an image.

        :param image_name: The image to get.

        :returns: The QPixmap data if it exists.
        """

        if image_name not in self.__images:
            logger.exception("Unknown resource name.")
            raise ValueError("Unknown resource name.")

        if self.__images.get(image_name, None)[1] is None:
            logger.debug("The image {0} has not been loaded yet. Loading it to memory now.", image_name)
            self.__images[image_name][1] = QPixmap(str(self.__images[image_name][0]))

        logger.debug("Returning {0} QPixmap object.", image_name)
        return self.__images[image_name][1]

    def addImage(self, image_name: str, image_path: str | Path, overwrite: bool = False, load: bool = False) -> None:
        """
        Add a new image in the image manager.

        :param image_name: The given name to the image.
        :param image_path: The filepath of the image.
        :param overwrite: If True, overwrite the contents of the `image_name` key if it exists.
        :param load: If True, load the image to memory.

        :returns:
        """

        if image_name in self.__images and not overwrite:
            logger.exception("{0} already exists in the image manager.", image_name)
            raise ValueError(f"{image_name} already exists in the image manager.")

        logger.debug("Adding image {0} to ImageManager.", image_name)
        self.__images[image_name] = []
        self.__images[image_name].append(image_path if isinstance(image_path, Path) else Path(image_path))
        self.__images[image_name].append(QPixmap(str(self.__images[image_name][0])) if load else None)
