""" Test the entity mapping functions and classes. """

from unittest import TestCase

from p2g_eval.config.config import P2GConfig
from p2g_eval.feed_mapper import FeedMapper
from p2g_eval.in_out.feed_reader import BaseFeedReader
from tests.utils import TEST_DATA_DIR


class TestBaseMapper(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        feed1_path = TEST_DATA_DIR.joinpath("vag.zip")
        cls.feed1 = BaseFeedReader(feed1_path).read()
        feed2_path = TEST_DATA_DIR.joinpath("p2g_vag_1.zip")
        cls.feed2 = BaseFeedReader(feed2_path).read()

    def test_map_stops(self) -> None:
        mapper = FeedMapper(self.feed1, self.feed2)
        config = P2GConfig()
        config.stop_mapping = TEST_DATA_DIR.joinpath(
            "stop_mapping-vag-p2g_vag_1.csv")
        mapper.map_stops(config.stop_mapping)
        mapping = mapper.mappings["stops"]
        self.assertEqual(22, len(mapping))
        for i, (true_stop_l, true_stop_r) in enumerate(config.stop_mapping):
            map_stop_l = mapper.feed1.stops.loc[mapping.iloc[i].stop1]
            map_stop_r = mapper.feed2.stops.loc[mapping.iloc[i].stop2]
            with self.subTest(i=i):
                self.assertEqual(true_stop_l, map_stop_l.stop_id)
                self.assertEqual(true_stop_r, map_stop_r.stop_id)

    def test_map_stops_sorted(self) -> None:
        # Test that the order of stops in the df does not change mapping.
        feed = self.feed1.copy()
        feed.stops = feed.stops.sort_values("stop_name")
        mapper = FeedMapper(feed, self.feed2)
        config = P2GConfig()
        config.stop_mapping = TEST_DATA_DIR.joinpath(
            "stop_mapping-vag-p2g_vag_1.csv")
        mapper.map_stops(config.stop_mapping)
        mapping = mapper.mappings["stops"]
        self.assertEqual(22, len(mapping))
        for i, (true_stop_l, true_stop_r) in enumerate(config.stop_mapping):
            map_stop_l = mapper.feed1.stops.loc[mapping.iloc[i].stop1]
            map_stop_r = mapper.feed2.stops.loc[mapping.iloc[i].stop2]
            with self.subTest(i=i):
                self.assertEqual(true_stop_l, map_stop_l.stop_id)
                self.assertEqual(true_stop_r, map_stop_r.stop_id)
