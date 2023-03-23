import numpy as np
from geopy.distance import distance

from p2g_eval.feed_mapper import FeedMapper


def evaluate_stop_distance(lat1, lon1, lat2, lon2) -> float:
    """ Return the distance between the given locations in meter. """
    return distance((lat1, lon1), (lat2, lon2)).m


class Evaluator:
    def __init__(self, mapper: FeedMapper) -> None:
        self.m = mapper
        self.measures = {}

    def evaluate_stops(self) -> None:
        """ Calculate the distance (min/max/mean/std) between mapped stops. """
        if not self.m.is_mapped:
            self.m.map()
        stops1 = self.m.feed1.stops[["stop_lat", "stop_lon"]]
        stops2 = self.m.feed2.stops[["stop_lat", "stop_lon"]]
        v_evaluate_stop_distance = np.vectorize(evaluate_stop_distance)
        self.measures["stops_dist"] = {"dist": v_evaluate_stop_distance(
            stops1.stop_lat, stops1.stop_lon,
            stops2.stop_lat, stops2.stop_lon)}
        dist = self.measures["stops_dist"]["dist"]
        self.measures["stops_dist"].update({
            "min": dist.min(), "max": dist.max(),
            "mean": dist.mean(), "std": dist.std()})

    def evaluate(self) -> None:
        self.evaluate_stops()
