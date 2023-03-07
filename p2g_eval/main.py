import sys

from p2g_eval.config.config import C
from p2g_eval.in_out.arg_parser import parse_args


def main() -> None:
    """ Evaluates a given GTFS feed based on another given GTFS-feed. """
    C.load_args_dict(parse_args(sys.argv))


if __name__ == "__main__":
    main()
