from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class EditingStrategy(Enum):
    COM = "COM"
    PSDTOOLS = "PSDTools"


@dataclass
class InputData:
    """A dataclass holding the contents of the input data."""

    filepath: Path
    headers: list[str]
    # 2D list of values from the input file.
    # The inner lists represent individual rows.
    values: list[list[str | int | float | Path]]
