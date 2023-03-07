from pathlib import Path
from typing import Any

from custom_conf.config import BaseConfig

from p2g_eval.config.feed_property import FeedProperty


class P2GConfig(BaseConfig):
    @property
    def config_dir(self) -> Path:
        return Path(".")

    @property
    def default_config_path(self) -> Path:
        return self.config_dir.joinpath("default_config.yaml")

    def _initialize_config_properties(self) -> None:
        self.ground_truth = FeedProperty("ground_truth")
        self.eval_feed = FeedProperty("eval_feed")
        super()._initialize_config_properties()

    def load_args_dict(self, values: dict[str: Any]) -> None:
        for key, value in values.items():
            setattr(self, key, value)


C = P2GConfig()
