from Proces import Proces
from Procesor import Procesor
from StrategieAlgorytmy.FCFS import FCFS


def main():
    # zadan powinno byc duzo, setki tysiecy do miliona
    # kazdy algorytm powinien przeanalizowac dokladnie te same procesy
    # rozklad czasow procesow?
    procesy = [Proces(1, 5), Proces(2, 4), Proces(3, 7), Proces(4, 1), Proces(5, 6)]
    procesor = Procesor(FCFS, procesy)
    for i in range(9):
        procesor.wykonaj_jednostke_czasu()
        print(procesor)

if __name__ == '__main__':
    main()
