from typing import Type

from Proces import Proces
from StrategieAlgorytmy.Strategia import Strategia


class Procesor:
    delta_t = 1
    def __init__(self, algorytm_kolejkowania: Type[Strategia], kolejka=None):
        if kolejka is None:
            kolejka = []
        self.kolejka = kolejka
        self.__algorytm_kolejkowania = algorytm_kolejkowania
        self.__aktualnie_wykonywany = None
        # kolejka procesow oczekujacych
        self.czas_dzialania = 0
        self.procesy_wykonane = []
        #liczba zmian pomiedzy zadaniami
        self.zmiany_zadan = 0
        self.liczba_obsl_zadan = len(self.procesy_wykonane)

    @property
    def algorytm_kolejkowania(self) -> Type[Strategia]:
        return self.__algorytm_kolejkowania

    @algorytm_kolejkowania.setter
    def algorytm_kolejkowania(self, algorytm_kolejkownia: Type[Strategia]):
        self.__algorytm_kolejkowania = algorytm_kolejkownia

    @property
    def aktualnie_wykonywany(self) -> Proces:
        return self.__aktualnie_wykonywany

    @aktualnie_wykonywany.setter
    def aktualnie_wykonywany(self, aktualnie_wykonywany: Proces):
        self.__aktualnie_wykonywany = aktualnie_wykonywany

    def dodaj_proces(self, proces: Proces):
        proces.zglos(self.czas_dzialania)
        self.kolejka.append(proces)

    def proces_zakonczony(self):
        self.aktualnie_wykonywany.status = "zakonczony"
        self.procesy_wykonane.append(self.aktualnie_wykonywany)
        self.aktualnie_wykonywany = None


    def wyczysc_kolejke(self):
        self.kolejka = []

    def wyswietl_procesy_wykonane(self):
        print(self.procesy_wykonane)

    # def przetworz_kolejke_jednokrotnie(self):
    #     print("Przetwarzam kolejke...")
    #     proces = self.algorytm_kolejkowania().wybierz_nastepny_proces(kolejka=self.kolejka)
    #     proces.status = "wykonywany"
    #     proces.czas_oczekiwania = self.czas_dzialania - proces.moment_zgloszenia
    #     self.czas_dzialania += proces.dlugosc_fazy_procesora
    #     self.usun_proces_zakonczony(proces)

    def wykonaj_jednostke_czasu(self):
        self.czas_dzialania += self.delta_t
        print(f'Mija {self.delta_t} jednostek czasu')
        if self.aktualnie_wykonywany is None:
            self.aktualnie_wykonywany = self.algorytm_kolejkowania().wybierz_nastepny_proces(self.kolejka)
            self.aktualnie_wykonywany.status = "wykonywanny"
            self.aktualnie_wykonywany.czas_trwania_realizacji = 0
            self.aktualnie_wykonywany.czas_oczekiwania_na_rozpoczecie = self.czas_dzialania - self.aktualnie_wykonywany.moment_zgloszenia

        self.aktualnie_wykonywany.czas_pozostaly_do_konca_realizacji = self.aktualnie_wykonywany.dlugosc_fazy_procesora - self.aktualnie_wykonywany.czas_trwania_realizacji
        self.aktualnie_wykonywany.czas_trwania_realizacji += self.delta_t
        if self.aktualnie_wykonywany.czas_pozostaly_do_konca_realizacji == 0:
            self.proces_zakonczony()



    def __repr__(self):
        return (f'Aktualnie wykonywany proces: {self.aktualnie_wykonywany}\n' 
                f'Aktualna kolejka: {self.kolejka}\n'
                f'Aktualna dlugosc kolejki: {len(self.kolejka)}\n'
                f'Aktualny algorytm kolejkowania: {self.__algorytm_kolejkowania()}\n'
                f'Czas dzialania procesora: {self.czas_dzialania}')
