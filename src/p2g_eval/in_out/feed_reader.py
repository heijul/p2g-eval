from io import StringIO
from pathlib import Path
from zipfile import ZipFile

from p2g_eval.datastructures.feed import Feed


class BaseFeedReader:
    """ Takes a GTFS feed and transforms its data into our datastructures. """
    def __init__(self, feed_path: Path) -> None:
        self.feed_path = feed_path
        self.feed = None

    def _read_file(self, name: str) -> StringIO:
        """ Read the given file and return its content as stream. """
        try:
            with ZipFile(self.feed_path).open(name, "r") as file:

                return StringIO(file.read().decode("utf-8"))
        except (PermissionError, OSError) as e:
            raise e

    def read(self) -> Feed:
        """ Reads the feed and creates the neccessary datastructures. """

        def remove_ext(filename: str) -> str:
            """ Remove the file extension from the given filename. """
            return filename.rstrip(".txt")

        if self.feed:
            return self.feed

        # Read required files.
        req_names = ["stops.txt", "routes.txt", "stop_times.txt", "trips.txt"]
        data = {remove_ext(name): self._read_file(name) for name in req_names}

        # Read conditionally required files.
        cond_req_names = ["calendar.txt", "calendar_dates.txt"]
        requirements_met = False
        for name in cond_req_names:
            try:
                contents = self._read_file(name)
                data[remove_ext(name)] = contents
                requirements_met = True
            except KeyError:  # File does not exist.
                data[remove_ext(name)] = StringIO()

        # At least one of the conditionally required files is necessary.
        if requirements_met:
            self.feed = Feed(data)
            return self.feed

        raise Exception("The given feed contains neither a 'calendar.txt' "
                        "nor a 'calendar_dates.txt'.")
