import os
from pathlib import Path

from data_models import KubeConfig

DEFAULT_KUBE_DIR = Path.home() / ".kube"
KUBE_CONFIG_FILE_NAME = "config"

NO_READ_FILES = [KUBE_CONFIG_FILE_NAME, "cache"]


class FileHandlerException(Exception):
    pass


class FileHandlerReadingException(FileHandlerException):
    pass


class FileHandlerFindingException(FileHandlerException):
    pass


class FileHandlerWritingException(FileHandlerException):
    pass


def get_stored_kube_configs(
    dir_path: Path = DEFAULT_KUBE_DIR, must_include_keyword: str = "config"
) -> list[KubeConfig]:
    """
    Gets kubeconfigs within directory containing the keyword and excluding the main config file

    Args:
        dir_path (Path, optional): Path to kube config directory. Defaults to DEFAULT_KUBE_DIR.
        must_include_keyword (str, optional): Required keyword in file name. Nullable. Defaults to "config".

    Raises:
        FileHandlerReadingException: Cannot access a kube config file that was found

    Returns:
        list[KubeConfig]: All saved kube config files
    """
    list_of_files = os.listdir(dir_path)
    # print(list_of_files)

    # remove extra files in dir from list
    list_of_kube_configs = []
    for file_name in list_of_files:  # config not here somehow
        has_keyword = must_include_keyword is not None and must_include_keyword in file_name
        if file_name not in NO_READ_FILES and has_keyword:
            try:
                with open(dir_path / file_name, "r", encoding="utf8") as kube_config_file:
                    config_data = kube_config_file.read()
                    tmp_kc = KubeConfig(name=file_name, file_contents=config_data)
                    list_of_kube_configs.append(tmp_kc)
            except Exception as kube_e:
                raise FileHandlerReadingException("Failed to read kube config file!", kube_e)

    return list_of_kube_configs


def set_kube_config(kube_config: KubeConfig, dir_path: Path = DEFAULT_KUBE_DIR):
    """
    Set the main kube config file with the data from the parameter

    Args:
        kube_config (KubeConfig): The config to set
        dir_path (Path, optional): Path to kube config directory. Defaults to DEFAULT_KUBE_DIR.

    Raises:
        FileHandlerWritingException: Cannot write to the main kube config file
    """
    try:
        with open(dir_path / KUBE_CONFIG_FILE_NAME, "w", encoding="utf8") as main_kube_config_file:
            main_kube_config_file.write(kube_config.file_contents)
    except Exception as kube_e:
        raise FileHandlerWritingException("Failed to write kube config file!", kube_e)

def get_kube_config_by_name(kube_config_name: str) -> KubeConfig | None:
    """
    Gets the machine KubeConfig

    Args:
        kube_config_name (str): A KubeConfig name

    Returns:
        KubeConfig | None: The matching KubeConfig
    """
    for kube_config in get_stored_kube_configs():
        if kube_config_name == kube_config.name:
            return kube_config
    
    return None
