from abc import ABC, abstractmethod
from Proces import Proces
from typing import List


class Strategia(ABC):
    @property
    @abstractmethod
    def zmiana_procesu_w_trakcie_trwania_innego(self) ->bool:
        raise NotImplementedError
    @abstractmethod
    def wybierz_nastepny_proces(self, kolejka: List[Proces], czas_dzialanie: int) -> Proces:
        pass

    @abstractmethod
    def wykonuj_proces(self, proces: Proces, delta_t: int) -> Proces:
        pass

    def __repr__(self):
        return self.__class__.__name__
