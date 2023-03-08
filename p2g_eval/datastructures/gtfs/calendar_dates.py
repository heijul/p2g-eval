from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Type, TYPE_CHECKING

from p2g_eval.datastructures.gtfs.base_gtfs_object import (
    BaseGTFSObject,
    GTFSObjectList)
from p2g_eval.datastructures.p2g_types import Date, GTFSExceptionType


if TYPE_CHECKING:
    from p2g_eval.datastructures.gtfs.calendar import Calendar


class CalendarDates(GTFSObjectList):
    pass


@dataclass(init=False)
class CalendarDate(BaseGTFSObject):
    service_id: str
    date: Date
    exception_type: int
    list_type: ClassVar[Type[GTFSObjectList]] = CalendarDates

    def __init__(self, service_id: str, date: Date,
                 exception_type: GTFSExceptionType) -> None:
        super().__init__()
        self.service_id = service_id
        self.date = date
        self.exception_type = exception_type

    @property
    def id(self) -> str:
        raise Exception("CalendarDates do not have an ID.")

    def to_calendar(self) -> Calendar:
        raise NotImplementedError("Not implemented yet.")

    def calculate_measures(
            self, ground_truth: CalendarDate) -> list[CalendarDate]:
        raise NotImplementedError("Not implemented yet.")
