from __future__ import annotations

from io import StringIO
from typing import Any

import pandas as pd
from pandas.errors import EmptyDataError

from p2g_eval.datastructures.gtfs.calendar import Calendar
from p2g_eval.datastructures.gtfs.calendar_dates import CalendarDate
from p2g_eval.datastructures.gtfs.routes import Route
from p2g_eval.datastructures.gtfs.stop import Stop
from p2g_eval.datastructures.gtfs.stop_times import StopTime
from p2g_eval.datastructures.gtfs.trips import Trip


def read_from_buffer(buffer: StringIO) -> pd.DataFrame:
    try:
        # noinspection PyTypeChecker
        df = pd.read_csv(buffer, dtype="str")
    except EmptyDataError:
        return pd.DataFrame()
    return df.fillna("")


class DFFeed:
    """ Represents a GTFS feed. """
    def __init__(self, data: dict[str: StringIO] = None) -> None:
        self.stops = None
        self.routes = None
        self.trips = None
        self.stop_times = None
        self.calendar = None
        self.calendar_dates = None
        if data is not None:
            self._create(data)

    def _create(self, data: dict[str: StringIO]) -> None:
        self.stops = read_from_buffer(data["stops"])
        self.routes = read_from_buffer(data["routes"])
        self.trips = read_from_buffer(data["trips"])
        self.stop_times = read_from_buffer(data["stop_times"])
        self.calendar = read_from_buffer(data["calendar"])
        self.calendar_dates = read_from_buffer(data["calendar_dates"])

    def reduce_using_stops(self, mapped_stop_ids: pd.Series) -> None:
        """ Removes all entries in the feed, that are not required.

        First, the mapped_stop_ids are used to remove all stops, that do not
        have any of these stop_ids. Then, the stop_times are filtered, such
        that it contains only trips using these and only these stops. Finally,
        the trips are used to keep only routes, calendar and calendar_dates
        entries, that are used in these trips.
        """
        # Remove all unused stops.
        self.stops = self.stops.loc[mapped_stop_ids]
        # Get all stop_times that use these, all these and only these stops.
        st = self.stop_times.copy()
        st["valid_stop"] = st.stop_id.isin(self.stops.stop_id)
        # All stop_times of complete trips, that contain only the valid stops.
        mask = st.valid_stop.eq(True).groupby(st.trip_id).transform("all")
        self.stop_times = st[mask]
        # Only trips described in the stop_times are served.
        trip_mask = self.trips.trip_id.isin(self.stop_times.trip_id)
        self.trips = self.trips[trip_mask]
        # Remove all routes, that are not used.
        route_mask = self.routes.route_id.isin(self.trips.route_id)
        self.routes = self.routes[route_mask]
        # Remove all calendar/calendar_dates with unmatched service_ids.
        service_ids = self.trips.service_id
        calendar_mask = self.calendar.service_id.isin(service_ids)
        self.calendar = self.calendar[calendar_mask]
        calendar_dates_mask = self.calendar_dates.service_id.isin(service_ids)
        self.calendar_dates = self.calendar_dates[calendar_dates_mask]

    def copy(self) -> DFFeed:
        """ Returns a copy of the current DFFeed. """
        feed = DFFeed()
        feed.stops = self.stops.copy()
        feed.routes = self.routes.copy()
        feed.trips = self.trips.copy()
        feed.stop_times = self.stop_times.copy()
        feed.calendar = self.calendar.copy()
        feed.calendar_dates = self.calendar_dates.copy()
        return feed

    def __eq__(self, other) -> bool:
        if not isinstance(other, DFFeed):
            return False
        fields = ["stops", "stop_times", "routes", "trips",
                  "calendar", "calendar_dates"]
        for field in fields:
            # noinspection PyTypeChecker
            if not all(getattr(self, field) == getattr(other, field)):
                return False
        return True


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
