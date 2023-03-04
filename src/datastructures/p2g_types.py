from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from datetime import datetime as dt

from geopy.distance import distance


class GTFSExceptionType(IntEnum):
    added = 1
    removed = 2


class Time:
    """ Time object used by GTFS files. Allows hours >= 24 """
    def __init__(self, hours: int, minutes: int, seconds: int) -> None:
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @staticmethod
    def from_str(time_str: str) -> Time:
        """ Creates a Time object from the given string. """
        # No need to use datetime here, because the format is so simple.
        hours, minutes, seconds = time_str.strip().split(":")
        return Time(hours, minutes, seconds)


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


class Location:
    """ Describes a location using latitude and longitude. """
    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    def as_tuple(self) -> tuple[float, float]:
        """ Return the location as tuple. """
        return self.lat, self.lon

    def distance(self, other: Location) -> int:
        """ The direct distance to the other location in meters. """
        return int(distance(self.as_tuple(), other.as_tuple()).m)


class RouteType(IntEnum):
    """ The routetype as described by the gtfs. """
    Tram = 0
    StreetCar = 1
    LightRail = 2
    Subway = 3
    Metro = 4
    Rail = 5
    Bus = 6
    Ferry = 7
    CableTram = 8
    AerialLift = 9
    SuspendedCableCar = 10
    Funicular = 11
    Trolleybus = 12
    Monorail = 13
