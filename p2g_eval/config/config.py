from pathlib import Path

from custom_conf.custom_conf.config import BaseConfig


class P2GConfig(BaseConfig):
    @property
    def config_dir(self) -> Path:
        return Path(".")

    @property
    def default_config_path(self) -> Path:
        return self.config_dir.joinpath("default_config.yaml")

    def _initialize_config_properties(self) -> None:
        
        super()._initialize_config_properties()
