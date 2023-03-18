from StrategieAlgorytmy.Strategia import Strategia


class FCFS(Strategia):
    @property

    def zmiana_procesu_w_trakcie_trwania_innego(self) ->bool:
        return False
    def wybierz_nastepny_proces(self, kolejka, czas_dzialania):
        if kolejka:
            proces = kolejka[0]
            if proces.moment_zgloszenia <= czas_dzialania:
                return proces
        return None

    def wykonuj_proces(self, proces, delta_t):
        proces.czas_pozostaly_do_konca_realizacji -= 1
