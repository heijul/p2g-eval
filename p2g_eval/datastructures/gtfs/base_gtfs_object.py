from __future__ import annotations

import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from io import StringIO
from typing import Any, ClassVar, Iterator, Type, TYPE_CHECKING

import pandas as pd
from pandas.errors import EmptyDataError


if TYPE_CHECKING:
    from p2g_eval.datastructures.measures.base_measure import BaseMeasure


class GTFSObjectList:
    def __init__(self, objects: list[BaseGTFSObject]) -> None:
        self.objects: list[BaseGTFSObject] = objects

    @functools.cached_property
    def id_map(self) -> dict[str: BaseGTFSObject]:
        return {obj.id: obj for obj in self.objects}

    def __iter__(self) -> Iterator:
        yield from self.objects

    def __len__(self) -> int:
        return self.objects.__len__()

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        if len(self) != len(other):
            return False
        for left, right in zip(self, other):
            if left != right:
                return False
        return True


@dataclass(init=False)
class BaseGTFSObject(ABC):
    list_type: ClassVar[Type[GTFSObjectList]] = GTFSObjectList

    def __init__(self, *_) -> None:
        """ Base class for objects from files contained in a GTFS feed. """
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @classmethod
    def field_names(cls) -> list[str]:
        return [field.name for field in fields(cls)]

    @classmethod
    def from_series(cls, series: pd.Series) -> BaseGTFSObject:
        """ Returns an object containing the defining values. """
        return cls(*list(series[cls.field_names()]))

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> GTFSObjectList:
        return cls.list_type([cls(*v) for v in df[cls.field_names()].values])

    @classmethod
    def from_buffer(cls, buffer: StringIO) -> GTFSObjectList:
        try:
            # noinspection PyTypeChecker
            return cls.from_df(pd.read_csv(buffer, dtype=str))
        except EmptyDataError:
            return GTFSObjectList([])

    @abstractmethod
    def calculate_measures(
            self, ground_truth: BaseGTFSObject) -> list[BaseMeasure]:
        """ Calculates all measures of the given GTFSObject. """
        pass

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        for field in self.field_names():
            if getattr(self, field) != getattr(other, field):
                return False
        return True
