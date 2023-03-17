from StrategieAlgorytmy.Strategia import Strategia


class SJF(Strategia):
    def zmiana_procesu_w_trakcie_trwania_innego(self) ->bool:
        return False
    def wybierz_nastepny_proces(self, kolejka):
        if kolejka:
            proces = min(kolejka, key=lambda x: x.czas_pozostaly_do_konca_realizacji)
            return proces
        else:
            return None

    def wykonuj_proces(self, proces, delta_t):
        pass
