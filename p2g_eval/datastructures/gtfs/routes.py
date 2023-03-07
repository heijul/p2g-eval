from __future__ import annotations

from dataclasses import dataclass

from p2g_eval.datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from p2g_eval.datastructures.measures.base_measure import BaseMeasure
from p2g_eval.datastructures.p2g_types import RouteType


@dataclass
class Route(BaseGTFSObject):
    route_id: str
    route_short_name: str
    route_long_name: str
    route_type: RouteType

    def calculate_measures(self, ground_truth: Route) -> list[BaseMeasure]:
        raise NotImplementedError("Not implemented yet.")
