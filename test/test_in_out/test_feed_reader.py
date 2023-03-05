from pathlib import Path
from unittest import TestCase

from p2g_eval.in_out.feed_reader import BaseFeedReader
from test import TEST_DIR


class TestFeedReader(TestCase):
    def test_read(self) -> None:
        feed_reader = BaseFeedReader(TEST_DIR.joinpath("testdata/vag.zip"))
        feed = feed_reader.read()
        self.assertEqual(1002, len(feed.stops))

    def test_read_perm_fail(self) -> None:
        feed_reader = BaseFeedReader(Path("/var/log/private"))
        with self.assertRaises(PermissionError):
            feed_reader.read()

    def test_read_non_existant_path(self) -> None:
        # TODO: Should this fail upon creation instead of reading?
        feed_reader = BaseFeedReader(Path("/THISPATHDOESNOTEXIST"))
        with self.assertRaises(OSError):
            feed_reader.read()

    def test_read_missing_required_file(self) -> None:
        path = TEST_DIR.joinpath("testdata/vag_invalid.zip")
        feed_reader = BaseFeedReader(path)
        with self.assertRaises(KeyError):
            feed_reader.read()

    def test_read_missing_cond_req_file(self) -> None:
        path = TEST_DIR.joinpath("testdata/vag_no_calendar_dates.zip")
        feed_reader = BaseFeedReader(path)
        feed = feed_reader.read()
        self.assertEqual(0, len(feed.calendar_dates))
