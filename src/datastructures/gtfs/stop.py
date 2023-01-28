from __future__ import annotations

from src.datastructures.gtfs.base_gtfs_file import BaseGTFSFile
from src.datastructures.location import Location


class Stop(BaseGTFSFile):
    fields = ["stop_id", "stop_name", "stop_lat", "stop_lon"]

    def __init__(self, id_: str, name: str, lat: str, lon: str) -> None:
        super().__init__()
        self.id = id_
        self.name = name
        self.loc = Location(float(lat), float(lon))
