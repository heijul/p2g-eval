""" Provides functions to evaluate a feed. """

from p2g_eval.feed_mapper import FeedMapper
from p2g_eval.measures import StopMeasure


class Evaluator:
    """
    Used to evaluate the feed, mapped to a ground truth by a FeedMapper.
    """
    def __init__(self, mapper: FeedMapper) -> None:
        self.mapper = mapper
        self._initialize_measures()

    def _initialize_measures(self) -> None:
        self.measures = {"stops": StopMeasure(self.mapper)}

    def evaluate_stops(self) -> None:
        """ Calculate the distance (min/max/mean/std) between mapped stops. """
        if not self.mapper.is_mapped:
            self.mapper.map()
        self.measures["stops"].calculate()

    def evaluate(self) -> None:
        """ Runs all defined evaluations. """
        self.evaluate_stops()

    def to_output(self) -> str:
        """ Output the evaluation results in a human-readable manner. """
        # Basic message about which feed was evaluated by which ground truth.
        lines = ["", "Evaluation complete.", "",
                 "Used ground truth",
                 f"\t{self.mapper.feed1.path.resolve()}",
                 "to evaluate the feed",
                 f"\t{self.mapper.feed2.path.resolve()}",
                 ""]
        for measure in self.measures.values():
            lines += [measure.to_output()]
        return "\n".join(lines)
