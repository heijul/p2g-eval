""" Provides the ability to store the files of a GTFS feed as DataFrames. """

from __future__ import annotations

from io import StringIO

import pandas as pd
from pandas.errors import EmptyDataError


def read_from_buffer(buffer: StringIO) -> pd.DataFrame:
    """ Read the .csv file contained in the buffer. """
    try:
        # noinspection PyTypeChecker
        df = pd.read_csv(buffer, dtype="str")
    except EmptyDataError:
        return pd.DataFrame()
    return df.fillna("")


class Feed:
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
        stop_times = self.stop_times.copy()
        stop_times["valid_stop"] = stop_times.stop_id.isin(self.stops.stop_id)
        # All stop_times of complete trips, that contain only the valid stops.
        mask = stop_times.valid_stop.eq(
            True).groupby(stop_times.trip_id).transform("all")
        self.stop_times = stop_times[mask]
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

    def copy(self) -> Feed:
        """ Returns a copy of the current DFFeed. """
        feed = Feed()
        feed.stops = self.stops.copy()
        feed.routes = self.routes.copy()
        feed.trips = self.trips.copy()
        feed.stop_times = self.stop_times.copy()
        feed.calendar = self.calendar.copy()
        feed.calendar_dates = self.calendar_dates.copy()
        return feed

    @property
    def fields(self) -> list[str]:
        """ The fields (i.e. files without extension) of the feed. """
        return ["stops", "routes", "trips",
                "stop_times", "calendar", "calendar_dates"]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Feed):
            return False
        for field in self.fields:
            # noinspection PyTypeChecker
            if not all(getattr(self, field) == getattr(other, field)):
                return False
        return True
