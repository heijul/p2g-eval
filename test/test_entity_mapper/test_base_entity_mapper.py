from unittest import TestCase

from p2g_eval.config.config import C
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

    def setUp(self) -> None:
        self.mapper = StopEntityMapper(self.feed1, self.feed2)

    def test_map_naive(self) -> None:
        mapping = self.mapper.map_naive()
        self.assertTrue(22, len(mapping))

    def test_map_manual(self) -> None:
        C.stop_mapping = TEST_DATA_DIR.joinpath("stop_mapping.csv")
        mapping = self.mapper.map_manual()
        self.assertTrue(22, len(mapping))
