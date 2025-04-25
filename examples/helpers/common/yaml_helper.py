"""
This module offers functions to work with config YAML files.
"""
from pathlib import Path
from typing import Dict

import yaml


def read_config_yaml(
    dir_path: Path,
    filename: str = ".config.yaml",
) -> Dict:
    """
    Reads settings from a config YAML file to dictionary.

    Args:
        dir_path:
            directory with a config YAML file;
            pass `Path(__file__).resolve().parent` to function
        filename:
            config filename

    Returns:
        config dictionary
    """
    config_file_path: Path = dir_path / filename

    if not config_file_path.is_file():
        raise FileNotFoundError(f"Config file not found: `{config_file_path}`.")

    with open(config_file_path, "r") as f:
        config: Dict = yaml.safe_load(f)

    return config
