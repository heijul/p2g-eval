from unittest import TestCase

from src.datastructures.location import Location


class TestLocation(TestCase):
    def test_location(self) -> None:
        loc = Location(48.113, 8.778)
        self.assertEqual(48.113, loc.lat)
        self.assertEqual(8.778, loc.lon)

    def test_distance(self) -> None:
        loc1 = Location(48.013407087440704, 7.835135607634816)
        loc2 = Location(47.99289635932313, 7.8494373607693)
        self.assertEqual(2517, loc1.distance(loc2))
        self.assertEqual(loc1.distance(loc2), loc2.distance(loc1))
        loc1.lat = 48
        loc2.lat = 49
        loc2.lon = loc1.lon
        self.assertEqual(111200, loc1.distance(loc2))

