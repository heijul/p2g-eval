import sys

from p2g_eval.config.config import C
from p2g_eval.feed_mapper import FeedMapper
from p2g_eval.evaluate import Evaluator
from p2g_eval.in_out.arg_parser import parse_args


def main() -> None:
    """ Evaluates a given GTFS feed based on another given GTFS-feed. """
    C.load_args_dict(parse_args(sys.argv))
    mapper = FeedMapper(C.true_feed, C.test_feed)
    mapper.map()
    evaluator = Evaluator(mapper)
    evaluator.evaluate()


if __name__ == "__main__":
    main()
