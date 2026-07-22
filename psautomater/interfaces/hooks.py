from typing import Protocol


class PreGenerationHook(Protocol):
    """Hook that is called before the generation process starts."""

    def __call__(self, *args, **kwargs) -> None: ...


class PreProcessingHook(Protocol):
    """Hook that is called before the processing of each input data starts."""

    def __call__(self, *args, **kwargs) -> None: ...


class PostProcessingHook(Protocol):
    """Hook that is called after the processing of each input data ends."""

    def __call__(self, *args, **kwargs) -> None: ...


class PostGenerationHook(Protocol):
    """Hook that is called after the generation process ends."""

    def __call__(self, *args, **kwargs) -> None: ...
