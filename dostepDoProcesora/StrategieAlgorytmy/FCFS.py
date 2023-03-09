from StrategieAlgorytmy.Strategia import Strategia


class FCFS(Strategia):
    def wybierz_nastepny_proces(self, kolejka):
        return kolejka[0]

