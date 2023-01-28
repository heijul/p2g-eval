from __future__ import annotations

from geopy.distance import distance


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
