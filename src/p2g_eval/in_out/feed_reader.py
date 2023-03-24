""" Provides the BaseFeedReader, which can be used to read GTFS feeds. """

from io import StringIO
from pathlib import Path
from zipfile import ZipFile

from p2g_eval.feed import Feed


def read_zip_file(zip_path: str | Path, name: str) -> StringIO:
    """ Read the given file and return its content as stream. """
    try:
        with ZipFile(zip_path).open(name, "r") as file:
            return StringIO(file.read().decode("utf-8"))
    except KeyError as e:
        raise MissingReqFileError(zip_path=zip_path, file_name=name) from e
    except (PermissionError, OSError) as e:
        raise e


class BaseFeedReader:
    """ Takes a GTFS feed and transforms its data into our datastructures. """
    def __init__(self, feed_path: Path) -> None:
        self.feed_path = feed_path
        self.feed = None

    def read(self) -> Feed:
        """ Reads the feed and creates the neccessary datastructures. """

        def remove_ext(filename: str) -> str:
            """ Remove the file extension from the given filename. """
            return filename.rstrip(".txt")

        if self.feed:
            return self.feed

        # Read required files.
        req_names = ["stops.txt", "routes.txt", "stop_times.txt", "trips.txt"]
        data = {remove_ext(name): read_zip_file(self.feed_path, name)
                for name in req_names}

        # Read conditionally required files.
        cond_req_names = ["calendar.txt", "calendar_dates.txt"]
        requirements_met = False
        for name in cond_req_names:
            try:
                contents = read_zip_file(self.feed_path, name)
                data[remove_ext(name)] = contents
                requirements_met = True
            except MissingReqFileError:
                data[remove_ext(name)] = StringIO()

        # At least one of the conditionally required files is necessary.
        if requirements_met:
            self.feed = Feed(self.feed_path, data)
            return self.feed

        raise MissingCReqFileError(zip_path=self.feed_path,
                                   files=cond_req_names)


class MissingReqFileError(Exception):
    """ Raised, when a GTFS-feed does not contain a required file. """
    def __init__(self, **kwargs) -> None:
        if "zip_path" not in kwargs or "file_name" not in kwargs:
            super().__init__()
            return
        self.zip_path = kwargs["zip_path"]
        self.file_name = kwargs["file_name"]
        msg = (f"The given GTFS feed '{self.zip_path}' does not contain the "
               f"required file '{self.file_name}'.")
        super().__init__(msg)


class MissingCReqFileError(Exception):
    """ Raised, when a GTFS-feed contains none of the conditionally
    required files. """
    def __init__(self, **kwargs) -> None:
        if "zip_path" not in kwargs or "files" not in kwargs:
            super().__init__()
            return
        self.zip_path = kwargs["zip_path"]
        self.files = kwargs["files"]
        msg = (f"The given GTFS feed '{self.zip_path}' contains none of "
               f"the conditionally required files ([{self.files}]).")
        super().__init__(msg)
