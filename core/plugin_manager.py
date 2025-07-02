from plugins.plugin_base import PluginBase
import importlib.util
from pathlib import Path
from typing import Any

class PluginManager:
    """
    PluginManager: This class
                            * import/loads the user defined plugins.
                            * validates them(confirm plugin inherit from PluginBase).
                            * stores them(store all plugin instances in a list self.plugins ).
                            * Dispatches events (on_violation,on_test_generated) on them.
                    Its the bridge between core engine of TypeSafeX and the external plugins 
                    that extend behavior.
    """

    def __init__(self,config) -> None:
        """
        load_config and initialize plugins
        """
        self.plugins = self._load_plugins(config["plugins"]["paths"])

    def _load_plugins(self,paths:list)->list:
        """
        import plugins from file system
        """
        loaded = []
        for path in paths:
            plugin = self._import_plugins(path)
            if isinstance(plugin, PluginBase):
                loaded.append(plugin)
        return loaded

    def _import_plugins(self, path: str)-> PluginBase:
        """
        import plugin from a given path 
        """
        module_name = Path(path).stem
        # Create a module spec and load the module
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None:
            raise ImportError(f"Could not load plugin from {path}")
        plugin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin_module)
        plugin_class = getattr(plugin_module, 'Plugin', None)
        if plugin_class is None:
            raise ValueError(f"[PLUGIN ERROR] Plugin '{path}' must define a class named 'Plugin'.")
        plugin_instance = plugin_class()
        return plugin_instance

    def dispatch(self,hook_name:str, *args:Any)->None:
        """
        call hook method on each plugin
        """
        for plugin in self.plugins:
            #get the 
            method = getattr(plugin, hook_name, None)
            if callable(method):
                try:
                    method(*args)
                except Exception as e:
                    print(f"[PLUGIN ERROR] {plugin}: {e}")