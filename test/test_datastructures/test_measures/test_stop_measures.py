from unittest import TestCase

from p2g_eval.datastructures.measures.stop_measures import StopLocMeasure


class TestStopLocMeasure(TestCase):
    def test_calculate(self) -> None:
        from p2g_eval.datastructures.gtfs.stop import Stop

        m = StopLocMeasure()
        stop1 = Stop("stop1", "stop1", 48.07773, 7.8889)
        stop2 = Stop("stop2", "stop2", 48.07772, 7.8889)
        m.calculate(stop1, stop2)
        self.assertEqual(0, m.value)

    def test_to_output(self) -> None:
        m = StopLocMeasure()
        self.assertEqual("Stop location distance: -1.00", m.to_output())
        m.value = 1/3
        self.assertEqual("Stop location distance:  0.33", m.to_output())
