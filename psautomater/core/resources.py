"""
MIT License

Copyright (c) 2023 Chris1320

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
from pathlib import Path

from PySide6.QtGui import QPixmap


class ImageManager:
    """
    This class handles the lazy-loading and management of resources.
    """

    resources_path = Path("data", "resources")

    __images: dict[str, list[Path | QPixmap | None]] = {}

    def __init__(self):
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
            raise ValueError("Unknown resource name.")

        if self.__images.get(image_name, None)[1] is None:
            self.__images[image_name][1] = QPixmap(str(self.__images[image_name][0]))

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
            raise ValueError(f"{image_name} already exists in the image manager.")

        self.__images[image_name] = []
        self.__images[image_name].append(image_path if isinstance(image_path, Path) else Path(image_path))
        self.__images[image_name].append(QPixmap(str(self.__images[image_name][0])) if not load else None)
