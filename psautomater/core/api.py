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
from .list_reader import ListReader


class Builder:
    """
    Create new PSD files from a template and an Excel spreadsheet or CSV list.
    """

    DUPLICATE_DEFAULT_ACTION = "skip"

    PSD_EXTENSIONS = ("psd", "psb")
    LIST_EXTENSIONS = ("xlsx", "xls", "csv")
    DUPLICATE_ACTIONS = ("skip", "overwrite")

    def __init__(self, **kwargs):
        """
        The initialization method of the Builder() class.

        :**kwargs class logger: The logger class to use.
        :**kwargs str template_filepath: The path to the template PSD file.
        :**kwargs str list_filepath: The path to the list file.
        :**kwargs str output_path: The path to the output directory.
        :**kwargs str default_empty_value: The default value to use if the cell is empty.
        :**kwargs bool strict_empty: Whether to throw an error if a cell is empty. Overrides `default_empty_value`.
        :**kwargs int column_titles_row: The row number (starting index 0) where the column titles are located in the list. (Default: 0)
        :**kwargs int data_row_start: The row number (starting index 0) where the details start in the list. (Default: <column_titles_row> + 1)
        """

        self.__logger: Logger = kwargs.get("logger", Logger())

        self._template_filepath: str = self._validateTemplateFilepath(kwargs.get("template_filepath", None))
        self._list_filepath: str = self._validateListFilepath(kwargs.get("list_filepath", None))
        self._output_path: str = self._validateOutputPath(kwargs.get("output_path", None))
        self._duplicate_default_action: str = self._validateDuplicateDefaultAction(kwargs.get("duplicate_default_action", self.DUPLICATE_DEFAULT_ACTION))

        self.default_empty_value: str = kwargs.get("default_empty_value", "")
        self.strict_empty: bool = kwargs.get("strict_empty", False)
        self.column_titles_row: int = kwargs.get("column_titles_row", 0)
        self.data_row_start: int = kwargs.get("data_row_start", self.column_titles_row + 1)
        self.export: bool = kwargs.get("export", False)

        if self.export:  # Only set export format if export is True.
            self.export_format: str = kwargs["export_format"]  # Raise an error when export_format does not exist.

        self.__logger.info(f"{self.__class__.__name__} initialized.")

    # Define private methods
    def _validateTemplateFilepath(self, filepath: str) -> bool:
        """
        Check if <filepath> is a valid template filepath or is None. (This method does not check if it exists)

        :param str filepath: The string to check if valid.

        :returns bool: Return True if it is a valid template filepath.
        """

        return True if filepath[::-1].partition('.')[0][::-1].lower() in self.PSD_EXTENSIONS or filepath is None else False

    def _validateListFilepath(self, filepath: str) -> bool:
        """
        Check if <filepath> is a valid list filepath or is None. (This method does not check if it exists)

        :param str filepath: The string to check if valid.

        :returns bool: Return True if it is a valid list filepath.
        """

        return True if filepath[::-1].partition('.')[0][::-1].lower() in self.LIST_EXTENSIONS or filepath is None else False

    def _validateOutputPath(self, path: str) -> bool:
        """
        Check whether <path> is an existing directory, does not exist, or is None.

        :param str path: The string to check if valid.

        :returns bool: Return True if it is a valid output path.
        """

        return True if os.path.isdir(path) or not os.path.exists(path) or path is None else False

    def _validateDuplicateDefaultAction(self, mode: str) -> bool:
        """
        Check if <mode> is a valid default action whenever there is a duplicate file to be created.

        :param str mode: The string to check if valid.

        :returns bool: Return True if it is a valid mode.
        """

        return True if mode in self.DUPLICATE_ACTIONS else False

    # Define properties
    @property
    def template_filepath(self):
        return self._template_filepath

    @property
    def list_filepath(self):
        return self._list_filepath

    @property
    def output_path(self):
        return self._output_filepath

    @property
    def duplicate_default_action(self):
        return self._duplicate_default_action

    @property
    def export_output_path(self):
        return os.path.join(self.output_path, "Exports") if self.export else None

    # Define property setters
    @template_filepath.setter
    def template_filepath(self, filepath: str):
        """
        Set the PSD template filepath.

        :param str filepath: The filepath of the PSD template.
        """

        self.__logger.debug(f"Setting template filepath to `{filepath}`...")

        if os.path.isfile(filepath):
            if self._validateTemplateFilepath(filepath):
                self._template_filepath = os.path.abspath(filepath)

            else:
                err_msg = f"The template file format `{filepath[::-1].partition('.')[0][::-1]}` is not supported."
                self.__logger.error(err_msg)
                raise NotImplementedError(err_msg)

        else:
            err_msg = f"The filepath `{filepath}` does not exist."
            self.__logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    @list_filepath.setter
    def list_filepath(self, filepath: str):
        """
        Set the Excel spreadsheet or CSV list filepath.

        :param str filepath: The filepath of the Excel spreadsheet or CSV list.
        """

        self.__logger.debug(f"Setting list filepath to `{filepath}`...")

        if os.path.isfile(filepath):
            if self._validateListFilepath(filepath):
                self._list_filepath = os.path.abspath(filepath)

            else:
                err_msg = f"The list file format `{filepath[::-1].partition('.')[0][::-1]}` is not supported."
                self.__logger.error(err_msg)
                raise NotImplementedError(err_msg)

        else:
            err_msg = f"The filepath `{filepath}` does not exist."
            self.__logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    @output_path.setter
    def output_path(self, filepath: str):
        """
        Set the output path.

        :param str filepath: The filepath of the output path.
        """

        self.__logger.debug(f"Setting output path to `{filepath}`...")

        if self._validateOutputPath(filepath):
            self._output_path = os.path.abspath(filepath)

        else:
            err_msg = f"The output path `{filepath}` is not valid."
            self.__logger.error(err_msg)
            raise ValueError(err_msg)

    @duplicate_default_action.setter
    def duplicate_default_action(self, mode: str):
        """
        Set the default action if a filename already exists.

        :param str mode: Duplicate action mode. (See self.DUPLICATE_ACTIONS)
        """

        self.__logger.debug(f"Setting duplicate default action to `{mode}`...")

        if self._validateDuplicateDefaultAction(mode):
            self._duplicate_default_action = mode

        else:
            err_msg = f"The duplicate default action `{mode}` is not valid."
            self.__logger.error(err_msg)
            raise ValueError(err_msg)

    # Define property deleters
    @template_filepath.deleter
    def template_filepath(self):
        self._template_filepath = None

    @list_filepath.deleter
    def list_filepath(self):
        self._list_filepath = None

    @output_path.deleter
    def output_path(self):
        self._output_path = None

    @duplicate_default_action.deleter
    def duplicate_default_action(self):
        self._duplicate_default_action = None

    # Define public methods
    def run(self):
        """
        Start the automation process.
        """

        # TODO
        self.__logger.info("Starting automation process...")

        self.__logger.debug("Checking if the value of `default_empty_value` is correct...")
        if not self.strict_empty and type(self.default_empty_value) is not str:
            self.__logger.warning("The value of `default_empty_value` is not a string. Setting it to default...")
            self.__logger.debug(f"`default_empty_value`: `{self.default_empty_value}`")
            self.default_empty_value = ''

        self.__logger.info("Checking if output folder exists...")
        if self._output_path is None:  # Check if output path is set.
            err_msg = "The output path is not set."
            self.__logger.error(err_msg)
            raise ValueError(err_msg)

        if not os.path.isdir(self._output_path):
            self.__logger.info("Output folder does not exist. Creating it now...")
            os.makedirs(self._output_path)

        if self.export:
            self.__logger.info("Checking if export folder exists...")
            if not os.path.isdir(self.export_output_path):
                self.__logger.info("Export folder does not exist. Creating it now...")
                os.makedirs(self.export_output_path)

        # TODO
        # spreadsheet = 


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

        # Check if `build` command is called.
        if self.__commands.get("build", False):
            self.__logger.info("Entering build mode...")
            newBuilder: Builder = Builder(logger=self.__logger)

        return 0
