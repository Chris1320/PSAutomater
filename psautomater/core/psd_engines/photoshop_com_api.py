# pylint: disable=line-too-long

from pathlib import Path

import photoshop.api as ps_api  # pyright: ignore[reportMissingTypeStubs]
from loguru import logger

from psautomater.core.models import PSDLayerInfo


class PhotoshopComAPI:
    """Control Photoshop via the COM API. This is the default engine for Windows users."""

    def __init__(self, file_path: Path):
        """
        Args:
            file_path: The path to the PSD file.
        """

        logger.debug(f"Loading PSD located in `{file_path}` using COM API.")
        self.file_path = file_path
        self.app = ps_api.Application()
        self.doc = self.app.load(  # pyright: ignore[reportUnknownMemberType]
            self.file_path
        )

    def get_layers(
        self, type_filter: ps_api.LayerKind | None = None
    ) -> list[PSDLayerInfo]:
        """Return the information of the layers in the PSD file.

        Args:
            type_filter: If provided, only return layers of the specified type.

        Returns:
            A list of `PSDLayerInfo` objects containing information about the layers in the PSD file.
        """

        layers_info: list[PSDLayerInfo] = []
        for layer in self.doc.layers:  # pyright: ignore[reportUnknownMemberType]
            if (
                type_filter and layer.kind != type_filter
            ):  # pyright: ignore[reportUnknownMemberType]
                logger.debug(
                    f"Looking for {type_filter.name} but found {ps_api.LayerKind(layer.kind)}"
                )
                continue

            logger.debug(
                f"Found layer: {layer.name} of type {ps_api.LayerKind(layer.kind)}"
            )
            # ignore galore!
            layer_info = PSDLayerInfo(
                name=layer.name,  # pyright: ignore[reportUnknownMemberType]
                kind=layer.kind,  # pyright: ignore[reportUnknownMemberType,reportArgumentType]
                visible=layer.visible,  # pyright: ignore[reportUnknownMemberType,reportArgumentType]
                opacity=layer.opacity,  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
            )
            layers_info.append(layer_info)

        return layers_info
