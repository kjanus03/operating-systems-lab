import statistics

from Proces import Proces
from Procesor import Procesor
from StrategieAlgorytmy.FCFS import FCFS
from StrategieAlgorytmy.SJF import SJF


def main():
    # zadan powinno byc duzo, setki tysiecy do miliona
    # kazdy algorytm powinien przeanalizowac dokladnie te same procesy
    # rozklad czasow procesow?
    procesy = [Proces(1, 5), Proces(2, 4), Proces(3, 7), Proces(4, 1), Proces(5, 6)]
    procesor = Procesor(SJF, procesy)
    for i in range(100):
        procesor.wykonaj_jednostke_czasu()
        if procesor.kolejka == [] and procesor.aktualnie_wykonywany is None:
            print("\nKoniec symulacji")
            print(f'Liczba przelaczen: {procesor.zmiany_zadan}')
            print(
                f'Sredni czas oczekiwania: {statistics.mean([proces.czas_oczekiwania_na_rozpoczecie for proces in procesor.procesy_wykonane])}')
            print(
                f'Najdluzszy czas oczekiwania: {max([proces.czas_oczekiwania_na_rozpoczecie for proces in procesor.procesy_wykonane])}')
            break
        print(procesor)


if __name__ == '__main__':
    main()
