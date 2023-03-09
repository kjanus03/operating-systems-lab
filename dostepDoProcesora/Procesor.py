from typing import Type

from Proces import Proces
from StrategieAlgorytmy.Strategia import Strategia


class Procesor:
    def __init__(self, algorytm_kolejkowania: Type[Strategia], kolejka=None):
        if kolejka is None:
            kolejka = []
        self.kolejka = kolejka
        self.__algorytm_kolejkowania = algorytm_kolejkowania
        # kolejka procesow oczekujacych
        self.czas_dzialania = 0
        self.procesy_wykonane = []

    @property
    def algorytm_kolejkowania(self) -> Type[Strategia]:
        return self.__algorytm_kolejkowania

    @algorytm_kolejkowania.setter
    def algorytm_kolejkowania(self, algorytm_kolejkownia: Type[Strategia]):
        self.__algorytm_kolejkowania = algorytm_kolejkownia

    def dodaj_proces(self, proces: Proces):
        proces.zglos(self.czas_dzialania)
        self.kolejka.append(proces)

    def usun_proces_zakonczony(self, proces: Proces):
        self.kolejka.remove(proces)
        self.procesy_wykonane.append(proces)
        proces.status = "zakonczony"

    def wyczysc_kolejke(self):
        self.kolejka = []

    def wyswietl_procesy_wykonane(self):
        print(self.procesy_wykonane)

    def przetworz_kolejke_jednokrotnie(self):
        print("Przetwarzam kolejke...")
        proces = self.algorytm_kolejkowania().wybierz_nastepny_proces(kolejka=self.kolejka)
        proces.status = "wykonywany"
        proces.czas_oczekiwania = self.czas_dzialania - proces.moment_zgloszenia
        self.czas_dzialania += proces.dlugosc_fazy_procesora
        self.usun_proces_zakonczony(proces)

    def __repr__(self):
        return (f'Aktualna kolejka: {self.kolejka}\n'
                f'Aktualna dlugosc kolejki: {len(self.kolejka)}\n'
                f'Aktualny algorytm kolejkowania: {self.__algorytm_kolejkowania()}\n'
                f'Czas dzialania procesora: {self.czas_dzialania}')
