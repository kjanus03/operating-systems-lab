class Proces:

    def __init__(self, numer: int, dlugosc_fazy_procesora: int, moment_zgloszenia: int):
        self.__numer = numer
        # dlugosc fazy procesora okresla ile czasu wymaga dany proces do zostania zrealizowanym przez procesor
        self.dlugosc_fazy_procesora = dlugosc_fazy_procesora
        # status przyjmuje wartosc nowy/oczekujacy/wykonywany/zakonczony
        self.__status = "nowy"
        self.moment_zgloszenia = moment_zgloszenia
        self.czas_oczekiwania_na_rozpoczecie = None
        self.czas_od_zgloszenia_do_ukonczenia = 0
        self.wszystkie_czasy_oczekiwania = []
        self.czas_pozostaly_do_konca_realizacji = dlugosc_fazy_procesora
        self.czas_trwania_realizacji = 0

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
        return f'{"{"}Numer procesu: {self.numer}\tDlugosc fazy procesora: {self.dlugosc_fazy_procesora}' \
               f'\tMoment zgloszenia: {self.moment_zgloszenia}' \
               f'\tCzas oczekiwania na rozpoczecie: {self.czas_oczekiwania_na_rozpoczecie}' \
               f'\tCzas trwania realizacji: {self.czas_trwania_realizacji}' \
               f'\tCzas pozostaly do konca realizacji: {self.czas_pozostaly_do_konca_realizacji}' \
               f'\tCzas od zgloszenia do ukonczenia: {self.czas_od_zgloszenia_do_ukonczenia}'\
               f'\tStatus: {self.status}{"}"}'

    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return (self.numer, self.dlugosc_fazy_procesora, self.status, self.moment_zgloszenia,
                   ) == (
                       other.numer, other.dlugosc_fazy_procesora, other.status, other.moment_zgloszenia,
                   )
        else:
            return NotImplemented
