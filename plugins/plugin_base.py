from contracts.violations import Violation
class PluginBase:
    """
    base class interface for hookable lifecycle event
    """
    def on_violation(self, violation: Violation): pass
    def on_pass(self, function_name: str): pass
    def on_test_generated(self, test_stub: str): pass
