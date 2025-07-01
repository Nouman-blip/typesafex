from pathlib import Path
import yaml
import os

# if .typesafex.yaml fails the system stil works
DEFAULT_CONFIG = {
    "mode": "strict",  # default
    "plugins": {
        "enabled": "true",
        "paths": [
            'plugins/slack_notifier.py',
            'plugins/violation_counter.py',
            'plugins/test_collector.py'
        ]
    }
}

CONFIG_PATHS= [
    "./.typesafex.yaml",
    os.path.expanduser("~/.typesafex.yaml"),
]

def load_config()->dict:
    """
    Load configuration from ./.typesafex.yaml file or fallback to default
    """
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
                return merge_dicts(DEFAULT_CONFIG,user_config)
                
    return DEFAULT_CONFIG

def merge_dicts(default: dict, override: dict) -> dict:
    """
    Recursively merge two dictionaries-useful when user override partial config
    """
    merged = default.copy()
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key]=value
    return merged

