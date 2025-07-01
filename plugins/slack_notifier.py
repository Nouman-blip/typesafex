from contracts.violations import Violation
from plugins.plugin_base import PluginBase


class SlackNotifier(PluginBase):
    """
    plugin: SlackNotifier
    Posts violation alerts to Slack when a contract fails.
    """

    def on_violation(self, violation: Violation)->None:
        """
        slack hook for contract violations.
        """
        # Simulated post(real: use request.post+webhook)
        print(f"[SlackNotifier] 🚨 Violation in {violation.reason}")

# make it dynamicaly loadable
Plugin = SlackNotifier