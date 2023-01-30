from io import StringIO

from src.datastructures.gtfs.stop import Stop


class Feed:
    """ Represents a GTFS feed. """
    def __init__(self, data: dict[str: StringIO]) -> None:
        self._create(data)

    def _create(self, data: dict[str: StringIO]) -> None:
        self.stops = Stop.from_buffer(data["stops"])
