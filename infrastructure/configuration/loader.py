import os
import typing

import yaml
from benedict import benedict

from infrastructure.configuration.configs.accounts import AccountsConfig
from infrastructure.configuration.configs.architecture import ArchConfig

CONFIGS_DIRECTORY = os.path.join(os.path.dirname(__file__), "../../config/")


def _load_yaml_as_dict(filename: str) -> typing.Optional[benedict]:
    path = os.path.join(CONFIGS_DIRECTORY, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            return benedict(yaml.safe_load(f))
    return None


def _merge_config_if_exists(config: benedict, extra_config_filename: str) -> benedict:
    extra_config = _load_yaml_as_dict(extra_config_filename)
    if extra_config:
        merged = config.clone()
        merged.merge(extra_config, overwrite=True, concat=True)
        return merged
    return config


def _load_merged_config(deployment_id: str, environment_id: typing.Optional[str] = None) -> benedict:
    common_config_filename = f"{deployment_id}/common.yaml"
    config = _load_yaml_as_dict(common_config_filename)

    if config is None:
        raise FileNotFoundError(f"Config file {common_config_filename} not found.")

    config = _merge_config_if_exists(config, f"{deployment_id}/common.local.yaml")
    if environment_id is not None:
        config = _merge_config_if_exists(config, f"{deployment_id}/{environment_id}.yaml")
        config = _merge_config_if_exists(config, f"{deployment_id}/{environment_id}.local.yaml")

    return config


def load_arch_config(deployment_id: str, environment_id: typing.Optional[str] = None) -> ArchConfig:
    config_dict = _load_merged_config(deployment_id, environment_id)
    return ArchConfig(**config_dict)


def load_accounts_config(deployment_id: str) -> AccountsConfig:
    config_filename = f"{deployment_id}/accounts.yaml"
    config = _load_yaml_as_dict(config_filename)
    if config is None:
        raise FileNotFoundError(f"Config file {config_filename} not found.")

    _merge_config_if_exists(config, f"{deployment_id}/accounts.local.yaml")

    return AccountsConfig(**config)
