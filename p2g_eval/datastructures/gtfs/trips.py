from __future__ import annotations

from dataclasses import dataclass

from p2g_eval.datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from p2g_eval.datastructures.measures.base_measure import BaseMeasure


@dataclass
class Trip(BaseGTFSObject):
    route_id: str
    service_id: str
    trip_id: str

    def calculate_measures(self, ground_truth: Trip) -> list[BaseMeasure]:
        raise NotImplementedError("Not implemented yet.")
