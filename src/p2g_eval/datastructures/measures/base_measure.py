from abc import ABC, abstractmethod


class BaseMeasure(ABC):
    def __init__(self, value_fmt: str = "5> .2f") -> None:
        self._value = -1
        self.value_fmt = value_fmt

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value

    @abstractmethod
    def calculate(self, **kwargs) -> None:
        pass

    def to_output(self) -> str:
        """ Turns the value of the measure into a string. """
        return f"{self.name} {self.value:{self.value_fmt}}"
