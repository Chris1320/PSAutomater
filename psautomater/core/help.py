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

from . import info


def help(print_info: bool = True) -> str:
    """
    Print this help menu.

    :param bool print_info: If True, print the help menu. Otherwise, just return the help menu.

    :returns str:
    """

    help_menu = f"""
{info.TITLE}

USAGE: {info.program_callsign} [OPTIONS]

AVAILABLE OPTIONS:
--list <filepath>             Manually set the list filepath.
--template <filepath>         Manually set the PSD template filepath. (Default: `template.psd`)
--overwrite                   Overwrite files instead of skipping it. (Useful when you updated something in the template)
--output-folder <filepath>    Set the custom output directory name
--default-empty <string>      Set the default value for keys that do not have one.
--no-export                   Do not export PSD files.
--interactive                 Run in interactive mode.
"""

    if print_info:
        print(help_menu)

    return help_menu
