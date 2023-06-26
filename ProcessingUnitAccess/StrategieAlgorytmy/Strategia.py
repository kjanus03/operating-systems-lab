from abc import ABC, abstractmethod
from typing import List

from Proces import Proces


class Strategia(ABC):
    @property
    @abstractmethod
    def zmiana_procesu_w_trakcie_trwania_innego(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def wybierz_nastepny_proces(self, kolejka: List[Proces], czas_dzialanie: int) -> Proces:
        pass

    def __repr__(self):
        return self.__class__.__name__
