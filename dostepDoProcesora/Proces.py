class Proces:

    def __init__(self, numer: int, dlugosc_fazy_procesora: float):
        self.__numer = numer
        # dlugosc fazy procesora okresla ile czasu wymaga dany proces do zostania zrealizowanym przez procesor
        self.dlugosc_fazy_procesora = dlugosc_fazy_procesora
        # status przyjmuje wartosc nowy/oczekujacy/wykonywany/zakonczony
        self.status = "nowy"
        self.moment_zgloszenia = 0
        self.czas_oczekiwania = None

    def zglos(self, moment_zgloszenia):
        self.moment_zgloszenia = moment_zgloszenia
        self.status = "oczekujacy"


    def czekaj(self):
        self.czas_oczekiwania += 1

    # korzystam z dekoratora property aby uczynic numer procesu zmienna niemodyfikowalna
    @property
    def numer(self) -> int:
        return self.__numer

    def __repr__(self):
        return f'{"{"}Numer procesu: {self.numer}\n\tDlugosc fazy procesora: {self.dlugosc_fazy_procesora}\n' \
               f'\tMoment zgloszenia: {self.moment_zgloszenia}\n\tCzas oczekiwania: {self.czas_oczekiwania}\n' \
               f'\tStatus: {self.status}{"}"}\n'

    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return (self.numer, self.dlugosc_fazy_procesora, self.status, self.moment_zgloszenia,
                    self.czas_oczekiwania) == (
                       other.numer, other.dlugosc_fazy_procesora, other.status, other.moment_zgloszenia,
                       other.czas_oczekiwania)
        else:
            return NotImplemented
