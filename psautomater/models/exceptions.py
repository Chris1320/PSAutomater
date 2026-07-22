class PluginLoadError(Exception):
    """Raised when a plugin fails to load."""

    def __init__(self, plugin_name: str, original_exception: Exception):
        self.plugin_name = plugin_name
        self.original_exception = original_exception
        super().__init__(f"Failed to load plugin '{plugin_name}': {original_exception}")


class PluginNotFoundError(Exception):
    """Raised when a plugin is not found in the plugin manager."""

    def __init__(self, plugin_uid: str):
        self.plugin_uid = plugin_uid
        super().__init__(f"Plugin with UID '{plugin_uid}' not found.")
