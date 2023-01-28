from contextlib import redirect_stderr
from os import devnull
from unittest import TestCase

from src.in_out import arg_parser as ap


class TestArgParser(TestCase):
    def test_parse_args(self) -> None:
        with (self.assertRaises(SystemExit),
              open(devnull, "w") as fnull,
              redirect_stderr(fnull)):
            ap.parse_args([])

        truth = {"test_feed": "test.zip", "eval_feed": "eval.zip"}
        args = ["test.zip", "eval.zip"]
        self.assertDictEqual(truth, ap.parse_args(args))
        # No checks about filetype.
        args[0] = "test.txt"
        truth["test_feed"] = "test.txt"
        self.assertDictEqual(truth, ap.parse_args(args))
