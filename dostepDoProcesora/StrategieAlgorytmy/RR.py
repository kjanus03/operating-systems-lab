from StrategieAlgorytmy.Strategia import Strategia


class RR(Strategia):
    def __init__(self):
        self.kwant_czasu = 5

    def zmiana_procesu_w_trakcie_trwania_innego(self) ->bool:
        return True

    def wybierz_nastepny_proces(self, kolejka):
        pass

    def wykonuj_proces(self, proces, delta_t):
        pass

