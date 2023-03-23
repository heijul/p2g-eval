import sys

from p2g_eval.config.config import C
from p2g_eval.datastructures.gtfs.feed import Feed
from p2g_eval.datastructures.measures.stop_measures import StopLocMeasure
from p2g_eval.entity_mapper.base_entity_mapper import StopEntityMapper
from p2g_eval.entity_mapper.dataframe_mapper import BaseMapper
from p2g_eval.evaluate.evaluator import Evaluator
from p2g_eval.in_out.arg_parser import parse_args


def calculate_feed_measures(true_feed: Feed, test_feed: Feed) -> None:
    entity_mappings = {"stops": StopEntityMapper}
    measures = {"stops": [StopLocMeasure]}
    evaluated_measures = {}
    for field_name in test_feed.field_names:
        if field_name != "stops":
            continue
        mapping = entity_mappings.get(field_name)
        if not mapping or not measures[field_name]:
            continue
        evaluated_measures[field_name] = []
        mapping = mapping(true_feed, test_feed).map()
        for measure in measures[field_name]:
            measure = measure()
            print("\n" + measure.name)
            for true_entity, test_entity in mapping:
                evaluated = measure.calculate(true_entity, test_entity)
                evaluated_measures[field_name].append(evaluated)
                print(f"\t{test_entity.stop_name:<23}{evaluated.value:>6.0f}")


def main() -> None:
    """ Evaluates a given GTFS feed based on another given GTFS-feed. """
    C.load_args_dict(parse_args(sys.argv))
    mapper = BaseMapper(C.true_feed, C.test_feed)
    mapper.map()
    evaluator = Evaluator(mapper)
    evaluator.evaluate()


if __name__ == "__main__":
    main()
