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

from .default_logger import Logger

# TODO
# from pandas import 

class ListReader:
    """
    Handles reading CSV lists or Excel spreadsheets.
    """

    def __init__(self, filepath: str, **kwargs):
        """
        The initialization method of ListReader() class.

        :param str filepath: The path to the list file.
        :**kwargs class logger: The logger object to use.
        """

        self.__logger: Logger = kwargs.get("logger", Logger())

        self._filepath: str = filepath

        self._column_titles_row: int = kwargs.get("column_titles_row", 0)
        self._data_row_start: int = kwargs.get("data_row_start", self._column_titles_row + 1)
