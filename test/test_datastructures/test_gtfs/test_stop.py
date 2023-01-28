from unittest import TestCase
import pandas as pd

from src.datastructures.gtfs.stop import Stop

from test import TEST_DIR


class TestStop(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.truth_path = TEST_DIR.joinpath("testdata/stops_vag.txt")
        cls.test_path = TEST_DIR.joinpath("testdata/stops_vag_p2g.txt")

    def test_from_series(self) -> None:
        df = pd.read_csv(self.truth_path)
        stop = Stop.from_series(df.iloc[0])
        self.assertEqual("de:08311:30300:0:1", stop.id)
        self.assertEqual("Freiburg, Laßbergstraße", stop.name)
        self.assertEqual(47.9844905384561, stop.loc.lat)
        self.assertEqual(7.89366708256103, stop.loc.lon)

    def test_calculate_measures(self) -> None:
        df1 = pd.read_csv(self.truth_path)
        stop_num = 0
        ground_truth = Stop.from_series(df1.iloc[stop_num])
        df2 = pd.read_csv(self.test_path)
        stop = Stop.from_series(df2.iloc[stop_num])
        measures = stop.calculate_measures(ground_truth)
        self.assertEqual(1, len(measures))
        self.assertEqual(33, measures[0].value)

        stop_num = 3
        ground_truth = Stop.from_series(df1.iloc[stop_num])
        df2 = pd.read_csv(self.test_path)
        stop = Stop.from_series(df2.iloc[stop_num])
        measures = stop.calculate_measures(ground_truth)
        self.assertEqual(1, len(measures))
        self.assertEqual(0, measures[0].value)
