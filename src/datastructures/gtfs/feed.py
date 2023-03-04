from io import StringIO

from src.datastructures.gtfs.calendar import Calendar
from src.datastructures.gtfs.calendar_dates import CalendarDate
from src.datastructures.gtfs.routes import Route
from src.datastructures.gtfs.stop import Stop
from src.datastructures.gtfs.stop_times import StopTime
from src.datastructures.gtfs.trips import Trip


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
