from StrategieAlgorytmy.Strategia import Strategia


class SJF(Strategia):
    def wybierz_nastepny_proces(self, kolejka):
        if kolejka:
            proces = min(kolejka, key=lambda x: x.czas_pozostaly_do_konca_realizacji)
            kolejka.remove(proces)
            return proces
        else:
            return None

    def wykonuj_proces(self, proces, delta_t):
        pass
