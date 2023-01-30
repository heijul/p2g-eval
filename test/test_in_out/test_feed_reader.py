from unittest import TestCase

from src.in_out.feed_reader import BaseFeedReader
from test import TEST_DIR


class TestFeedReader(TestCase):
    def test_read(self) -> None:
        feed_reader = BaseFeedReader(TEST_DIR.joinpath("testdata/vag.zip"))
        feed = feed_reader.read()
        self.assertEqual(1002, len(feed.stops))
