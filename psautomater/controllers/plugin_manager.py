import importlib
from pathlib import Path
from types import ModuleType
from typing import Final

from loguru import logger

from psautomater.models import NodeKind, NodeMetadata
from psautomater.models.exceptions import PluginNotFoundError

PLUGINS_PATH: Final[Path] = Path(__file__).parent.parent / "plugins"
# EXCLUDED_PLUGINS: Final[list[str]] = ["__init__.py", "template.py"]
EXCLUDED_PLUGINS: Final[tuple[str, ...]] = ("__init__.py",)
PLUGIN_IMPORT_ROOT: Final[str] = "psautomater.plugins"


class Node:
    def __init__(self, metadata: NodeMetadata, entrypoint: ModuleType):
        self.metadata = metadata
        self.entrypoint = entrypoint


class PluginManager:
    __plugins: dict[str, Node] = {}
    __init = False

    def __init__(self):
        if not self.__init:
            logger.info("Initializing PluginManager...")
            self.scan_plugins()
            self.__init = True

    @property
    def plugins(self) -> dict[str, Node]:
        return self.__plugins

    def scan_plugins(self):
        """Scans the plugins directory for available plugins and loads them."""

        logger.info("Scanning for plugins...")
        logger.debug(f"Plugins path: {PLUGINS_PATH}")
        logger.debug(f"Excluded plugins: {', '.join(EXCLUDED_PLUGINS)}")

        logger.debug("Scanning input reader plugins...")
        input_reader_len = 0
        for plugin_file in (PLUGINS_PATH / "input_readers").glob("*.py"):
            if plugin_file.name in EXCLUDED_PLUGINS:
                logger.debug(f"Skipping excluded plugin: {plugin_file.name}")
                continue

            import_name = f"{PLUGIN_IMPORT_ROOT}.input_readers.{plugin_file.stem}"
            try:
                module = importlib.import_module(import_name)
                logger.info(f'Added "{module.NAME}" v{module.VERSION}')
                self.__plugins[module.UID] = Node(
                    metadata=NodeMetadata(
                        uid=module.UID,
                        name=module.NAME,
                        version=module.VERSION,
                        kind=module.KIND,
                    ),
                    entrypoint=module,
                )
                input_reader_len += 1

            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(f"Failed to load plugin {import_name}: {e}")

        logger.info(f"Loaded {input_reader_len} input reader plugins.")

    def get_all_plugin_metadata(
        self, kind: NodeKind | None = None
    ) -> dict[NodeKind, list[NodeMetadata]]:
        """Get metadata for all plugins.

        Args:
            kind: The kind of plugin to get metadata for. If None, all plugins are returned.

        Returns:
            A dictionary of plugin metadata, keyed by plugin UID.
        """

        result: dict[NodeKind, list[NodeMetadata]] = {
            NodeKind.INPUT_READER: [],
            NodeKind.HOOK: [],
            NodeKind.OUTPUT_GENERATOR: [],
        }

        for plugin in self.__plugins.values():
            if kind is None or plugin.metadata.kind == kind:
                result[plugin.metadata.kind].append(plugin.metadata)

        return result

    def get_plugin(self, uid: str) -> Node:
        """Get a plugin by its UID.

        Args:
            uid: The UID of the plugin to get.

        Returns:
            The plugin with the given UID.

        Raises:
            PluginNotFoundError: If the plugin with the given UID is not found.
        """

        if uid not in self.__plugins:
            logger.error(f"Plugin with UID {uid} not found.")
            raise PluginNotFoundError(uid)

        return self.__plugins[uid]
