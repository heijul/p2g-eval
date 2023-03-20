""" Mapping functions between objects of two different DFFeeds. """
import pandas as pd

from p2g_eval.config.config import C
from p2g_eval.datastructures.gtfs.feed import DFFeed


def create_contains_any_regex(strings: list[str]) -> str:
    """ Return a regex, that matches any full string in the given list. """
    return "|".join([fr"(?:{string})" for string in strings])


class BaseMapper:
    def __init__(self, feed1: DFFeed, feed2: DFFeed) -> None:
        self.feed1 = feed1.copy()
        self.feed2 = feed2.copy()
        self.mappings = {}
        self.is_mapped = False

    def map_stops(self, stop_mapping) -> None:
        """ Return a mapping using the respective indices of both feeds. """
        # Get all stops of the feeds, defined in the stop_mapping.
        lefts = [left for left, _ in stop_mapping]
        left_regex = create_contains_any_regex(lefts)
        stops1 = self.feed1.stops
        stops1 = stops1[stops1.stop_id.str.fullmatch(left_regex, False)]

        rights = [right for _, right in stop_mapping]
        right_regex = create_contains_any_regex(rights)
        stops2 = self.feed2.stops
        stops2 = stops2[stops2.stop_id.str.fullmatch(right_regex, False)]

        mapping: list[tuple[int, int]] = []
        # This assumes, that all stops exist in both feeds.
        # TODO: Fix mapping in case a feed does not contain one stop.
        for left, right in stop_mapping:
            mapping.append((stops1[stops1.stop_id == left].index[0],
                            stops2[stops2.stop_id == right].index[0]))

        columns = ["stop1", "stop2"]
        self.mappings["stops"] = pd.DataFrame(mapping, columns=columns)

    def map(self) -> None:
        """ Try to map all objects of feed1 to those matching in feed2. """
        self.map_stops(C.stop_mapping)
        self.feed1.reduce_using_stops(self.mappings["stops"].stop1)
        # TODO: This is probably unneccessary, because feed2 is p2g-generated.
        self.feed2.reduce_using_stops(self.mappings["stops"].stop2)

        # TODO: Remaining mappings.
        self.is_mapped = True
