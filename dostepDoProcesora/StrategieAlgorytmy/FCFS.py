from StrategieAlgorytmy.Strategia import Strategia


class FCFS(Strategia):
    def wybierz_nastepny_proces(self, kolejka):
        proces = kolejka[0]
        kolejka.remove(proces)
        return proces

    def wykonuj_proces(self, proces, delta_t):
        proces.czas_pozostaly_do_konca_realizacji -= 1
