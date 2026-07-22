from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Row:
    index: int
    data: dict[str, str | int | float | Path | None]
