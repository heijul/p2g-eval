from unittest import TestCase

import custom_conf.errors as err
from custom_conf.properties.property import Property

from p2g_eval.config.config import P2GConfig
from p2g_eval.in_out.feed_reader import BaseFeedReader
from test import TEST_DATA_DIR


class TestP2GConfig(TestCase):
    def test_p2g_config(self) -> None:
        c = P2GConfig()

        for var in vars(c):
            prop = object.__getattribute__(c, var)
            if not isinstance(prop, Property):
                continue
            self.assertEqual(var, prop.name)
        for i, prop in enumerate(c.properties):
            self.assertTrue(isinstance(prop, Property))
            with (self.subTest(i=i),
                  self.assertRaises(err.MissingRequiredPropertyError)):
                _ = getattr(c, prop.name)

    def test_default_config_path(self) -> None:
        c = P2GConfig()
        self.assertTrue(c.default_config_path.exists())

    def test_load_args_dict(self) -> None:
        ground_truth = BaseFeedReader(TEST_DATA_DIR.joinpath("vag.zip")).read()
        eval_feed_path = TEST_DATA_DIR.joinpath("p2g_vag_1.zip")
        stop_mapping = TEST_DATA_DIR.joinpath("stop_mapping.csv")
        values = {"eval_feed": eval_feed_path,
                  "ground_truth": ground_truth,
                  "stop_mapping": stop_mapping}
        c = P2GConfig()
        c.load_args_dict(values)
        self.assertEqual(id(ground_truth), id(c.ground_truth))
        eval_feed = BaseFeedReader(eval_feed_path).read()
        self.assertTrue(eval_feed == c.eval_feed)
        self.assertNotEqual(id(eval_feed), id(c.eval_feed))
        with open(stop_mapping) as fil:
            contents = fil.read()
        mapping = [tuple(line.split(",")) for line in contents.split("\n")[1:]]
        self.assertEqual(mapping, mapping)
