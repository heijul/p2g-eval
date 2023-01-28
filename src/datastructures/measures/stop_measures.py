from datastructures.measures.base_measure import BaseMeasure
from datastructures.location import Location


class StopLocMeasure(BaseMeasure):
    """ Uses the distance as a measure to calculate the quality of a stops'
    location. """
    @property
    def name(self) -> str:
        return "Stop location distance"

    def calculate(self, loc1: Location, loc2: Location) -> None:
        """ Calculate the value. If the distance is below 10 meters,
        set it to 0 instead"""
        self.value = loc1.distance(loc2)
        if self.value <= 10:
            self.value = 0
