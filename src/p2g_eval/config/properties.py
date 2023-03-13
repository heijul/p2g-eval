from pathlib import Path
from typing import TypeAlias

import pandas as pd
from custom_conf.properties.nested_property import NestedTypeProperty
from custom_conf.properties.property import Property

from p2g_eval.datastructures.gtfs.feed import Feed
from p2g_eval.in_out.feed_reader import BaseFeedReader


class FeedProperty(Property):
    def __init__(self, name: str) -> None:
        super().__init__(name, Feed)

    def __set__(self, instance, value: Feed | Path) -> None:
        # Allow paths as well.
        if isinstance(value, str):
            value = Path(value)
        if isinstance(value, Path) and value.exists():
            value = BaseFeedReader(value).read()

        super().__set__(instance, value)


M: TypeAlias = list[tuple[str, str]]


class MappingProperty(NestedTypeProperty):
    def __init__(self, name: str) -> None:
        super().__init__(name, M)

    def __set__(self, instance, value: M | str | Path) -> None:
        if isinstance(value, str) or isinstance(value, Path):
            value = self._get_value_from_str_or_path(value)
        super().__set__(instance, value)

    @staticmethod
    def _get_value_from_str_or_path(value_str: str | Path) -> M:
        """ Returns a value of the proper type, in case a path was given. """
        if isinstance(value_str, str):
            value_str = Path(value_str)
        if not value_str.exists():
            raise Exception("GOT INVALID PATH WHEN SETTING VALUE DYNAMICALLY")
        values = pd.read_csv(value_str).values
        return [(str(val[0]), str(val[1])) for val in values]
