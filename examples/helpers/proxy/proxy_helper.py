import os
from pathlib import Path
from typing import Dict

from helpers.common.yaml_helper import read_config_yaml


def set_proxy(proxy: str) -> None:
    """
    Sets the company's proxy to the OS environment variables.

    Args:
        proxy: company's proxy URL
    """
    os.environ["HTTP_PROXY"] = proxy
    os.environ["HTTPS_PROXY"] = proxy


def set_default_proxy() -> None:
    """
    Sets the company's proxy to the OS environment variables using the settings
    in the `.config.yaml` file that is located in the directory of this module.
    """
    dir_path: Path = Path(__file__).resolve().parent
    config: Dict = read_config_yaml(dir_path)

    proxy_dict: Dict = config.get("proxies", {})
    proxy: str = proxy_dict.get("proxy_1", "") or proxy_dict.get("proxy_2", "")
    set_proxy(proxy)
