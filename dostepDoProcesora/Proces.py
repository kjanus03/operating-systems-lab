class Proces:

    def __init__(self, numer: int, dlugosc_fazy_procesora: int):
        self.__numer = numer
        # dlugosc fazy procesora okresla ile czasu wymaga dany proces do zostania zrealizowanym przez procesor
        self.dlugosc_fazy_procesora = dlugosc_fazy_procesora
        # status przyjmuje wartosc nowy/oczekujacy/wykonywany/zakonczony
        self.__status = "nowy"
        self.moment_zgloszenia = 0
        self.czas_oczekiwania_na_rozpoczecie = None
        self.wszystkie_czasy_oczekiwania = []
        self.czas_pozostaly_do_konca_realizacji = dlugosc_fazy_procesora
        self.czas_trwania_realizacji = None

    def zglos(self, moment_zgloszenia):
        self.moment_zgloszenia = moment_zgloszenia
        self.__status = "oczekujacy"

    # korzystam z dekoratora property aby uczynic numer procesu zmienna niemodyfikowalna
    @property
    def numer(self) -> int:
        return self.__numer

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, s: str):
        self.__status = s

    def __repr__(self):
        return f'{"{"}Numer procesu: {self.numer}\n\tDlugosc fazy procesora: {self.dlugosc_fazy_procesora}\n' \
               f'\tMoment zgloszenia: {self.moment_zgloszenia}\n' \
               f'\tCzas oczekiwania na rozpoczecie: {self.czas_oczekiwania_na_rozpoczecie}\n' \
               f'\tCzas trwania realizacji: {self.czas_trwania_realizacji}\n' \
               f'\tCzas pozostaly do konca realizacji: {self.czas_pozostaly_do_konca_realizacji}\n' \
               f'\tStatus: {self.status}{"}"}\n'

    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return (self.numer, self.dlugosc_fazy_procesora, self.status, self.moment_zgloszenia,
                    self.czas_oczekiwania_na_rozpoczecie) == (
                       other.numer, other.dlugosc_fazy_procesora, other.status, other.moment_zgloszenia,
                       other.czas_oczekiwania)
        else:
            return NotImplemented
