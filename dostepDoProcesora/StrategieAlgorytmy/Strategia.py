from abc import ABC, abstractmethod
from Proces import Proces
from typing import List


class Strategia(ABC):
    @abstractmethod
    def wybierz_nastepny_proces(self, kolejka: List[Proces]) -> Proces:
        pass

    @abstractmethod
    def wykonuj_proces(self, proces: Proces, delta_t: int) -> Proces:
        pass

    def __repr__(self):
        return self.__class__.__name__
