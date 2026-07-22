from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    """An enum representing the available themes."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


@dataclass(frozen=True)
class Colors:
    """A dataclass holding the contents of a style's colors."""

    background: str
    border: str
    foreground: str
    primary: str


@dataclass(frozen=True)
class Style:
    """A dataclass holding the contents of a style."""

    name: str

    light: Colors
    dark: Colors
