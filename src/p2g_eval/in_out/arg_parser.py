""" Allows parsing of all the command line arguments. """

from argparse import ArgumentParser
from typing import Any


def parse_args(args: list[Any]) -> dict[str: Any]:
    """ Parse the cli args and return a dictionary containing the values. """
    desc = "Tool used to evaluate the output of pdf2gtfs."

    arg_parser = ArgumentParser(prog="python /path/to/p2g_eval/main.py",
                                description=desc)

    args_names = [("--stop_mapping", "-s"), ("true_feed",), ("test_feed",)]
    helps = [
        "A csv file, detailing the mapping between the stop of the two feeds.",
        "The GTFS feed that is used to evaluate the other feed.",
        "The GTFS feed that should be evaluated.",
        ]
    for arg_names, help_ in zip(args_names, helps):
        arg_parser.add_argument(*arg_names, help=help_)

    parsed_args = arg_parser.parse_args(args[1:])
    return {arg: getattr(parsed_args, arg)
            for arg in vars(parsed_args) if not arg.startswith("_")}
