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

from sys import argv

from . import info


def help(print_info: bool = True) -> str:
    """
    Print or return the help menu.
    """

    help_menu = f"""
{info.TITLE}

USAGE:
    {argv[0]} [SWITCHES] [COMMANDS] [OPTIONS]

AVAILABLE SWITCHES:
    -h, --help                          Print the help menu and quit.
    -v, --version                       Print the version of the program and quit.

    --no-gui                            *Do not use the GUI.
    --debug                             Capture debug information to log file.

AVAILABLE COMMANDS & OPTIONS:
    build                               Create new files using a PSD template and a list.
        --template <filepath>           The PSD template to use.
        --list <filepath>               The Excel spreadsheet or CSV list to read details from.
        --output <folder name>          The path of the new folder to create new files in.

        --default-empty <string>        If a cell is empty, use this string instead.
        --strict-empty                  If a cell is empty, throw an error.

        --overwrite                     If enabled, overwrite existing files instead of skipping.
        --export <format>               Export the newly-created files to a specified format.

*If GUI is enabled, other options will be ignored.
"""

    if print_info:
        print(help_menu)

    return help_menu
