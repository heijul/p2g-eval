""" Mapping functions between objects of two different DFFeeds. """
import numpy as np
import pandas as pd
from geopy.distance import distance

from p2g_eval.config.config import C
from p2g_eval.datastructures.gtfs.feed import DFFeed


def create_contains_any_regex(strings: list[str]) -> str:
    """ Return a regex, that matches any full string in the given list. """
    return "|".join([fr"(?:{string})" for string in strings])


def evaluate_stop_distance(lat1, lon1, lat2, lon2) -> float:
    """ Return the distance between the given locations in meter. """
    return distance((lat1, lon1), (lat2, lon2)).m


v_evaluate_stop_distance = np.vectorize(evaluate_stop_distance)


class BaseMapper:
    def __init__(self, feed1: DFFeed, feed2: DFFeed) -> None:
        self.feed1 = feed1.copy()
        self.feed2 = feed2.copy()
        self.mappings = {}
        self.df_mappings = {}
        self.measures = {}
        self.is_mapped = False

    def map_stops(self) -> None:
        """ Return a mapping using the respective indices of both feeds. """
        # Get all stops of the feeds, defined in the stop_mapping.
        lefts = [left for left, _ in C.stop_mapping]
        left_regex = create_contains_any_regex(lefts)
        stops1 = self.feed1.stops
        stops1 = stops1[stops1.stop_id.str.fullmatch(left_regex, False)]
        rights = [right for _, right in C.stop_mapping]
        right_regex = create_contains_any_regex(rights)
        stops2 = self.feed2.stops
        stops2 = stops2[stops2.stop_id.str.fullmatch(right_regex, False)]

        mapping: list[tuple[int, int]] = []
        # This assumes, that all stops exist in both feeds.
        for left, right in C.stop_mapping:
            mapping.append((stops1[stops1.stop_id == left].index[0],
                            stops2[stops2.stop_id == right].index[0]))

        self.mappings["stops"] = mapping
        self.df_mappings["stops"] = pd.DataFrame(mapping,
                                                 columns=["stop1", "stop2"])

    def map(self) -> None:
        """ Try to map all objects of feed1 to those matching in feed2. """
        self.map_stops()
        self.feed1.reduce_using_stops(self.df_mappings["stops"].stop1)
        # TODO: This is probably unneccessary, because feed2 is p2g-generated.
        self.feed2.reduce_using_stops(self.df_mappings["stops"].stop2)
        self.is_mapped = True

    # TODO: Move to evaluation

    def evaluate_stops(self) -> None:
        """ Calculate the distance (min/max/mean/std) between mapped stops. """
        if not self.is_mapped:
            self.map()
        stop_lat1, stop_lon1 = self.feed1.stops[["stop_lat1", "stop_lat2"]]
        stop_lat2, stop_lon2 = self.feed1.stops[["stop_lat1", "stop_lat2"]]
        self.measures["stops_dist"] = {"dist": v_evaluate_stop_distance(
            stop_lat1, stop_lon1, stop_lat2, stop_lon2)}
        dist = self.measures["stops_dist"]["dist"]
        self.measures["stops_dist"].update({
            "min": dist.min(), "max": dist.max(),
            "mean": dist.mean(), "std": dist.std()})

    def evaluate(self) -> None:
        self.evaluate_stops()
