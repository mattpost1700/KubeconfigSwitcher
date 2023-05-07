import os
from pathlib import Path

from .data_models import KubeConfig

DEFAULT_KUBE_DIR = Path.home() / ".kube"
KUBE_CONFIG_FILE_NAME = "config"

NO_READ_FILES = [KUBE_CONFIG_FILE_NAME, "cache"]


def get_stored_kube_configs(path: Path = DEFAULT_KUBE_DIR, must_include_keyword: str = "config") -> list[KubeConfig]:
    """
    Gets kubeconfigs within directory containing the keyword and excluding the main config file

    Args:
        path (Path, optional): Path to kube config directory. Defaults to DEFAULT_KUBE_DIR.
        must_include_keyword (str, optional): Required keyword in file name. Nullable. Defaults to "config".

    Returns:
        list[KubeConfig]: _description_
    """
    list_of_files = os.listdir(path)
    print(list_of_files)

    # remove extra files in dir from list
    list_of_config_files = []
    for file in list_of_files:  # config not here somehow
        has_keyword = must_include_keyword is not None and must_include_keyword in file
        if file not in NO_READ_FILES and has_keyword:
            list_of_config_files.append(file)

    print(list_of_config_files)
