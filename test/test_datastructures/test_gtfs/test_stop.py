from unittest import TestCase
import pandas as pd

from src.datastructures.gtfs.stop import Stop

from test import TEST_DIR


class TestStop(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.file_path = TEST_DIR.joinpath("testdata/stops_vag.txt")

    def test_from_series(self) -> None:
        df = pd.read_csv(self.file_path)
        stop = Stop.from_series(df.iloc[0])
        self.assertEqual("de:08311:30300:0:1", stop.id)
        self.assertEqual("Freiburg, Laßbergstraße", stop.name)
        self.assertEqual(47.9844905384561, stop.loc.lat)
        self.assertEqual(7.89366708256103, stop.loc.lon)
