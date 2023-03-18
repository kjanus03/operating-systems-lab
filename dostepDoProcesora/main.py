import statistics

from Proces import Proces
from Procesor import Procesor
from StrategieAlgorytmy.FCFS import FCFS
from StrategieAlgorytmy.SJF import SJF
from StrategieAlgorytmy.SJF_wyw import SJF_wyw
from StrategieAlgorytmy.RR import RR
from random import randint


def generuj_procesy():
    pass

def main():
    # zadan powinno byc duzo, setki tysiecy do miliona
    # kazdy algorytm powinien przeanalizowac dokladnie te same procesy
    # rozklad czasow procesow?
    procesy = [Proces(1, 4, 0), Proces(2, 4, 0), Proces(3, 9, 0), Proces(4, 1, 0), Proces(5, 8, 0), Proces(6, 3, 14)]
    procesor = Procesor(SJF_wyw, procesy)
    for i in range(100):
        procesor.wykonaj_jednostke_czasu()
        if procesor.kolejka == [] and procesor.aktualnie_wykonywany is None:
            print("\nKoniec symulacji")
            print(f'Liczba przelaczen: {procesor.zmiany_zadan}')
            print(
                f'Sredni czas oczekiwania na rozpoczecie procesu: {statistics.mean([proces.czas_oczekiwania_na_rozpoczecie for proces in procesor.procesy_wykonane])}')
            print(
                f'Najdluzszy czas oczekiwania: {max([proces.czas_oczekiwania_na_rozpoczecie for proces in procesor.procesy_wykonane])}')
            print(f'Sredni czas od zgloszenia procesu do ukonczenia go: {statistics.mean([proces.czas_od_zgloszenia_do_ukonczenia for proces in procesor.procesy_wykonane])}')
            print(f'Procesy wykonane: {procesor.procesy_wykonane}')
            break
        print(procesor)


if __name__ == '__main__':
    main()



