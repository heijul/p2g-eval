""" Test the argument parser. """

from contextlib import redirect_stderr
from os import devnull
from unittest import TestCase

from p2g_eval.in_out import arg_parser as ap


class TestArgParser(TestCase):
    def test_parse_args(self) -> None:
        with (self.assertRaises(SystemExit),
              open(devnull, "w", encoding="utf-8") as fnull,
              redirect_stderr(fnull)):
            ap.parse_args([])

        truth = {"true_feed": "true.zip", "test_feed": "tests.zip",
                 "stop_mapping": None}
        # First arg is the commandline command and can be ignored.
        args = ["", "true.zip", "tests.zip"]
        self.assertDictEqual(truth, ap.parse_args(args))
        # No checks about filetype.
        args[1] = "tests.txt"
        truth["true_feed"] = "tests.txt"
        self.assertDictEqual(truth, ap.parse_args(args))
