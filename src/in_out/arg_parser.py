from argparse import ArgumentParser
from typing import Any


def parse_args(args: list[Any]) -> dict[str: Any]:
    """ Parse the args and return a dictionary containing the values. """
    desc = "Tool used to evaluate the output of pdf2gtfs."

    ap = ArgumentParser(prog="p2g-eval", description=desc)

    args_names = [("test_feed",), ("eval_feed",)]
    helps = ["The GTFS feed that should be evaluated.",
             "The GTFS feed that is used to evaluate other feeds.",
             ]
    for arg_names, help_ in zip(args_names, helps):
        ap.add_argument(*arg_names, help=help_)

    parsed_args = ap.parse_args(args)
    return {arg_names[0]: getattr(parsed_args, arg_names[0])
            for arg_names in args_names}
