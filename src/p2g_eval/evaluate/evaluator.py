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
        # TODO: Assert same length
        stop_lat1, stop_lon1 = self.m.feed1.stops[["stop_lat", "stop_lat"]]
        stop_lat2, stop_lon2 = self.m.feed1.stops[["stop_lat", "stop_lat"]]
        self.measures["stops_dist"] = {"dist": v_evaluate_stop_distance(
            stop_lat1, stop_lon1, stop_lat2, stop_lon2)}
        dist = self.measures["stops_dist"]["dist"]
        self.measures["stops_dist"].update({
            "min": dist.min(), "max": dist.max(),
            "mean": dist.mean(), "std": dist.std()})

    def evaluate(self) -> None:
        self.evaluate_stops()
