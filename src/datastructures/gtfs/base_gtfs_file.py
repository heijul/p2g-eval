from __future__ import annotations

from abc import ABC, abstractmethod
from io import StringIO
from typing import TYPE_CHECKING

import pandas as pd


if TYPE_CHECKING:
    from src.datastructures.measures.base_measure import BaseMeasure


class BaseGTFSObject(ABC):
    """ Base class for objects of files contained in a GTFS feed. """
    fields: list[str] = []

    def __init__(self, *_) -> None:
        pass

    @classmethod
    def from_series(cls, series: pd.Series) -> BaseGTFSObject:
        """ Returns an object containing the defining values. """
        return cls(*list(series[cls.fields]))

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> list[BaseGTFSObject]:
        return [cls(*v) for v in df[cls.fields].values]

    @classmethod
    def from_buffer(cls, buffer: StringIO) -> list[BaseGTFSObject]:
        # noinspection PyTypeChecker
        return cls.from_df(pd.read_csv(buffer))

    @abstractmethod
    def calculate_measures(
            self, ground_truth: BaseGTFSObject) -> list[BaseMeasure]:
        """ Calculates all measures of the given GTFSObject. """
        pass
