from abc import ABC


class OutputGenerator(ABC):
    """A plugin protocol for generating output files."""

    def __call__(self, *args, **kwargs) -> None: ...
