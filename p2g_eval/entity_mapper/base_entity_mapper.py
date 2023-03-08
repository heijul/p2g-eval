from __future__ import annotations

import re
from typing import Iterator, Optional, TypeVar

from p2g_eval.config.config import C
from p2g_eval.datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from p2g_eval.datastructures.gtfs.feed import Feed


class BaseEntityMapper:
    def __init__(self, true_feed: Feed, test_feed: Feed) -> None:
        self.true_feed = true_feed
        self.test_feed = test_feed

    def map(self) -> EntityMapping:
        pass


class StopEntityMapper(BaseEntityMapper):
    def __init__(self, true_feed: Feed, test_feed: Feed) -> None:
        super().__init__(true_feed, test_feed)

    def map_naive(self) -> EntityMapping:
        """ Map each stop of the true stops (len n) to the first stop
        of the test feeds' stops (len k), that has the same name.
        Naive algorithm, taking O(n*k). However, k is generally small (~ 20),
        so this _might_ be ok for now.
        """
        mapping = EntityMapping()
        for test_stop in self.test_feed.stops:
            for true_stop in self.true_feed.stops:
                search = re.search(test_stop.normalized_name,
                                   true_stop.normalized_name)
                if search:
                    mapping.add_next(true_stop, test_stop)
                    break
        return mapping

    def map_manual(self) -> EntityMapping:
        """ Basic mapping, where each mapping has been manually defined. """
        mapping = EntityMapping()
        for true_stop_id, test_stop_id in C.stop_mapping:
            true_stop = self.true_feed.stops.id_map[true_stop_id]
            test_stop = self.test_feed.stops.id_map[test_stop_id]
            mapping.add_next(true_stop, test_stop)
        return mapping

    def map(self) -> EntityMapping:
        if C.stop_mapping:
            return self.map_manual()
        return self.map_naive()


T = TypeVar("T", bound=BaseGTFSObject)


class EntityMapping:
    def __init__(self) -> None:
        """ A mapping between two entities. """
        self.obj_type: Optional[T] = None
        self._mapping: tuple[tuple[T, T]] = tuple()

    @property
    def mapping(self) -> tuple[tuple[T, T]]:
        return self._mapping

    def add_next(self, left: T, right: T) -> None:
        """ Add a new entry to the mapping. """
        self._mapping += ((left, right),)

    def __iter__(self) -> Iterator:
        yield from self.mapping

    def __len__(self) -> int:
        return len(self.mapping)
