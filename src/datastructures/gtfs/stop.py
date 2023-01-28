from __future__ import annotations

from src.datastructures.location import Location


class Stop:
    def __init__(self, id_: str, name: str, loc: Location) -> None:
        self.id = id_
        self.name = name
        self.loc = loc

    @staticmethod
    def from_values(header_info: list[str], values: list[str]) -> Stop:
        """ Returns a Stop containing the defining values. """
        headers = ["stop_id", "stop_name", "stop_lat", "stop_lon"]
        ids = [i for i, header in enumerate(header_info) if header in headers]

        return Stop(*[values[i] for i in ids])
