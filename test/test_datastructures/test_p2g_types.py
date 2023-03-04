from unittest import TestCase

from src.datastructures.p2g_types import Date, Location, Time


class TestTime(TestCase):
    def test_time(self) -> None:
        time = Time(12, 30, 22)
        self.assertEqual(12, time.hours)
        self.assertEqual(30, time.minutes)
        self.assertEqual(22, time.seconds)

    def test_from_str(self) -> None:
        time = Time(25, 30, 1)
        time1 = Time.from_str("25:30:01")
        time2 = Time.from_str("25:30:1")
        self.assertEqual(time.hours, time1.hours)
        self.assertEqual(time.minutes, time1.minutes)
        self.assertEqual(time.seconds, time1.seconds)

        self.assertEqual(time.hours, time2.hours)
        self.assertEqual(time.minutes, time2.minutes)
        self.assertEqual(time.seconds, time2.seconds)
        # Invalid times
        inval_time_strs = ["", "25:30.33", "25:30"]
        for i, inval_time_str in enumerate(inval_time_strs):
            with (self.subTest(i=i), self.assertRaises(ValueError)):
                Time.from_str(inval_time_str)


class TestDate(TestCase):
    def test_date(self) -> None:
        date = Date(2023, 10, 4)
        self.assertEqual(2023, date.year)
        self.assertEqual(10, date.month)
        self.assertEqual(4, date.day)

    def test_from_str(self) -> None:
        date = Date(2023, 10, 4)
        date1 = Date.from_str("2023104")
        date2 = Date.from_str("20231004")
        self.assertEqual(date.year, date1.year)
        self.assertEqual(date.month, date1.month)
        self.assertEqual(date.day, date1.day)
        self.assertEqual(date.year, date2.year)
        self.assertEqual(date.month, date2.month)
        self.assertEqual(date.day, date2.day)
        # Invalid date
        inval_date_strs = ["", "2O23104", "04102023", "20230229"]
        for i, inval_date in enumerate(inval_date_strs):
            with (self.subTest(i=i), self.assertRaises(ValueError)):
                Date.from_str(inval_date)


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
