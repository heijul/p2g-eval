""" Some utils used by multiple different tests. """

from pathlib import Path

TEST_DIR = Path(__file__).parent
TEST_DATA_DIR = TEST_DIR.joinpath("testdata")
