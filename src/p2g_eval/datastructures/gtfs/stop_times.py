from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Type

from p2g_eval.datastructures.gtfs.base_gtfs_object import (
    BaseGTFSObject,
    GTFSObjectList)
from p2g_eval.datastructures.p2g_types import Time


class StopTimes(GTFSObjectList):
    pass


@dataclass(init=False)
class StopTime(BaseGTFSObject):
    trip_id: str
    arrival_time: Time
    departure_time: Time
    stop_id: str
    stop_sequence: int
    list_type: ClassVar[Type[GTFSObjectList]] = StopTimes

    def __init__(self, trip_id: str, arrival_time: str, departure_time: str,
                 stop_id: str, stop_sequence: int) -> None:
        super().__init__()
        self.trip_id = trip_id
        self.arrival_time = Time.from_str(arrival_time)
        self.departure_time = Time.from_str(departure_time)
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence

    @property
    def id(self) -> str:
        return self.trip_id

    def calculate_measures(self, ground_truth: StopTime) -> list[StopTime]:
        raise NotImplementedError("Not implemented yet.")
