from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import photoshop.api as ps_api  # pyright: ignore[reportMissingTypeStubs]


class EditingStrategy(Enum):
    COM = "COM"
    PSDTOOLS = "PSDTools"


@dataclass
class GenerationConfig:
    """Configuration for the PSD generation process."""

    spreadsheet_path: Path
    target_sheet: str
    template_path: Path
    output_dir: Path

    feature_auto_crop_image: bool
    feature_auto_center_image: bool
    feature_remove_background: bool

    editing_strategy: EditingStrategy


@dataclass
class PSDLayerInfo:
    """A dataclass to store information about a PSD layer."""

    name: str
    kind: ps_api.LayerKind
    visible: bool
    opacity: int
