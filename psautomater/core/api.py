"""
MIT License

Copyright (c) 2022 Chris1320

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

from .default_logger import Logger


class Builder:
    """
    Create new PSD files from a template and an Excel spreadsheet or CSV list.
    """

    PSD_EXTENSIONS = (".psd", ".psb")
    LIST_EXTENSIONS = (".xlsx", ".xls", ".csv")

    def __init__(self, **kwargs):
        """
        The initialization method of the Builder() class.

        :**kwargs class logger: The logger class to use.
        :**kwargs str template_filepath: The path to the template PSD file.
        :**kwargs str list_filepath: The path to the list file.
        """

        self.__logger: Logger = kwargs.get("logger", Logger())
        self._template_filepath: str = kwargs.get("template_filepath", None)
        self._list_filepath: str = kwargs.get("list_filepath", None)

    # Define properties
    @property
    def template_filepath(self):
        return self._template_filepath

    @property
    def list_filepath(self):
        return self._list_filepath

    # Define property setters
    @template_filepath.setter
    def template_filepath(self, filepath: str):
        """
        Set the PSD template filepath.

        :param str filepath: The filepath of the PSD template.
        """

        self.__logger.debug(f"Setting template filepath to `{filepath}`...")

        if os.path.isfile(filepath) and filepath.lower().endswith(self.PSD_EXTENSIONS):
            self._template_filepath = filepath

        else:
            err_msg = f"The filepath `{filepath}` does not exist or is not a PSD file."
            self.__logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    @list_filepath.setter
    def list_filepath(self, filepath: str):
        """
        Set the Excel spreadsheet or CSV list filepath.

        :param str filepath: The filepath of the Excel spreadsheet or CSV list.
        """

        self.__logger.debug(f"Setting list filepath to `{filepath}`...")

        if os.path.isfile(filepath) and filepath.lower().endswith(self.LIST_EXTENSIONS):
            self._list_filepath = filepath

        else:
            err_msg = f"The filepath `{filepath}` does not exist or is not in a supported format. (xlsx, csv)"
            self.__logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    # Define property deleters
    @template_filepath.deleter
    def template_filepath(self):
        self._template_filepath = None

    @list_filepath.deleter
    def list_filepath(self):
        self._list_filepath = None

    # Define methods
    def run(self):
        """
        Start the automation process.
        """

        # TODO
        print("Building files...")


class CommandParser:
    """
    Parse a dictionary containing commands.
    """

    def __init__(self, commands: dict, **kwargs):
        """
        The initialization method of the CommandParser() class.

        :param dict commands: The dictionary containing commands.

        :**kwargs class logger: The logger class to use.
        """

        self.__commands = commands
        self.__logger: Logger = kwargs.get("logger", Logger())

    def __call__(self) -> int:
        """
        Parse the commands.

        :returns int: The exit code.
        """

        # TODO
        print("Processing commands.")
        return 0
