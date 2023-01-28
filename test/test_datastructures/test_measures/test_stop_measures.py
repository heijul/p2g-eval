from unittest import TestCase

from src.datastructures.location import Location
from src.datastructures.measures.stop_measures import StopLocMeasure


class TestStopLocMeasure(TestCase):
    def test_calculate(self) -> None:
        m = StopLocMeasure()
        loc1 = Location(48.07773, 7.8889)
        loc2 = Location(48.07772, 7.8889)
        m.calculate(loc1, loc2)
        self.assertEqual(0, m.value)

    def test_to_output(self) -> None:
        m = StopLocMeasure()
        self.assertEqual("Stop location distance: -1.00", m.to_output())
        m.value = 1/3
        self.assertEqual("Stop location distance:  0.33", m.to_output())

