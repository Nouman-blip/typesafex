

class ViolationJson:
    """
    if report true then format is:
        {
            "func": "function_name",
            "reason": "reason for violation",
            "args":[],
            "kwargs":{},
            "mode": "mode",
            timestamp: "timestamp",
        }
        
        save into a json file where user provide path
    """
    def __init__(self, func: str, reason: str, *args: Any, **kwargs: Any, mode: str) -> None:
        self.func = func
        self.reason = reason
        self.args = args
        self.kwargs = kwargs
        self.mode = mode
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
    def to_dict(self) -> dict:
        return {
            "func": self.func,
            "reason": self.reason,
            "args": self.args,
            "kwargs": self.kwargs,
            "mode": self.mode,
            "timestamp": self.timestamp
        }
    
    # Save the violation to a JSON file
    def save_to_file(self, file_path: str) -> None:
        import json
        with open(file_path, 'a') as f:
            json.dump(self.to_dict(), f)
            f.write('\n')
   