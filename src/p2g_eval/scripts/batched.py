import sys
import traceback
from argparse import ArgumentParser
from glob import glob
from pathlib import Path

from p2g_eval.main import main


def run_all():
    batch_args = batch_parse_args().parse_args()
    ground_truth = Path(batch_args.ground_truth).resolve(strict=True)
    assert ground_truth.exists(), "Ground truth is missing"
    feed_dir = Path(batch_args.feed_directory).resolve(strict=True)
    msg = "Feed dir is missing or not a directory"
    assert feed_dir.exists() and feed_dir.is_dir(), msg
    out_dir = feed_dir.joinpath("out")
    if not out_dir.exists():
        out_dir.mkdir()
    results = []
    for filepath in glob("*.zip", root_dir=feed_dir):
        feed = feed_dir.joinpath(filepath)
        if feed == ground_truth:
            continue
        mapping = feed.with_name(feed.stem + ".csv")
        if not mapping.exists():
            print(f"Could not find mapping for '{feed.name}'.")
            continue
        sys.argv = ["p2g-eval", "-s", str(mapping),
                    str(ground_truth), str(feed)]
        print(f"Evaluating {feed.name}...", end=" ")
        try:
            results.append(main(True))
            print("Done. No errors occurred.")
        except Exception as e:
            log_file = out_dir.joinpath(feed.stem + ".log")
            with open(log_file, "w") as fil:
                traceback.print_exception(e, file=fil)
            print(f"Errors occurred. See the log file '{log_file.name}'.")
    with open(out_dir.joinpath("results"), "w") as fil:
        fil.write("\n".join(results) + "\n")


def batch_parse_args() -> ArgumentParser:
    """ Argument parser for the batchmode. """
    parser = ArgumentParser("p2g-eval-batch")
    text = "The path to the ground truth feed."
    parser.add_argument("ground_truth", type=str, help=text)
    text = ("The directory that contains the GTFS feeds and the mappings. "
            "Each mapping must have the same base name as the feed it maps.")
    parser.add_argument("feed_directory", type=str, help=text)
    return parser


if __name__ == "__main__":
    run_all()
