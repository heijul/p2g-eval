from io import StringIO
from unittest import TestCase

import pandas as pd

from p2g_eval.config.config import P2GConfig
from p2g_eval.feed import read_from_buffer
from p2g_eval.feed_mapper import FeedMapper
from p2g_eval.in_out.feed_reader import BaseFeedReader, read_zip_file
from test import TEST_DATA_DIR


class TestFeed(TestCase):
    def test_read_from_buffer(self) -> None:
        # Empty buffer does not result in an error.
        buffer = StringIO()
        df = read_from_buffer(buffer)
        self.assertTrue(df.empty)
        # Test reading actual data from a buffer.
        path = TEST_DATA_DIR.joinpath("p2g_vag_1.zip")
        stops_buffer = read_zip_file(path, "stops.txt")
        stops_buffer.seek(0)
        df = read_from_buffer(stops_buffer)
        self.assertEqual(22, len(df))
        # TODO: Improve this test

    def test_reduce_using_stops(self) -> None:
        c = P2GConfig()
        c.stop_mapping = TEST_DATA_DIR.joinpath(
            "stop_mapping-vag-p2g_vag_1.csv")
        feed1 = BaseFeedReader(TEST_DATA_DIR.joinpath("vag.zip")).read()
        feed2 = BaseFeedReader(TEST_DATA_DIR.joinpath("p2g_vag_1.zip")).read()
        mapper = FeedMapper(feed1, feed2)
        mapper.map_stops(c.stop_mapping)
        feed1.reduce_using_stops(mapper.mappings["stops"].stop1)
        self.assertEqual(22, len(feed1.stops))
        self.assertEqual(1, len(feed1.routes))
        # TODO: Completeness of routes, etc. using feed1.copy() beforehand.
        # All stops need to exist.
        with self.assertRaises(KeyError):
            feed1.reduce_using_stops(pd.Series(["this_id_does_not_exist"]))
        # TODO: Test this with more/different feeds + gtfs_files.
