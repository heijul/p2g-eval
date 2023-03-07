from __future__ import annotations

from dataclasses import dataclass

from p2g_eval.datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from p2g_eval.datastructures.measures.stop_measures import (
    StopLocMeasure, StopMeasure)
from p2g_eval.datastructures.p2g_types import Location


@dataclass(init=False)
class Stop(BaseGTFSObject):
    stop_id: str
    stop_name: str
    stop_lat: float
    stop_lon: float

    def __init__(self, stop_id: str, stop_name: str,
                 lat: float, lon: float) -> None:
        super().__init__()
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_lat = lat
        self.stop_lon = lon
        self.loc = Location(float(lat), float(lon))

    def calculate_measures(self, ground_truth: Stop) -> list[StopMeasure]:
        return [StopLocMeasure().calculate(ground_truth, self)]
