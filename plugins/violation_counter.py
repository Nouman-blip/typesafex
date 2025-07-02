from plugins.plugin_base import PluginBase
from contracts.violations import Violation

class ViolationCounter(PluginBase):
    """
    Violation Counter to calculate how many violation
    """
    def __init__(self):
        """
        Initialize the ViolationCounter plugin.
        """
        super().__init__()
        self.counted_violation = 0

    # Override the on_violation method from PluginBase
    def on_violation(self, violation: Violation)->None:
      """
      count the number of current violations
      """ 
     # If the violation is not None, increment the counter
      if Violation:
        self.counted_violation += 1
        
      print(f"[VIOLATIONCOUNTER] 🚫 Number of violations right now = {self.counted_violation}.")

#Make it availbale dynamically loadable
Plugin=ViolationCounter