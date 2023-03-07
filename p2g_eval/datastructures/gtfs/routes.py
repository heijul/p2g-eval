from __future__ import annotations

from dataclasses import dataclass

from datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from datastructures.measures.base_measure import BaseMeasure
from datastructures.p2g_types import RouteType


@dataclass
class Route(BaseGTFSObject):
    route_id: str
    route_short_name: str
    route_long_name: str
    route_type: RouteType

    def calculate_measures(self, ground_truth: Route) -> list[BaseMeasure]:
        raise NotImplementedError("Not implemented yet.")
