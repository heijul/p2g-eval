""" Provides some p2g-eval specific custom_conf-properties. """

from pathlib import Path
from typing import TypeAlias

import pandas as pd
from custom_conf.errors import PropertyError
from custom_conf.properties.nested_property import NestedTypeProperty
from custom_conf.properties.property import Property


from p2g_eval.feed import Feed
from p2g_eval.in_out.feed_reader import BaseFeedReader


class FeedProperty(Property):
    """ Property containing a GTFS feed. """
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
    """ Property used to provide a mapping between the objects of a ground
    truth and a test set. """
    def __init__(self, name: str) -> None:
        super().__init__(name, M)

    def __set__(self, instance, value: M | str | Path) -> None:
        if isinstance(value, (Path, str)):
            value = self._get_value_from_str_or_path(value)
        super().__set__(instance, value)

    @staticmethod
    def _get_value_from_str_or_path(value_str: str | Path) -> M:
        """ Returns a value of the proper type, in case a path was given. """
        if isinstance(value_str, str):
            value_str = Path(value_str)
        if not value_str.exists():
            raise MissingMapfileError(
                name=MappingProperty.__class__.__name__, value=value_str)
        values = pd.read_csv(value_str).values
        return [(str(val[0]), str(val[1])) for val in values]


class MissingMapfileError(PropertyError):
    """ Error raised, when a mapfile provided to a MappingProperty does
    not exist or is not a proper file.
    """
    def __init__(self, **kwargs) -> None:
        if "name" not in kwargs or "value" not in kwargs:
            msg = "A path to a mapping file was provided, that does not exist."
            super().__init__(msg)
            return
        self.name = kwargs["name"]
        self.value = kwargs["value"]
        msg = (f"The property '{self.name}' was provided with the path "
               f"'{self.value}' to a mapping file, even though the path does "
               f"not exist or is not a valid file.")
        super().__init__(msg)
