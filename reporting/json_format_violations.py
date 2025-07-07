from typing import List, Dict, Optional, Any
from pathlib import Path
import json
class ViolationJson:
    """    
        save into a json file where user provide path
    """
   
    
    # Save the violation to a JSON file
    @staticmethod
    def save_to_file(file_path: Optional[str], violation_data:Optional[List[Dict[str,Any]]]):
        """
        violation_data=[
             {
             "func_name":func_name
             "reason":reason,
             ....
             },{
             }
        ]
        file_path: str
            The path to the JSON file where the violation data will be saved.
        """
        if violation_data is None or not isinstance(violation_data, list):
            raise ValueError("Violation data must be a non-empty list.")
        # if file path is None then use config file path
        if file_path is None:
            file_path = "violation_report.json"
        # read the file and check if it same data as previously saved since file path is str
        file_path = Path(file_path)
        # Ensure the directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # Check if the file exists and read its content
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
                # If the data is the same, do not overwrite
                if existing_data == violation_data:
                    print(f"No changes detected. Not overwriting {file_path}.")
                    return
            except (FileNotFoundError, json.JSONDecodeError):
                # If file does not exist or is empty, we can proceed to write
                pass
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(violation_data, file, indent=4, ensure_ascii=False)
            print(f"Violation data saved to {file_path}")
        except IOError as e:
            print(f"Error saving violation data to {file_path}: {e}")