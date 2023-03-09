from Proces import Proces
from Procesor import Procesor
from StrategieAlgorytmy.FCFS import FCFS


def main():
    procesy = [Proces(1, 5.2), Proces(2, 3.7), Proces(3, 7.1), Proces(4, 1.8)]
    procesor = Procesor(FCFS, procesy)
    print(procesor)
    procesor.przetworz_kolejke_jednokrotnie()
    print(procesor)
    procesor.przetworz_kolejke_jednokrotnie()
    print(procesor)
    procesor.wyswietl_procesy_wykonane()

if __name__ == '__main__':
    main()
