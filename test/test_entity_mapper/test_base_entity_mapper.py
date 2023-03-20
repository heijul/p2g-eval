from unittest import TestCase

from p2g_eval.config.config import P2GConfig
from p2g_eval.entity_mapper.dataframe_mapper import BaseMapper
from p2g_eval.in_out.feed_reader import BaseFeedReader
from test import TEST_DATA_DIR


class TestBaseMapper(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        feed1_path = TEST_DATA_DIR.joinpath("vag.zip")
        cls.feed1 = BaseFeedReader(feed1_path).read()
        feed2_path = TEST_DATA_DIR.joinpath("p2g_vag_1.zip")
        cls.feed2 = BaseFeedReader(feed2_path).read()

    def test_map_stops(self) -> None:
        mapper = BaseMapper(self.feed1, self.feed2)
        c = P2GConfig()
        c.stop_mapping = TEST_DATA_DIR.joinpath(
            "stop_mapping-vag-p2g_vag_1.csv")
        mapper.map_stops(c.stop_mapping)
        mapping = mapper.mappings["stops"]
        self.assertTrue(22, len(mapping))
        # TODO: Test order
        for i, (l1, r1) in enumerate(c.stop_mapping):
            l2 = mapper.feed1.stops.iloc[mapping.loc[i].stop1]
            r2 = mapper.feed2.stops.iloc[mapping.loc[i].stop2]
            with self.subTest(i=i):
                self.assertEqual(l1, l2.stop_id)
                self.assertEqual(r1, r2.stop_id)
