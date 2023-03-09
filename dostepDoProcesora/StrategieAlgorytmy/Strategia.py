from abc import ABC, abstractmethod
from Proces import Proces


class Strategia(ABC):
    @abstractmethod
    def wybierz_nastepny_proces(self, kolejka) -> Proces:
        pass

    def __repr__(self):
        return self.__class__.__name__
