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

import sys
import time

from . import api
from . import info

from simplelogger.logger import Logger
from config_handler.advanced import Advanced


def main() -> int:
    """
    The main function of cmd_handler.py module.

    :returns int: The exit code of the program.
    """

    logger = Logger(
        name=info.NAME,
        logfile=info.DEFAULT_LOGFILEPATH,
        loglevel=5 if "--debug" in sys.argv else 3,  # 3 = INFO, 5 = DEBUG
    )

    logger.info(f"{info.TITLE} started on {time.ctime()}")

    logger.info("Checking if GUI mode is enabled...")
    # Check if the user wants to use the GUI or not.
    if "--no-gui" not in sys.argv:
        logger.info("GUI mode is enabled.")
        # GUI mode enabled
        from . import gui
        gui.GUI(logger).main()

    else:
        logger.info("GUI mode is disabled. Continuing to run in CLI mode.")

    logger.info("Checking command-line arguments...")
    for i, arg in enumerate(sys.argv):
        logger.debug(f"Argument {i}: {arg}")
        if i == 0:
            logger.debug("Ignoring first argument. (program name)")
            continue

        elif arg in ("--debug", "--no-gui"):
            logger.debug("Ignoring argument since it is already processed.")
            continue

        elif arg in ("--help", "-h"):
            logger.debug("Printing help message and returning 0.")
            # Print help and quit.
            print(info.HELP)
            return 0

        elif arg in ("--version", "-v"):
            logger.debug("Printing version and returning 0.")
            print(info.TITLE)
            print()
            print("Program Name:", info.NAME)
            print("Program Version:", info.VERSIONS)
            print()
            print("Logfile Path:", info.DEFAULT_LOGFILEPATH)
            print()
            print(info.COPYRIGHT)
            return 0

        elif arg == "build":
            logger.info("Build mode is enabled.")

        else:
            logger.warning("Unknown argument: `{arg}`")
