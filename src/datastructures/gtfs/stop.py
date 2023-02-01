from __future__ import annotations

from dataclasses import dataclass

from src.datastructures.measures.stop_measures import (
    StopLocMeasure, StopMeasure)
from src.datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from src.datastructures.location import Location


@dataclass
class Stop(BaseGTFSObject):
    stop_id: str
    stop_name: str
    loc: Location

    def __init__(self, stop_id: str, stop_name: str, lat: float, lon: float
                 ) -> None:
        super().__init__()
        self.id = stop_id
        self.stop_name = stop_name
        self.loc = Location(float(lat), float(lon))

    def calculate_measures(self, ground_truth: Stop) -> list[StopMeasure]:
        return [StopLocMeasure().calculate(ground_truth, self)]
