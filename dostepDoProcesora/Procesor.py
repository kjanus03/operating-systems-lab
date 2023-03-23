from typing import Type

from Proces import Proces
from StrategieAlgorytmy.Strategia import Strategia


class Procesor:
    delta_t = 1

    def __init__(self, algorytm_kolejkowania: Type[Strategia], kolejka=None):
        if kolejka is None:
            kolejka = []
        self.kolejka = kolejka
        self.__algorytm_kolejkowania = algorytm_kolejkowania()
        self.__aktualnie_wykonywany = None
        # kolejka procesow oczekujacych
        self.czas_dzialania = 0
        self.procesy_wykonane = []
        # liczba zmian pomiedzy zadaniami
        self.zmiany_zadan = 0
        self.liczba_obsl_zadan = 0
        self.wydajnosc = None

    @property
    def algorytm_kolejkowania(self) -> Strategia:
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
        self.aktualnie_wykonywany.czas_trwania_realizacji -= 1
        self.aktualnie_wykonywany.status = "zakonczony"
        self.procesy_wykonane.append(self.aktualnie_wykonywany)
        self.kolejka.remove(self.aktualnie_wykonywany)
        self.aktualnie_wykonywany.czas_od_zgloszenia_do_ukonczenia = self.czas_dzialania - self.aktualnie_wykonywany.moment_zgloszenia
        self.aktualnie_wykonywany = None
        self.liczba_obsl_zadan += 1
        self.wydajnosc = self.liczba_obsl_zadan / self.czas_dzialania

    def wyczysc_kolejke(self):
        self.kolejka = []

    def wyswietl_procesy_wykonane(self):
        print(self.procesy_wykonane)

    def wybierz_proces(self):
        poprzedni = self.aktualnie_wykonywany
        self.aktualnie_wykonywany = self.algorytm_kolejkowania.wybierz_nastepny_proces(self.kolejka,
                                                                                       self.czas_dzialania)
        if self.aktualnie_wykonywany != poprzedni:
            self.zmiany_zadan += 1
            if (self.aktualnie_wykonywany.status == "nowy"):
                self.aktualnie_wykonywany.czas_oczekiwania_na_rozpoczecie = self.czas_dzialania - self.aktualnie_wykonywany.moment_zgloszenia
            self.aktualnie_wykonywany.status = "wykonywany"

    def wykonaj_jednostke_czasu(self):
        self.czas_dzialania += self.delta_t

        if self.aktualnie_wykonywany is None and self.kolejka:
            self.wybierz_proces()
        if self.aktualnie_wykonywany is not None:
            self.aktualnie_wykonywany.czas_pozostaly_do_konca_realizacji = self.aktualnie_wykonywany.dlugosc_fazy_procesora - self.aktualnie_wykonywany.czas_trwania_realizacji
            self.aktualnie_wykonywany.czas_trwania_realizacji += self.delta_t

            if self.aktualnie_wykonywany.czas_pozostaly_do_konca_realizacji == 0:
                self.proces_zakonczony()
        if self.algorytm_kolejkowania.zmiana_procesu_w_trakcie_trwania_innego:
            self.wybierz_proces()

    def wykonaj_jednostke_czasu_RR(self):
        self.czas_dzialania += self.delta_t
        if self.aktualnie_wykonywany is None and self.kolejka:
            self.wybierz_proces()
        self.aktualnie_wykonywany.czas_pozostaly_do_konca_realizacji = self.aktualnie_wykonywany.dlugosc_fazy_procesora - self.aktualnie_wykonywany.czas_trwania_realizacji
        self.aktualnie_wykonywany.czas_trwania_realizacji += self.delta_t

        if self.aktualnie_wykonywany.czas_pozostaly_do_konca_realizacji <= 0:
            self.proces_zakonczony()

        elif self.kolejka and self.aktualnie_wykonywany.czas_pozostaly_do_konca_realizacji % self.algorytm_kolejkowania.kwant_czasu == 0:
            self.wybierz_proces()

    def __repr__(self):
        return (f'Aktualnie wykonywany proces: {self.aktualnie_wykonywany}\n'
                f'Aktualna kolejka: {self.kolejka}\n'
                f'Aktualna dlugosc kolejki: {len(self.kolejka)}\n'
                f'Aktualny algorytm kolejkowania: {self.__algorytm_kolejkowania}\n'
                f'Czas dzialania procesora: {self.czas_dzialania}'
                )
