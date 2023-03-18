from StrategieAlgorytmy.Strategia import Strategia


class SJF(Strategia):
    @property
    def zmiana_procesu_w_trakcie_trwania_innego(self) ->bool:
        return False
    def wybierz_nastepny_proces(self, kolejka, czas_dzialania):
        if kolejka:
            proces = min([proces1 for proces1 in kolejka if proces1.moment_zgloszenia<=czas_dzialania], key=lambda x: x.czas_pozostaly_do_konca_realizacji)
            return proces
        else:
            return None

    def wykonuj_proces(self, proces, delta_t):
        pass
