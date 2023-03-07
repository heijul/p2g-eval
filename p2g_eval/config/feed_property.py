from pathlib import Path

from custom_conf.properties.property import Property
from p2g_eval.datastructures.gtfs.feed import Feed
from p2g_eval.in_out.feed_reader import BaseFeedReader


class FeedProperty(Property):
    def __init__(self, name: str) -> None:
        super().__init__(name, Feed)

    def __set__(self, instance, value: Feed | Path) -> None:
        if isinstance(value, Path):
            value = BaseFeedReader(value).read()
        super().__set__(instance, value)
