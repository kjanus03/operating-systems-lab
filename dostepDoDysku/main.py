import warnings
from copy import deepcopy
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from DiskScheduler import DiskScheduler
from Request import Request
from RequestGenerator import RequestGenerator


def adjust_seaborn(palette: str, style: str) -> None:
    sns.set_palette(palette)
    sns.set_style(style)


def turn_dss_to_req_dfs(*schedulers: DiskScheduler) -> List[pd.DataFrame]:
    """Turns disk scheduler objects to pandas DataFrames of finished requests"""
    dfs = []
    for ds in schedulers:
        data = [{"position": r.position, "arrival_time": r.arrival_time, "wait_time": r.wait_time} for r in
                ds.finished_requests]
        df = pd.DataFrame(data)
        dfs.append(df)
    return dfs


def resize_plot(title: str) -> None:
    plt.figure(figsize=(12, 8))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title(title, fontsize=20)


alg_names = ["FCFS", "SSTF", "SCAN", "C-SCAN"]


def main_plot(*request_lists: List[pd.DataFrame], request_count: int, time_limit: int, disk_size: int,
              max_arrival_time: int) -> None:

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(26, 18), )
    fig.suptitle(
        f'Disk scheduling simulation: {request_count} requests; {disk_size} disk size; '
        f'{max_arrival_time} max arrival time; {time_limit} time limit\n', fontsize=34)
    for i, df in enumerate(request_lists):
        positions: pd.Series = df['position']
        arrival_times: pd.Series = df['arrival_time']
        df["y_value"] = range(len(df) - 1, -1, -1)
        ax = axes[i // 2, i % 2]
        # sns.scatterplot(positions, range(len(df) - 1, -1, -1), s=200, hue=arrival_times, legend=True, ax=ax)
        sns.scatterplot(x="position", y="y_value", data=df, s=210, hue="arrival_time", ax=ax, palette="viridis_r",
                        legend=False)
        norm = plt.Normalize(arrival_times.min(), arrival_times.max())
        sm = plt.cm.ScalarMappable(cmap="viridis_r", norm=norm)
        sm.set_array([])
        colorbar = fig.colorbar(sm, ax=ax)
        colorbar.set_label("arrival_time", fontsize=20)
        colorbar.ax.tick_params(labelsize=18)

        for j in range(len(df) - 1):
            ind = abs(len(df) - j) - 2
            dy = -1  # adjust this value to set the vertical distance of the line
            line_x = [positions[ind], positions[ind + 1]]
            line_y = [j + 1, j + 1 + dy]
            ax.plot(line_x, line_y, color='black', linewidth=1)

        ax.set_title(alg_names[i], fontsize=30)
        ax.set_xlabel("Request position", fontsize=22)
        ax.set_ylabel("Order of execution", fontsize=22)
        ax.tick_params(labelsize=20)

        ax.set_ylim([0, len(df) - 1])
        ax.set_yticks([])
    plt.tight_layout()
    plt.show()


def example() -> None:
    requests = [Request(98), Request(183), Request(37), Request(122), Request(14), Request(124), Request(65),
                Request(67)]

    disk_scheduler1 = DiskScheduler(200, deepcopy(requests), 53)
    print(f'Number of head movements: {disk_scheduler1.fcfs()}')

    disk_scheduler2 = DiskScheduler(200, deepcopy(requests), 53)
    print(f'Number of head movements: {disk_scheduler2.sstf()}')

    disk_scheduler3 = DiskScheduler(200, deepcopy(requests), 53)
    print(f'Number of head movements: {disk_scheduler3.scan()}')

    disk_scheduler4 = DiskScheduler(200, deepcopy(requests), 53)
    print(f'Number of head movements: {disk_scheduler4.cscan()}\n')

    df1, df2, df3, df4 = turn_dss_to_req_dfs(disk_scheduler1, disk_scheduler2, disk_scheduler3, disk_scheduler4)

    main_plot(
        *[finished_req_df for finished_req_df in (df1, df2, df3, df4)],
        request_count=len(requests), time_limit=disk_scheduler1.time_limit,
        disk_size=disk_scheduler1.disk_size, max_arrival_time=0,
    )


def main() -> None:
    time_limit = 1500
    request_number_with_arrival_time = 600
    request_number_initial = 100
    max_arrival_time = 1300
    disk_size = 200
    initial_head_position = 112
    reqGenerator = RequestGenerator(request_number_with_arrival_time, max_arrival_time, disk_size)
    request_list = [Request(position) for position in
                    reqGenerator.generate_uniform_positions()[:request_number_initial]] + reqGenerator.get_requests(
        time_type="uniform")

    # pprint(sorted(request_list, key=lambda x: x.arrival_time))
    adjust_seaborn("viridis", "white")

    resize_plot("Time arrival of processes generated with normal distribution, std=350")
    sns.histplot(reqGenerator.generate_std_times().reshape((request_number_with_arrival_time, 1)), legend=False)
    plt.show()

    resize_plot("Time arrival of processes generated with uniform distribution")
    sns.histplot(reqGenerator.generate_uniform_times().reshape((request_number_with_arrival_time, 1)), legend=False)
    plt.show()

    diskScheduler1_1 = DiskScheduler(disk_size, deepcopy(request_list), initial_head_position, time_limit=time_limit)
    print(f'FCFS number of head movements: {diskScheduler1_1.fcfs()}')
    print(f'Number of executed requests: {diskScheduler1_1.request_count}')
    print(f'Mean number of moves per request: {diskScheduler1_1.moves_per_request()}')
    print(f'Mean wait time of a request: {diskScheduler1_1.mean_wait_time()}\n')

    diskScheduler2_1 = DiskScheduler(disk_size, deepcopy(request_list), initial_head_position, time_limit=time_limit)
    print(f'SSTF number of head movements: {diskScheduler2_1.sstf()}')
    print(f'Number of executed requests: {diskScheduler2_1.request_count}')
    print(f'Mean number of moves per request: {diskScheduler2_1.moves_per_request()}')
    print(f'Mean wait time of a request: {diskScheduler2_1.mean_wait_time()}\n')

    diskScheduler3_1 = DiskScheduler(disk_size, deepcopy(request_list), initial_head_position, time_limit=time_limit)
    print(f'SCAN number of head movements: {diskScheduler3_1.scan()}')
    print(f'Number of executed requests: {diskScheduler3_1.request_count}')
    print(f'Mean number of moves per request: {diskScheduler3_1.moves_per_request()}')
    print(f'Mean wait time of a request: {diskScheduler3_1.mean_wait_time()}\n')

    diskScheduler4_1 = DiskScheduler(disk_size, deepcopy(request_list), initial_head_position, time_limit=time_limit)
    print(f'C-SCAN number of head movements: {diskScheduler4_1.cscan()}')
    print(f'Number of executed requests: {diskScheduler4_1.request_count}')
    print(f'Mean number of moves per request: {diskScheduler4_1.moves_per_request()}')
    print(f'Mean wait time of a request: {diskScheduler4_1.mean_wait_time()}\n')

    df1_1, df2_1, df3_1, df4_1 = turn_dss_to_req_dfs(diskScheduler1_1, diskScheduler2_1, diskScheduler3_1,
                                                     diskScheduler4_1)

    wait_times = {"labels": alg_names,
                  "mean_wait_time": [np.mean(df['wait_time']) for df in (df1_1, df2_1, df3_1, df4_1)]}
    resize_plot("Mean algorithm wait time for a request execution")
    sns.barplot(x="labels", y="mean_wait_time", data=wait_times)
    plt.show()

    main_plot(
        *[finished_req_df for finished_req_df in (df1_1, df2_1, df3_1, df4_1)],
        request_count=request_number_initial + request_number_with_arrival_time, time_limit=time_limit,
        disk_size=disk_size, max_arrival_time=max_arrival_time,
    )

    plt.show()


if __name__ == '__main__':
    example()
    main()
