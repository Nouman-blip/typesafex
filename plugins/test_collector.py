from plugins.plugin_base import PluginBase
from config.loader import load_config
from pathlib import Path

CONFIG=load_config()
class TestCollector(PluginBase):
    """
    collect test stub generated to a file
    """
    def __init__(self):
        super().__init__()
        # load the config of test_generated from .typesafex.yaml
        self.test_stub_config = CONFIG["test_generation"]["export_stub_path"] 

    def on_test_generated(self,func_name:str, location:str , test_stub: str)-> None:
        """
        generated test stub collect into a .py file 
        Args:
            test_stub (str): The generated test stub code.
        """
        # write the test stub to a file
        if not test_stub:
            raise ValueError("test_stub is empty!")
        # create file name 
        folder_path = Path(self.test_stub_config)
        test_file_name = f"test_{func_name}_{location}.py"
        full_file_path = folder_path / test_file_name
        # create folder if it not exist already


        try:
            full_file_path.mkdir(parents=True,exist_ok=True)
        except (OSError, PermissionError) as e:
            print(f"[TEST-SUGGESTION] Error creating directory {folder_path}: {e}")
            return
        # if file not exist it will create new 
        # and if it already exist it will just update and append new content without overwritng
        try:

            if full_file_path.exists():
                content = full_file_path.read_text(encoding='utf-8')
                # if all the content of test_stub in content do not write to file
                if test_stub in content:
                return
        except (FileNotFoundError, IOError) as e:
            print(f"[TEST-SUGGESTION] Error reading file {full_file_path}: {e}")
            content=""

        # write the test stub to a file
        try:
            with full_file_path.open('a',encoding='utf-8') as f:
                    f.write(test_stub)
        except (FileNotFoundError, IOError) as e:
            print(f"[TEST-SUGGESTION] Error writing to file {full_file_path}: {e}")
            return
        print(f"[TEST-SUGGESTION] saved to a file path {full_file_path}")

        
# make it dynamically loadable
Plugin=TestCollector