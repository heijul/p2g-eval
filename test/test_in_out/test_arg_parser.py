from contextlib import redirect_stderr
from os import devnull
from unittest import TestCase

from p2g_eval.in_out import arg_parser as ap


class TestArgParser(TestCase):
    def test_parse_args(self) -> None:
        with (self.assertRaises(SystemExit),
              open(devnull, "w") as fnull,
              redirect_stderr(fnull)):
            ap.parse_args([])

        truth = {"ground_truth": "test.zip", "eval_feed": "eval.zip"}
        # First arg is the commandline command and can be ignored.
        args = ["", "test.zip", "eval.zip"]
        self.assertDictEqual(truth, ap.parse_args(args))
        # No checks about filetype.
        args[1] = "test.txt"
        truth["ground_truth"] = "test.txt"
        self.assertDictEqual(truth, ap.parse_args(args))
