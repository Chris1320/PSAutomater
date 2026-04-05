from dataclasses import dataclass
from enum import Enum
from pathlib import Path


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
