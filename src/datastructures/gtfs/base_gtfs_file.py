from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

import pandas as pd

from datastructures.measures.base_measure import BaseMeasure


class BaseGTFSObject(ABC):
    """ Base class for objects of files contained in a GTFS feed. """
    fields: list[str] = []

    def __init__(self, *_) -> None:
        pass

    @classmethod
    def from_series(cls, series: pd.Series) -> BaseGTFSObject:
        """ Returns an object containing the defining values. """
        return cls(*list(series[cls.fields]))

    @staticmethod
    def from_df(cls, df: pd.DataFrame) -> list[Type[BaseGTFSObject]]:
        return [cls(*v) for v in df[cls.fields].values]

    @abstractmethod
    def calculate_measures(
            self, ground_truth: BaseGTFSObject) -> list[BaseMeasure]:
        """ Calculates all measures of the given GTFSObject. """
        pass
