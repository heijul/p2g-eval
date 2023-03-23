""" Provides functions to evaluate a feed. """

import numpy as np
from geopy.distance import distance

from p2g_eval.feed_mapper import FeedMapper


def evaluate_stop_distance(lat1, lon1, lat2, lon2) -> float:
    """ Return the distance between the given locations in meter. """
    return distance((lat1, lon1), (lat2, lon2)).m


class Evaluator:
    """
    Used to evaluate the feed, mapped to a ground truth by a FeedMapper.
    """
    def __init__(self, mapper: FeedMapper) -> None:
        self.mapper = mapper
        self.measures = {}

    def evaluate_stops(self) -> None:
        """ Calculate the distance (min/max/mean/std) between mapped stops. """
        if not self.mapper.is_mapped:
            self.mapper.map()
        stops1 = self.mapper.feed1.stops[["stop_lat", "stop_lon"]]
        stops2 = self.mapper.feed2.stops[["stop_lat", "stop_lon"]]
        v_evaluate_stop_distance = np.vectorize(evaluate_stop_distance)
        self.measures["stops_dist"] = {"dist": v_evaluate_stop_distance(
            stops1.stop_lat, stops1.stop_lon,
            stops2.stop_lat, stops2.stop_lon)}
        dist = self.measures["stops_dist"]["dist"]
        self.measures["stops_dist"].update({
            "min": dist.min(), "max": dist.max(),
            "mean": dist.mean(), "std": dist.std()})

    def evaluate(self) -> None:
        """ Runs all defined evaluations. """
        self.evaluate_stops()
