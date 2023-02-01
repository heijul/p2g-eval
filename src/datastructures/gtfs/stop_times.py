from __future__ import annotations

from dataclasses import dataclass

from src.datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from src.datastructures.p2g_time import Time


@dataclass
class StopTime(BaseGTFSObject):
    trip_id: str
    arrival_time: Time
    departure_time: Time
    stop_id: str
    stop_sequence: int

    def __init__(self, trip_id: str, arrival_time: str, departure_time: str,
                 stop_id: str, stop_sequence: int) -> None:
        super().__init__()
        self.trip_id = trip_id
        self.arrival_time = Time.from_str(arrival_time)
        self.departure_time = Time.from_str(departure_time)
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence

    def calculate_measures(self, ground_truth: StopTimes) -> list[StopTimes]:
        ...
