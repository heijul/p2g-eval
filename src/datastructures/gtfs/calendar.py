from __future__ import annotations

from dataclasses import dataclass

from src.datastructures.gtfs.base_gtfs_object import BaseGTFSObject


@dataclass
class Calendar(BaseGTFSObject):
    service_id: str
    mon: bool
    tue: bool
    wed: bool
    thu: bool
    fri: bool
    sat: bool
    sun: bool

    def calculate_measures(self, ground_truth: Calendar) -> list[Calendar]:
        pass
