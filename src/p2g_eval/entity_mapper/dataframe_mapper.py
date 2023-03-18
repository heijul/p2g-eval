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
        self.feed1 = feed1
        self.feed2 = feed2
        self.mappings = {}
        self.df_mappings = {}
        self.measures = {}

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
        self.df_mappings["stops"] = pd.DataFrame(
            mapping, columns=["stop1", "stop2"])

    def map(self) -> None:
        """ Try to map all objects of feed1 to those matching in feed2. """
        self.map_stops()

    def evaluate_stops(self) -> None:
        """ Calculate the distance (min/max/mean/std) between mapped stops. """
        stops1 = self.feed1.stops.loc[self.df_mappings["stops"].stop1]
        stops2 = self.feed2.stops.loc[self.df_mappings["stops"].stop2]
        self.measures["stops_dist"] = {
            "dist": v_evaluate_stop_distance(stops1.stop_lat, stops1.stop_lon,
                                             stops2.stop_lat, stops2.stop_lon)}
        dist = self.measures["stops_dist"]["dist"]
        self.measures["stops_dist"].update({
            "min": dist.min(), "max": dist.max(),
            "mean": dist.mean(), "std": dist.std()})

    def evaluate(self) -> None:
        self.evaluate_stops()
