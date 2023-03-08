from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Type, TYPE_CHECKING

from p2g_eval.datastructures.gtfs.base_gtfs_object import (
    BaseGTFSObject,
    GTFSObjectList)
from p2g_eval.datastructures.p2g_types import Date


if TYPE_CHECKING:
    from p2g_eval.datastructures.gtfs.calendar_dates import CalendarDate


class Calendars(GTFSObjectList):
    pass


@dataclass
class Calendar(BaseGTFSObject):
    service_id: str
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    start_date: Date
    end_date: Date
    list_type: ClassVar[Type[GTFSObjectList]] = Calendars

    @property
    def id(self) -> str:
        return self.service_id

    def to_dates(self) -> CalendarDate:
        raise NotImplementedError("Not implemented yet.")

    def calculate_measures(self, ground_truth: Calendar) -> list[Calendar]:
        raise NotImplementedError("Not implemented yet.")
