from __future__ import annotations

from typing import Type

import pandas as pd


class BaseGTFSFile:
    fields: list[str] = []

    def __init__(self, *_) -> None:
        pass

    @classmethod
    def from_series(cls, series: pd.Series) -> BaseGTFSFile:
        """ Returns a Stop containing the defining values. """
        return cls(*list(series[cls.fields]))

    @staticmethod
    def from_df(cls, df: pd.DataFrame) -> list[Type[BaseGTFSFile]]:
        return [cls(*v) for v in df[cls.fields].values]
