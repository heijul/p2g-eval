from unittest import TestCase

from src.datastructures.gtfs.stop import Stop


class TestStop(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.file_path = "../../testdata/stops.txt"

    def test_from_values(self) -> None:
        stops = []
        with open(self.file_path, "w") as file:
            header = [h.strip() for h in file.readline().split(";")]
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue
                values = [v.strip() for v in line.split(";")]
                stops.append(Stop.from_values(header, values))
        self.assertEqual("de:08311:30300:0:1", stops[0].id)
        self.assertEqual("Freiburg, Laßbergstraße", stops[0].name)
        self.assertEqual("47.9844905384561", stops[0].loc.lat)
        self.assertEqual("7.89366708256103", stops[0].loc.lon)


