from abc import ABC


class PreGenerationHook(ABC):
    """Hook that is called before the generation process starts."""

    def __call__(self, *args, **kwargs) -> None: ...


class PreProcessingHook(ABC):
    """Hook that is called before the processing of each input data starts."""

    def __call__(self, *args, **kwargs) -> None: ...


class PostProcessingHook(ABC):
    """Hook that is called after the processing of each input data ends."""

    def __call__(self, *args, **kwargs) -> None: ...


class PostGenerationHook(ABC):
    """Hook that is called after the generation process ends."""

    def __call__(self, *args, **kwargs) -> None: ...
