from typesafex.core.engine import Engine
from typesafex.core.plugin_manager import PluginManager

class TestEngine:
    """
    main core engine part of the integeration tests
    """
    def setup_method(self):
        """
        setup the engine
        """
        self.engine = Engine()
        self.plugin_manager = PluginManager()

    def test_plugin_manager_initialization(self):
        """
        Test lazy initialization of plugin manager
        """
        assert self.engine.plugin_manager is not None
        assert isinstance(self.engine.plugin_manager, PluginManager)

    def test_handle_type_violations(self):
        """
        Test handling of type violations
        """
        metadata = {
            'func_name': 'test_function',
            'args': [1, 'test'],
            'return_value': 2
        }
        args_violations = ['arg1: expected int, got str']
        return_violations = 'expected int, got str'

        self.engine.handle_type_violations(metadata, args_violations, return_violations)

    def test_handle_violation(self):
        """
        Test handling of violations in different modes
        """
        self.engine._mode = 'strict'
        violations = [{'arg':'arg1', 'expected':'int', 'got':'str'}]
        func_name = 'test_function'
        self.engine.handle_violations(func_name,violations)
        



