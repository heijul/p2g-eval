""" Different measures for different GTFS objects. """

from typing import Iterable

import numpy as np
from geopy.distance import distance

from p2g_eval.feed_mapper import FeedMapper


def evaluate_stop_distance(lat1, lon1, lat2, lon2) -> float:
    """ Return the distance between the given locations in meter. """
    return distance((lat1, lon1), (lat2, lon2)).m


def get_max_float_size(items: Iterable[float], decimal_places: int = 2) -> int:
    """ Return the maximal length of the largest number + decimal places. """
    return max((len(f"{item:.{decimal_places}f}") for item in items))


def get_max_str_size(items: Iterable[str]) -> int:
    """ Return the maximal length of the longest string. """
    return max(map(len, items))


class StopMeasure:
    """ Basic measure for stops. """
    def __init__(self, mapper: FeedMapper) -> None:
        self.mapper = mapper
        self.results = None
        self.name = "stop location"

    def calculate(self) -> None:
        """ Calculate the distance (min/max/mean/std) between mapped stops. """
        if not self.mapper.is_mapped:
            self.mapper.map()
        stops1 = self.mapper.feed1.stops[["stop_lat", "stop_lon"]]
        stops2 = self.mapper.feed2.stops[["stop_lat", "stop_lon"]]
        v_evaluate_stop_distance = np.vectorize(evaluate_stop_distance)
        self.results = v_evaluate_stop_distance(
            stops1.stop_lat, stops1.stop_lon, stops2.stop_lat, stops2.stop_lon)

    def get_meta_values(self, *which) -> dict[str: float]:
        """ Calculates the selected meta values about the results. """
        values = {}
        if "min" in which:
            values["min"] = self.results.min()
        if "max" in which:
            values["max"] = self.results.max()
        if "mean" in which:
            values["mean"] = self.results.mean()
        if "std" in which:
            values["std"] = self.results.std()
        return values

    def _meta_values_to_output(self) -> list[str]:
        lines = [""]
        meta_values = self.get_meta_values("min", "max", "mean", "std")
        max_meta_size = get_max_float_size(meta_values.values())
        for key, value in meta_values.items():
            lines += [f"\t{key: <5}: {value:{max_meta_size}.2f}"]
        return lines

    def to_output(self, values_only: bool) -> str:
        """ Return a human-readable string about the results. """
        if values_only:
            return "\n".join(map(str, self.results))

        lines = [f"Result for the {self.name} measure"]
        stops1 = self.mapper.feed1.stops
        stops2 = self.mapper.feed2.stops
        max_size = get_max_float_size(self.results)
        stops1_max_size = get_max_str_size(stops1.stop_name)
        stops2_max_size = get_max_str_size(stops2.stop_name)
        delim = "  | "
        titles = ["Ground truth stop", "Evaluation feed stop", "Distance in m"]
        max_size = max((max_size, len(titles[-1])))
        lines += [f"{titles[0]: >{stops1_max_size}}{delim}"
                  f"{titles[1]: >{stops2_max_size}}{delim}"
                  f"{titles[2]: >{max_size}}"]
        lines += [len(lines[-1]) * "-"]
        zipped = zip(stops1.iterrows(), stops2.iterrows(), self.results)
        for (_, stop_1), (_, stop_2), result in zipped:
            lines += [f"{stop_1.stop_name: >{stops1_max_size}}{delim}"
                      f"{stop_2.stop_name: >{stops2_max_size}}{delim}"
                      f"{result: >{max_size}.2f}"]

        lines += self._meta_values_to_output()
        return "\n".join(lines)
