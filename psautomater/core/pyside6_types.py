"""
This module is used to tell the IDE that the attributes in
the classes are of type Signal.

"The patch was applied but not cherry-picked to 6.4 - added that right now so
that the change will be visible in 6.4.3."

Source: https://bugreports.qt.io/browse/PYSIDE-1603
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal


class QPushButton(QtWidgets.QPushButton):
    clicked: Signal  # pyright: ignore[reportIncompatibleVariableOverride]
