from StrategieAlgorytmy.Strategia import Strategia


class RR(Strategia):
    indeks = -1
    kwant_czasu=2

    @property
    def zmiana_procesu_w_trakcie_trwania_innego(self) ->bool:
        return True

    def wybierz_nastepny_proces(self, kolejka, czas_dzialania):
        self.indeks+=1
        if self.indeks >= len(kolejka):
            self.indeks = 0
        proces = kolejka[self.indeks]
        while proces.moment_zgloszenia>czas_dzialania:
            self.indeks += 1
            if self.indeks >= len(kolejka):
                self.indeks = 0
            proces = kolejka[self.indeks]
        return proces

    def wykonuj_proces(self, proces, delta_t):
        pass

