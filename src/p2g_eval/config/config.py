""" Contains the Config to be used by p2g-eval. """

from pathlib import Path
from typing import Any

from custom_conf.config import BaseConfig

from p2g_eval.config.properties import FeedProperty, MappingProperty


class P2GConfig(BaseConfig):
    """ The config. Provides the ground-truth and test feeds, as well as
    the different user-provided mappings. """
    @property
    def src_dir(self) -> Path:
        """ The source directory of p2g-eval, that contains the 'main.py'. """
        return Path(__file__).parents[1].resolve()

    @property
    def config_dir(self) -> Path:
        return self.src_dir

    @property
    def default_config_path(self) -> Path:
        return self.config_dir.joinpath("default_config.yaml")

    def _initialize_config_properties(self) -> None:
        self.true_feed = FeedProperty("true_feed")
        self.test_feed = FeedProperty("test_feed")
        self.stop_mapping = MappingProperty("stop_mapping")

        super()._initialize_config_properties()

    def load_args_dict(self, values: dict[str: Any]) -> None:
        """ Load the command line arguments provided by the dictionary.
        Values already set will be overwritten. """
        for key, value in values.items():
            setattr(self, key, value)


C = P2GConfig()
