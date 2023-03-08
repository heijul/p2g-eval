from io import StringIO
from typing import Any

from p2g_eval.datastructures.gtfs.calendar import Calendar
from p2g_eval.datastructures.gtfs.calendar_dates import CalendarDate
from p2g_eval.datastructures.gtfs.routes import Route
from p2g_eval.datastructures.gtfs.stop import Stop
from p2g_eval.datastructures.gtfs.stop_times import StopTime
from p2g_eval.datastructures.gtfs.trips import Trip


class Feed:
    """ Represents a GTFS feed. """
    def __init__(self, data: dict[str: StringIO]) -> None:
        self._create(data)

    def _create(self, data: dict[str: StringIO]) -> None:
        self.stops = Stop.from_buffer(data["stops"])
        self.routes = Route.from_buffer(data["routes"])
        self.trips = Trip.from_buffer(data["trips"])
        self.stop_times = StopTime.from_buffer(data["stop_times"])
        self.calendar = Calendar.from_buffer(data["calendar"])
        self.calendar_dates = CalendarDate.from_buffer(data["calendar_dates"])

    @property
    def field_names(self) -> list[str]:
        return ["stops", "routes", "trips",
                "stop_times", "calendar", "calendar_dates"]

    def __eq__(self, other: Any) -> bool:
        """ Two feeds are equal if all their objects are equal. """
        if not isinstance(other, Feed):
            return False

        for field in self.field_names:
            if getattr(self, field) != getattr(other, field):
                return False
        return True
