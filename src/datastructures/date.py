from __future__ import annotations

from datetime import datetime as dt


class Date:
    """ Date type used by GTFS files. """
    def __init__(self, year: int, month: int, day: int) -> None:
        self.year = year
        self.month = month
        self.day = day

    @staticmethod
    def from_str(date_str: str) -> Date:
        date = dt.strptime(date_str, "%Y%m%d")
        return Date(date.year, date.month, date.day)
