from io import StringIO
from pathlib import Path
from zipfile import ZipFile

from src.datastructures.gtfs.feed import Feed


class BaseFeedReader:
    """ Takes a GTFS feed and transforms its data into our datastructures. """
    def __init__(self, feed_path: Path) -> None:
        self.feed_path = feed_path

    def _read_file(self, name: str, noexist_ok: bool = False) -> StringIO:
        """ Read the given file and return its content as stream. """
        try:
            with ZipFile(self.feed_path).open(name, "r") as file:

                return StringIO(file.read().decode("utf-8"))
        except (PermissionError, OSError) as e:
            raise e
        except KeyError as e:
            if noexist_ok:
                return StringIO()
            # TODO: Better error message
            raise e

    def read(self) -> Feed:
        """ Reads the feed and creates the neccessary datastructures. """
        names = ["stops.txt", "routes.txt", "stop_times.txt", "trips.txt"]
        conditional_req = ["calendar.txt", "calendar_dates.txt"]
        data = {}
        for name in names + conditional_req:
            noexist_ok = name in conditional_req
            data[name.rstrip(".txt")] = self._read_file(name, noexist_ok)

        return Feed(data)
