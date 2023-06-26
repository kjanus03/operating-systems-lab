import copy
import random
import statistics
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from Proces import Proces
from Procesor import Procesor
from StrategieAlgorytmy.FCFS import FCFS
from StrategieAlgorytmy.RR import RR
from StrategieAlgorytmy.SJF import SJF
from StrategieAlgorytmy.SJF_wyw import SJF_wyw


def generuj_procesy(liczba_procesow: int, max_dlugosc_fazy: int, max_moment_zgloszenia) -> list[Proces]:
    # max dlugosc fazy - ograniczenie na dlugosc fazy, max czas zgloszenia - ostatni moemnt w ktorym moze byc zglaszany proces
    procesy = []
    srednia_czasow = max_dlugosc_fazy // 2.2
    odchylenie_standardowe_czasow = srednia_czasow

    srednia_zgloszen = max_moment_zgloszenia // 2.5
    odchylenie_standardowe_zgloszen = max_moment_zgloszenia // 2.5

    for i in range(liczba_procesow):
        dlugosc_fazy_procesora = abs(int(random.gauss(srednia_czasow, odchylenie_standardowe_czasow))) + 1
        if i < liczba_procesow // 10:
            proces = Proces(i, dlugosc_fazy_procesora, 0)
        else:
            moment_zgloszenia = int(np.random.uniform(1, max_moment_zgloszenia))
            proces = Proces(i, dlugosc_fazy_procesora, moment_zgloszenia)
        procesy.append(proces)
    procesy.sort(key=lambda x: x.moment_zgloszenia)
    return procesy


def main():
    # zadan powinno byc duzo, setki tysiecy do miliona
    # kazdy algorytm powinien przeanalizowac dokladnie te same procesy
    # rozklad czasow procesow?
    random.seed(45)
    liczba_procesow, max_czas, max_moment_zgloszenia = 400, 34, 1200
    procesy = generuj_procesy(liczba_procesow, max_czas, max_moment_zgloszenia)
    algorytmy = [FCFS, SJF, SJF_wyw]
    listy_procesow = [copy.deepcopy(procesy) for _ in range(len(algorytmy) + 1)]
    lista_wykonanych = []
    print(Counter([p.dlugosc_fazy_procesora for p in procesy]))

    liczby_przelaczen = []
    for i, alg in enumerate(algorytmy):
        procesor = Procesor(alg, listy_procesow[i])
        limit_czasu = 4000000
        for i2 in range(limit_czasu):
            procesor.wykonaj_jednostke_czasu()
            if (procesor.kolejka == [] and procesor.aktualnie_wykonywany is None) or i2 == limit_czasu - 1:
                print(f'\nKoniec symulacji dla algorytmu {alg}')
                print(f'Liczba wykonanych zadan: {len(procesor.procesy_wykonane)}')
                print(f'Liczba przelaczen: {procesor.zmiany_zadan}')
                liczby_przelaczen.append(procesor.zmiany_zadan)
                print(
                    f'Sredni czas oczekiwania na rozpoczecie procesu: {statistics.mean([proces.czas_oczekiwania_na_rozpoczecie for proces in procesor.procesy_wykonane])}')
                print(
                    f'Najdluzszy czas oczekiwania: {max([proces.czas_oczekiwania_na_rozpoczecie for proces in procesor.procesy_wykonane])}')
                print(
                    f'Sredni czas od zgloszenia procesu do ukonczenia go: {statistics.mean([proces.czas_od_zgloszenia_do_ukonczenia for proces in procesor.procesy_wykonane])}')
                print()
                lista_wykonanych.append(procesor.procesy_wykonane)
                break

    procesor = Procesor(RR, listy_procesow[3])
    for i in range(limit_czasu):
        procesor.wykonaj_jednostke_czasu_RR()
        if (procesor.kolejka == [] and procesor.aktualnie_wykonywany is None) or i == limit_czasu - 1:
            print(f'\nKoniec symulacji dla algorytmu {RR}')
            print(f'Liczba wykonanych zadan: {len(procesor.procesy_wykonane)}')
            print(f'Liczba przelaczen: {procesor.zmiany_zadan}')
            liczby_przelaczen.append(procesor.zmiany_zadan)
            print(
                f'Sredni czas oczekiwania na rozpoczecie procesu: {statistics.mean([proces.czas_oczekiwania_na_rozpoczecie for proces in procesor.procesy_wykonane])}')
            print(
                f'Najdluzszy czas oczekiwania: {max([proces.czas_oczekiwania_na_rozpoczecie for proces in procesor.procesy_wykonane])}')
            print(
                f'Sredni czas od zgloszenia procesu do ukonczenia go: {statistics.mean([proces.czas_od_zgloszenia_do_ukonczenia for proces in procesor.procesy_wykonane])}')
            print()
            lista_wykonanych.append(procesor.procesy_wykonane)
            break

    # Analiza wynikow
    wykonane_fcfs, wykonane_sjf, wykonane_sjf_wyw, wykonane_rr = lista_wykonanych
    print(wykonane_fcfs[:12])
    print(wykonane_rr[:12])
    czasy_oczekiwania, czasy_wykonania, labels = [], [], []
    for cls in wykonane_fcfs:
        czasy_oczekiwania.append(cls.czas_oczekiwania_na_rozpoczecie)
        czasy_wykonania.append(cls.czas_od_zgloszenia_do_ukonczenia)
        labels.append("FCFS")

    for cls in wykonane_sjf:
        czasy_oczekiwania.append(cls.czas_oczekiwania_na_rozpoczecie)
        czasy_wykonania.append(cls.czas_od_zgloszenia_do_ukonczenia)
        labels.append("SJF")

    for cls in wykonane_sjf_wyw:
        czasy_oczekiwania.append(cls.czas_oczekiwania_na_rozpoczecie)
        czasy_wykonania.append(cls.czas_od_zgloszenia_do_ukonczenia)
        labels.append("SJF_wyw")

    for cls in wykonane_rr:
        czasy_oczekiwania.append(cls.czas_oczekiwania_na_rozpoczecie)
        czasy_wykonania.append(cls.czas_od_zgloszenia_do_ukonczenia)
        labels.append("RR")

    sns.set_palette("Pastel2")
    df = pd.DataFrame({"Algorytm": labels, "Czas_oczekiwania_na_rozpoczecie": czasy_oczekiwania,
                       "Czas_od_zgloszenia_do_zakonczenia": czasy_wykonania})
    sns.violinplot(x="Algorytm", y='Czas_oczekiwania_na_rozpoczecie', data=df)
    plt.show()

    sns.boxplot(x="Algorytm", y='Czas_oczekiwania_na_rozpoczecie', data=df)
    plt.savefig("boxplot_wait_time.png")
    plt.show()

    sns.pairplot(df, hue="Algorytm")
    plt.show()

    sns.histplot(data=df, x="Czas_od_zgloszenia_do_zakonczenia", hue="Algorytm", multiple="stack", legend=True)
    plt.show()

    nazwy = ["FCFS", "SJF", "SJF_wyw", "RR"]
    switches_df = pd.DataFrame({"Algorytm": nazwy, "Liczba_przelaczen": liczby_przelaczen})
    wykonane_df = pd.DataFrame({"Algorytm": nazwy, "Liczba_wykonanych_procesow": [len(w) for w in lista_wykonanych]})
    sns.barplot(x="Algorytm", y="Liczba_przelaczen", data=switches_df)
    plt.show()

    sns.barplot(x="Algorytm", y="Liczba_wykonanych_procesow", data=wykonane_df)
    plt.show()

    plt.plot()
    plt.show()


if __name__ == '__main__':
    main()
