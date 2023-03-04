from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from io import StringIO
from typing import TYPE_CHECKING

import pandas as pd
from pandas.errors import EmptyDataError


if TYPE_CHECKING:
    from src.datastructures.measures.base_measure import BaseMeasure


@dataclass(init=False)
class BaseGTFSObject(ABC):
    def __init__(self, *_) -> None:
        pass

    @classmethod
    def field_names(cls) -> list[str]:
        return [field.name for field in fields(cls)]

    """ Base class for objects of files contained in a GTFS feed. """
    @classmethod
    def from_series(cls, series: pd.Series) -> BaseGTFSObject:
        """ Returns an object containing the defining values. """
        return cls(*list(series[cls.field_names()]))

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> list[BaseGTFSObject]:
        return [cls(*v) for v in df[cls.field_names()].values]

    @classmethod
    def from_buffer(cls, buffer: StringIO) -> list[BaseGTFSObject]:
        try:
            # noinspection PyTypeChecker
            return cls.from_df(pd.read_csv(buffer))
        except EmptyDataError:
            return []

    @abstractmethod
    def calculate_measures(
            self, ground_truth: BaseGTFSObject) -> list[BaseMeasure]:
        """ Calculates all measures of the given GTFSObject. """
        pass
