"""
config_parser.py

Module for loading and saving configuration files.
Supports JSON and YAML formats (if PyYAML is installed).
This module allows dynamic loading of configuration settings
that can override the default values defined in settings.py.
"""

import json
import os
from typing import Any, Dict

# Attempt to import PyYAML. If not available, flag accordingly.
try:
    import yaml
    YAML_AVAILABLE: bool = True
except ImportError:
    YAML_AVAILABLE: bool = False


def load_config(file_path: str) -> Dict[str, Any]:
    """
    Loads a configuration file in JSON or YAML format.

    :param file_path: The path to the configuration file.
    :return: A dictionary containing the configuration settings.
    :raises FileNotFoundError: If the file does not exist.
    :raises ValueError: If the file format is not supported or parsing fails.
    :raises ImportError: If YAML is required but not installed.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".json":
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                config: Dict[str, Any] = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON: {e}") from e

    elif ext in (".yaml", ".yml"):
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is not installed. Install it with 'pip install pyyaml' to load YAML files.")
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML: {e}") from e
    else:
        raise ValueError("Unsupported file format. Please use a .json or .yaml/.yml file.")
    return config


def save_config(config: Dict[str, Any], file_path: str) -> None:
    """
    Saves the configuration dictionary to a file in JSON or YAML format.

    :param config: The configuration dictionary to save.
    :param file_path: The path where the configuration should be saved.
    :raises ValueError: If the file format is not supported.
    :raises ImportError: If saving YAML is requested and PyYAML is not installed.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".json":
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    elif ext in (".yaml", ".yml"):
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is not installed. Install it with 'pip install pyyaml' to save YAML files.")
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config, f, default_flow_style=False, allow_unicode=True)
    else:
        raise ValueError("Unsupported file format. Please use a .json or .yaml/.yml file.")


if __name__ == "__main__":
    # Example usage: load a configuration file
    example_path = os.path.join("config", "config_example.json")
    try:
        config_data = load_config(example_path)
        print("Configuration loaded successfully:")
        print(config_data)
    except Exception as error:
        print(f"Error loading configuration file: {error}")
