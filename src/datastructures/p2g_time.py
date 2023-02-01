from __future__ import annotations


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

