from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from datastructures.gtfs.base_gtfs_object import BaseGTFSObject
from datastructures.p2g_types import Date


if TYPE_CHECKING:
    from datastructures.gtfs.calendar_dates import CalendarDate


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

    def to_dates(self) -> CalendarDate:
        raise NotImplementedError("Not implemented yet.")

    def calculate_measures(self, ground_truth: Calendar) -> list[Calendar]:
        raise NotImplementedError("Not implemented yet.")
