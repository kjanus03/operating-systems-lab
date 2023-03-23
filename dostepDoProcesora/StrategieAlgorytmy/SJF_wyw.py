from StrategieAlgorytmy.Strategia import Strategia


class SJF_wyw(Strategia):
    @property
    def zmiana_procesu_w_trakcie_trwania_innego(self) -> bool:
        return True

    def wybierz_nastepny_proces(self, kolejka, czas_dzialania):
        if kolejka:
            mozliwe = [proces1 for proces1 in kolejka if proces1.moment_zgloszenia <= czas_dzialania]
            if mozliwe:
                proces = min(mozliwe, key=lambda x: x.czas_pozostaly_do_konca_realizacji)
                return proces
        return None
