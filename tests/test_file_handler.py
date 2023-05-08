from unittest import mock

import pytest

from src.kubeconfig_switcher import file_handler
from src.kubeconfig_switcher.data_models import KubeConfig


def test_get_stored_kube_configs():
    with mock.patch("src.kubeconfig_switcher.file_handler.os.listdir", return_value=["config", "config2", "thing"]):
        with mock.patch("builtins.open", mock.mock_open(read_data="config_data")):
            ret_val = file_handler.get_stored_kube_configs()

            assert len(ret_val) == 1
            assert ret_val[0].name == "config2"
            assert ret_val[0].file_contents == "config_data"

        with mock.patch("builtins.open", mock.mock_open()) as mocked_open:
            mocked_open.side_effect = IOError()
            with pytest.raises(file_handler.FileHandlerReadingException):
                file_handler.get_stored_kube_configs()


def test_set_kube_config():
    test_kc = KubeConfig(name="test_name", file_contents="test_data")

    with mock.patch("builtins.open", mock.mock_open()) as mocked_open:
        file_handler.set_kube_config(test_kc)
        mocked_open.assert_called_once()

        mocked_open.side_effect = IOError()
        with pytest.raises(file_handler.FileHandlerWritingException):
            file_handler.set_kube_config(test_kc)
