import sys

from config.config import C
from in_out.arg_parser import parse_args


def main() -> None:
    """ Evaluates a given GTFS feed based on another given GTFS-feed. """
    C.load_args(parse_args(sys.argv))


if __name__ == "__main__":
    main()
