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
# from config_handler.advanced import Advanced


def main() -> int:
    """
    The main function of cmd_handler.py module.

    :returns int: The exit code of the program.
    """

    # Enable debug mode if "--debug" is in <sys.argv>.
    DEBUG_MODE = True if "--debug" in sys.argv else False

    # Initialize the logger.
    logger = Logger(
        name=info.NAME,
        logfile=info.DEFAULT_LOGFILEPATH,
        loglevel=5 if DEBUG_MODE else 3,  # 3 = INFO, 5 = DEBUG
    )

    logger.info(f"{info.TITLE} started on {time.ctime()}")
    logger.info("Checking if GUI mode is enabled...")
    # Check if the user wants to use the GUI or not.
    if "--no-gui" not in sys.argv:
        logger.info("GUI mode is enabled.")
        from . import gui  # Import and start the GUI.
        return gui.GUI(logger).main()

    else:
        logger.info("GUI mode is disabled. Continuing to run in CLI mode.")

    logger.info("Checking command-line arguments...")
    skip_next = False
    commands = {}  # Contains commands to perform.
    # Possible contents of <commands>:
    #
    # "build": type(bool)
    # "build_opts": type(dict)
    #     "template_filepath": type(str)
    #     "list_filepath": type(str)
    #     "output_path": type(str)
    #     "default_empty_value": type(str)
    #     "strict_empty": type(bool)
    #     "duplicate_default_action": type(str)
    #     "export": type(bool)
    #     "export_format": type(str)

    for i, arg in enumerate(sys.argv):
        if skip_next:
            logger.debug("Skipping current argument.")
            skip_next = False
            continue

        logger.debug(f"Argument {i}: {arg}")
        if i == 0:
            logger.debug("Ignoring first argument. (program name)")
            continue

        elif arg in ("--debug", "--no-gui"):
            logger.debug("Ignoring argument since it is already processed.")
            continue

        elif arg in ("--help", "-h"):
            logger.debug("Printing help message and returning 0.")
            print(info.HELP)
            return 0

        elif arg in ("--version", "-v"):
            logger.debug("Printing version and returning 0.")
            print()
            print(info.TITLE)
            print()
            print("Program Name:", info.NAME)
            print("Program Version:", info.VERSIONS)
            print()
            print("Logfile Path:", info.DEFAULT_LOGFILEPATH)
            print()
            print(info.COPYRIGHT)
            print()
            return 0

        elif arg == "build":
            logger.info("Build mode is enabled.")
            commands["build"] = True
            commands["build_opts"] = {}

        elif commands.get("build", False) and arg == "--template":
            logger.info("Setting template filepath.")
            # Check if there is a next argument.
            try:
                commands["build_opts"]["template_filepath"] = sys.argv[i + 1]
                logger.debug(f"Template filepath: {sys.argv[i + 1]}")
                skip_next = True

            except IndexError:
                err_msg = "`--template` called but no template filepath specified."
                logger.error(err_msg)
                print("[E]", err_msg)
                return 3

        elif commands.get("build", False) and arg == "--list":
            logger.info("Setting list filepath.")
            try:
                commands["build_opts"]["list_filepath"] = sys.argv[i + 1]
                logger.debug(f"List filepath: {sys.argv[i + 1]}")
                skip_next = True

            except IndexError:
                err_msg = "`--list` called but no list filepath specified."
                logger.error(err_msg)
                print("[E]", err_msg)
                return 4

        elif commands.get("build", False) and arg == "--output":
            logger.info("Setting output path.")
            try:
                commands["build_opts"]["output_path"] = sys.argv[i + 1]
                logger.debug(f"Output path: {sys.argv[i + 1]}")
                skip_next = True

            except IndexError:
                err_msg = "`--output` called but no output path specified."
                logger.error(err_msg)
                print("[E]", err_msg)
                return 5

        elif commands.get("build", False) and arg == "--default-empty":
            logger.info("Setting default empty value.")
            # Check if strict_empty is True.
            if commands["build_opts"].get("strict_empty", False):
                err_msg = "`--default-empty` called but `--strict-empty` is already enabled."
                logger.error(err_msg)
                print("[E]", err_msg)
                return 7

            try:
                commands["build_opts"]["default_empty_value"] = sys.argv[i + 1]
                logger.debug(f"Default empty value: {sys.argv[i + 1]}")
                skip_next = True

            except IndexError:
                err_msg = "`--default-empty` called but no default empty value specified."
                logger.error(err_msg)
                print("[E]", err_msg)
                return 6

        elif commands.get("build", False) and arg == "--strict-empty":
            logger.info("Enabling strict empty mode.")
            commands["build_opts"]["strict_empty"] = True

        elif commands.get("build", False) and arg == "--overwrite":
            logger.info("Switching to overwrite mode.")
            commands["build_opts"]["duplicate_default_action"] = "overwrite"

        elif commands.get("build", False) and arg == "--export":
            logger.info("Enabling export mode.")
            commands["build_opts"]["export"] = True
            try:
                commands["build_opts"]["export_format"] = sys.argv[i + 1]
                logger.debug(f"Export format: {sys.argv[i + 1]}")
                skip_next = True

            except IndexError:
                err_msg = "`--export` called but no export format specified."
                logger.error(err_msg)
                print("[E]", err_msg)
                return 8

        else:
            err_msg = f"Unknown argument: `{arg}`"
            logger.error(err_msg)
            print("[E]", err_msg)
            return 2

    return api.CommandParser(commands, logger=logger)()
