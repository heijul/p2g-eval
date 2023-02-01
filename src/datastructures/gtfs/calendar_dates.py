from __future__ import annotations

from dataclasses import dataclass

from src.datastructures.date import Date
from src.datastructures.gtfs.base_gtfs_object import BaseGTFSObject


@dataclass(init=False)
class CalendarDate(BaseGTFSObject):
    service_id: str
    date: Date
    exception_type: int

    def __init__(self, service_id: str, date: Date, exception_type: int
                 ) -> None:
        super().__init__()
        self.service_id = service_id
        self.date = date
        # TODO: Check if exception_type in [1, 2]
        self.exception_type = exception_type

    def calculate_measures(
            self, ground_truth: CalendarDate) -> list[CalendarDate]:
        ...
