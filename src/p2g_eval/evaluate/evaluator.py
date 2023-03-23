from p2g_eval.entity_mapper.dataframe_mapper import BaseMapper
from p2g_eval.evaluate.evaluations import v_evaluate_stop_distance


class Evaluator:
    def __init__(self, mapper: BaseMapper) -> None:
        self.m = mapper
        self.measures = {}

    def evaluate_stops(self) -> None:
        """ Calculate the distance (min/max/mean/std) between mapped stops. """
        if not self.m.is_mapped:
            self.m.map()
        stops1 = self.m.feed1.stops[["stop_lat", "stop_lon"]]
        stops2 = self.m.feed2.stops[["stop_lat", "stop_lon"]]
        self.measures["stops_dist"] = {"dist": v_evaluate_stop_distance(
            stops1.stop_lat, stops1.stop_lon,
            stops2.stop_lat, stops2.stop_lon)}
        dist = self.measures["stops_dist"]["dist"]
        self.measures["stops_dist"].update({
            "min": dist.min(), "max": dist.max(),
            "mean": dist.mean(), "std": dist.std()})

    def evaluate(self) -> None:
        self.evaluate_stops()
