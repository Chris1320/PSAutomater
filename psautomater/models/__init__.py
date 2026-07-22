from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class NodeKind(Enum):
    INPUT_READER = "Input Reader"
    HOOK = "Hook"
    OUTPUT_GENERATOR = "Output Generator"


class HookType(Enum):
    PRE_GENERATION = "Pre-Generation"
    PRE_PROCESS = "Pre-Process"
    POST_PROCESS = "Post-Process"
    POST_GENERATION = "Post-Generation"


@dataclass(frozen=True)
class Row:
    index: int
    data: dict[str, str | int | float | Path | None]


@dataclass
class NodeMetadata:
    uid: str
    name: str
    version: str
    kind: NodeKind
    hook_type: HookType | None = None
