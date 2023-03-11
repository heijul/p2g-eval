from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Type

from p2g_eval.datastructures.gtfs.base_gtfs_object import (
    BaseGTFSObject,
    GTFSObjectList)
from p2g_eval.datastructures.measures.base_measure import BaseMeasure
from p2g_eval.datastructures.p2g_types import RouteType


class Routes(GTFSObjectList):
    pass


@dataclass
class Route(BaseGTFSObject):
    route_id: str
    route_short_name: str
    route_long_name: str
    route_type: RouteType
    list_type: ClassVar[Type[GTFSObjectList]] = Routes

    @property
    def id(self) -> str:
        return self.route_id

    def calculate_measures(self, ground_truth: Route) -> list[BaseMeasure]:
        raise NotImplementedError("Not implemented yet.")
