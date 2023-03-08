from __future__ import annotations

import re
from typing import Iterator, Optional, TypeVar

from p2g_eval.config.config import C
from p2g_eval.datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from p2g_eval.datastructures.gtfs.feed import Feed


class BaseEntityMapper:
    def __init__(self, ground_truth: Feed, feed: Feed) -> None:
        self.ground_truth = ground_truth
        self.feed = feed

    def map(self) -> EntityMapping:
        pass


class StopEntityMapper(BaseEntityMapper):
    def __init__(self, ground_truth: Feed, feed: Feed) -> None:
        super().__init__(ground_truth, feed)

    def map_naive(self) -> EntityMapping:
        """ Map each stop of the ground truths stops (len n) to the first stop
        of the second feeds stops (len k), that has the same name.
        Naive algorithm, taking O(n*k). However, k is generally small (~ 20),
        so this _might_ be ok for now.
        """
        mapping = EntityMapping()
        for feed_stop in self.feed.stops:
            for gt_stop in self.ground_truth.stops:
                search = re.search(feed_stop.normalized_name,
                                   gt_stop.normalized_name)
                if search:
                    mapping.add_next(gt_stop, feed_stop)
                    break
        return mapping

    def map_manual(self) -> EntityMapping:
        """ Basic mapping, where each mapping has been manually defined. """
        mapping = EntityMapping()
        for gt_stop_id, feed_stop_id in C.stop_mapping:
            gt_stop = self.ground_truth.stops.id_map[gt_stop_id]
            feed_stop = self.feed.stops.id_map[feed_stop_id]
            mapping.add_next(gt_stop, feed_stop)
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
