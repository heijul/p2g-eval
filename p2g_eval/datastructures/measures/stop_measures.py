from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from p2g_eval.datastructures.measures.base_measure import BaseMeasure

if TYPE_CHECKING:
    from p2g_eval.datastructures.gtfs.stop import Stop


class StopMeasure(BaseMeasure, ABC):
    """ Base class for all measures about stops. """
    pass


class StopLocMeasure(StopMeasure):
    """ Uses the distance to calculate the quality of a stops' location. """
    @property
    def name(self) -> str:
        return "Stop location distance"

    def calculate(self, stop1: Stop, stop2: Stop) -> StopLocMeasure:
        """ Calculate the value. If the distance is below 10 meters,
        set it to 0 instead"""
        self.value = stop1.loc.distance(stop2.loc)
        if self.value <= 10:
            self.value = 0
        return self


class StopMeasures:
    """ A container for multiple stop measures, all using one ground truth. """
    def __init__(self, ground_truth: Stop) -> None:
        self.ground_truth = ground_truth
        self.measures = [StopLocMeasure]

    def calculate(self, stop: Stop) -> list[StopMeasure]:
        results = []
        for measure_cls in self.measures:
            measure = measure_cls()
            measure.calculate(self.ground_truth, stop)
            results.append(measure)
        return results
