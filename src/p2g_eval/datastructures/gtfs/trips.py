from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Type

from p2g_eval.datastructures.gtfs.base_gtfs_object import (
    BaseGTFSObject,
    GTFSObjectList)
from p2g_eval.datastructures.measures.base_measure import BaseMeasure


class Trips(GTFSObjectList):
    pass


@dataclass
class Trip(BaseGTFSObject):
    route_id: str
    service_id: str
    trip_id: str
    list_type: ClassVar[Type[GTFSObjectList]] = Trips

    @property
    def id(self) -> str:
        return self.trip_id

    def calculate_measures(self, ground_truth: Trip) -> list[BaseMeasure]:
        raise NotImplementedError("Not implemented yet.")
