from __future__ import annotations

from src.datastructures.measures.stop_measures import (
    StopLocMeasure, StopMeasure)
from src.datastructures.gtfs.base_gtfs_file import BaseGTFSObject
from src.datastructures.location import Location


class Stop(BaseGTFSObject):
    fields = ["stop_id", "stop_name", "stop_lat", "stop_lon"]

    def __init__(self, id_: str, name: str, lat: str, lon: str) -> None:
        super().__init__()
        self.id = id_
        self.name = name
        self.loc = Location(float(lat), float(lon))

    def calculate_measures(self, ground_truth: Stop) -> list[StopMeasure]:
        return [StopLocMeasure().calculate(ground_truth, self)]
