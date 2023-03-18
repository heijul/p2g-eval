from unittest import TestCase

from p2g_eval.config.config import P2GConfig
from p2g_eval.entity_mapper.base_entity_mapper import StopEntityMapper
from p2g_eval.in_out.feed_reader import BaseFeedReader
from test import TEST_DATA_DIR


class TestStopEntityMapper(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        feed1_path = TEST_DATA_DIR.joinpath("vag.zip")
        cls.feed1 = BaseFeedReader(feed1_path).read()
        feed2_path = TEST_DATA_DIR.joinpath("p2g_vag_1.zip")
        cls.feed2 = BaseFeedReader(feed2_path).read()

    def test_map_naive(self) -> None:
        mapper = StopEntityMapper(self.feed2, self.feed2)
        c = P2GConfig()
        c.stop_mapping = TEST_DATA_DIR.joinpath(
            "stop_mapping-p2g_vag_1-p2g_vag_1.csv")
        mapping = mapper.map_naive()
        self.assertTrue(22, len(mapping))
        manual_map = mapper.map_manual(c.stop_mapping).mapping
        self.assertEqual(manual_map, mapping.mapping)

    def test_map_manual(self) -> None:
        mapper = StopEntityMapper(self.feed1, self.feed2)
        c = P2GConfig()
        c.stop_mapping = TEST_DATA_DIR.joinpath(
            "stop_mapping-vag-p2g_vag_1.csv")
        mapping = mapper.map_manual(c.stop_mapping)
        self.assertTrue(22, len(mapping))
        for i, ((l1, r1), (l2, r2)) in enumerate(zip(c.stop_mapping, mapping)):
            with self.subTest(i=i):
                self.assertEqual(l1, l2.stop_id)
                self.assertEqual(r1, r2.stop_id)
