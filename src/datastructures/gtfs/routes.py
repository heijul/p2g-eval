from __future__ import annotations

from dataclasses import dataclass

from src.datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from src.datastructures.measures.base_measure import BaseMeasure


@dataclass
class Route(BaseGTFSObject):
    route_id: str
    short_name: str
    long_name: str
    route_type: str

    def calculate_measures(self, ground_truth: Route
                           ) -> list[BaseMeasure]:
        ...
