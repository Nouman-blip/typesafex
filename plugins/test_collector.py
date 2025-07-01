from plugins.plugin_base import PluginBase

class TestCollector(PluginBase):
    """
    collect test stub generated to a file
    """
    def on_test_generated(self, test_stub: str) -> None:
        """
        generated test stub collect into a file 
        Args:
           function_name
        """
        print(f"[TESTCOLLECTOR] 💾 below are suggested test_stub: {test_stub}")


# make it dynamically loadable
Plugin=TestCollector