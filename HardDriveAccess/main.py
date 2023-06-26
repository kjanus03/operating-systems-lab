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
        data = [
            {"position": r.position, "arrival_time": r.arrival_time, "wait_time": r.wait_time, "deadline": r.deadline}
            for r in
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
    nrows, ncols = 2, 2
    if (len(request_lists) == 2):
        nrows = 2
        ncols = 1
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(26, 18), )
    fig.suptitle(
        f'Disk scheduling simulation: {request_count} requests; {disk_size} disk size; '
        f'{max_arrival_time} max arrival time; {time_limit} time limit\n', fontsize=34)
    for i, df in enumerate(request_lists):
        df = request_lists[i]
        positions: pd.Series = df['position']
        arrival_times: pd.Series = df['arrival_time']
        df["y_value"] = range(len(df) - 1, -1, -1)
        yy = [0, 0, 1, 1]
        xx = [0, 1, 0, 1]
        ax = axes[xx[i], yy[i]]
        # sns.scatterplot(positions, range(len(df) - 1, -1, -1), s=200, hue=arrival_times, legend=True, ax=ax)
        sns.scatterplot(x="position", y="y_value", data=df, s=210, hue="arrival_time", ax=ax, palette="viridis_r",
                        legend=False)
        norm = plt.Normalize(arrival_times.min(), arrival_times.max())
        sm = plt.cm.ScalarMappable(cmap="viridis_r", norm=norm)
        sm.set_array([])
        colorbar = fig.colorbar(sm, ax=ax)
        colorbar.set_label("arrival_time", fontsize=20)
        colorbar.ax.tick_params(labelsize=18)
        colorbar.ax.invert_yaxis()

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
    plt.savefig("plots/main_plot.png")
    plt.show()


def deadline_plot(*request_lists: List[pd.DataFrame], request_count: int, time_limit: int, disk_size: int,
                  max_arrival_time: int, missed_deadlines: List[Request]) -> None:
    alg_names2 = ["SSTF_EDF", "SSTF_FD_SCAN"]
    nrows, ncols = 1, 2
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(26, 18), )
    fig.suptitle(
        f'Disk scheduling deadlines simulation: {request_count} requests; {disk_size} disk size; '
        f'{max_arrival_time} max arrival time;\n {time_limit} time limit; 5% deadline probability\n', fontsize=34)
    for i, df in enumerate(request_lists):
        df = request_lists[i]
        positions: pd.Series = df['position']
        arrival_times: pd.Series = df['arrival_time']
        df["y_value"] = range(len(df) - 1, -1, -1)
        xx = [0, 1, 0, 1]
        ax = axes[xx[i]]
        df1 = df[df['deadline'] == 0]
        df2 = df[df['deadline'] > 0]
        # sns.scatterplot(positions, range(len(df) - 1, -1, -1), s=200, hue=arrival_times, legend=True, ax=ax)

        sns.scatterplot(x="position", y="y_value", data=df1, s=210, hue="arrival_time", ax=ax, palette="Blues",
                        legend=False, edgecolor='black', linewidth=1)

        sns.scatterplot(x="position", y="y_value", data=df2, s=210, ax=ax, color='r', legend=False, edgecolor='black',
                        linewidth=0.5)

        norm = plt.Normalize(arrival_times.min(), arrival_times.max())
        sm = plt.cm.ScalarMappable(cmap="Blues", norm=norm)
        sm.set_array([])
        colorbar = fig.colorbar(sm, ax=ax)
        colorbar.set_label("arrival_time", fontsize=20)
        colorbar.ax.tick_params(labelsize=18)
        colorbar.ax.invert_yaxis()

        for j in range(len(df) - 1):
            ind = abs(len(df) - j) - 2
            dy = -1  # adjust this value to set the vertical distance of the line
            line_x = [positions[ind], positions[ind + 1]]
            line_y = [j + 1, j + 1 + dy]
            ax.plot(line_x, line_y, color='black', linewidth=1)

        ax.set_title(alg_names2[i], fontsize=30)
        ax.set_xlabel("Request position", fontsize=22)
        ax.set_ylabel("Order of execution", fontsize=22)
        ax.tick_params(labelsize=20)

        ax.set_ylim([0, len(df) - 1])
        ax.set_yticks([])
    plt.tight_layout()
    plt.savefig("plots/deadline_plot.png")
    plt.show()


def facet_plot(df: pd.DataFrame) -> None:
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    plt.figure(figsize=(8, 6))
    # Initialize the FacetGrid object
    g = sns.FacetGrid(df, row="Label", hue="Label", aspect=7, height=2, palette="viridis_r")

    # Draw the densities in a few steps
    g.map(sns.kdeplot, "wait_time",
          bw_adjust=.5, clip_on=False,
          fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, "wait_time", clip_on=False, color="w", lw=2, bw_adjust=.5)

    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)

    g.map(label, "wait_time")

    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-.30)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)
    plt.suptitle("Wait time density distribution", fontsize=28)
    plt.savefig("plots/wait_time_density.png")
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
    time_limit = 10_000
    request_number_with_arrival_time = 800
    request_number_initial = 200
    max_arrival_time = 10_000
    disk_size = 500
    initial_head_position = 250
    reqGenerator = RequestGenerator(request_number_with_arrival_time, max_arrival_time, disk_size)
    request_list = [Request(position) for position in
                    reqGenerator.generate_uniform_positions()[:request_number_initial]] + reqGenerator.get_requests(
        time_type="uniform")
    request_list_deadlines = [Request(position) for position in
                              reqGenerator.generate_uniform_positions()[
                              :request_number_initial]] + reqGenerator.get_requests(
        time_type="normal")
    request_list_deadlines = reqGenerator.generate_deadlines_for_requests(request_list_deadlines)

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


    time_limit2 = 15000
    diskScheduler3_1 = DiskScheduler(disk_size, deepcopy(request_list), initial_head_position, time_limit=time_limit2)
    print(f'SCAN number of head movements: {diskScheduler3_1.scan()}')
    print(f'Number of executed requests: {diskScheduler3_1.request_count}')
    print(f'Mean number of moves per request: {diskScheduler3_1.moves_per_request()}')
    print(f'Mean wait time of a request: {diskScheduler3_1.mean_wait_time()}\n')

    diskScheduler4_1 = DiskScheduler(disk_size, deepcopy(request_list), initial_head_position, time_limit=time_limit2)
    print(f'C-SCAN number of head movements: {diskScheduler4_1.cscan()}')
    print(f'Number of executed requests: {diskScheduler4_1.request_count}')
    print(f'Mean number of moves per request: {diskScheduler4_1.moves_per_request()}')
    print(f'Mean wait time of a request: {diskScheduler4_1.mean_wait_time()}\n')

    diskScheduler5_1 = DiskScheduler(disk_size, deepcopy(request_list_deadlines), initial_head_position,
                                     time_limit=time_limit)
    print(len(request_list_deadlines))
    print(f'SSTF-EDF number of head movements: {diskScheduler5_1.sstf_edf()}')
    print(f'Number of executed requests: {diskScheduler5_1.request_count}')
    print(f'Number of executed deadline requests: {diskScheduler5_1.finished_deadline_requests()}')
    print(f'Number of missed deadline requests: {diskScheduler5_1.missed_deadline_requests()}')
    print(f'Mean number of moves per request: {diskScheduler5_1.moves_per_request()}')
    print(f'Mean wait time of a request: {diskScheduler5_1.mean_wait_time()}\n')

    diskScheduler6_1 = DiskScheduler(disk_size, deepcopy(request_list_deadlines), initial_head_position,
                                     time_limit=time_limit)
    print(f'SSTF-FD-SCAN number of head movements: {diskScheduler6_1.sstf_fd_scan()}')
    print(f'Number of executed requests: {diskScheduler6_1.request_count}')
    print(f'Number of executed deadline requests: {diskScheduler6_1.finished_deadline_requests()}')
    print(f'Number of missed deadline requests: {diskScheduler6_1.missed_deadline_requests()}')
    print(f'Mean number of moves per request: {diskScheduler6_1.moves_per_request()}')
    print(f'Mean wait time of a request: {diskScheduler6_1.mean_wait_time()}\n')

    df1_1, df2_1, df3_1, df4_1 = turn_dss_to_req_dfs(diskScheduler1_1, diskScheduler2_1, diskScheduler3_1,
                                                     diskScheduler4_1)
    df5_1, df6_1 = turn_dss_to_req_dfs(diskScheduler5_1, diskScheduler6_1)

    wait_times = {"labels": alg_names,
                  "mean_wait_time": [np.mean(df['wait_time']) for df in (df1_1, df2_1, df3_1, df4_1)]}
    resize_plot("Mean algorithm wait time for a request execution")
    sns.barplot(x="labels", y="mean_wait_time", data=wait_times)
    plt.show()

    merged_df1 = pd.concat([df1_1.assign(Label=alg_names[0]),
                            df2_1.assign(Label=alg_names[1]),
                            df3_1.assign(Label=alg_names[2]),
                            df4_1.assign(Label=alg_names[3])])
    merged_df1 = merged_df1[merged_df1['wait_time'] < 0.95 * max(merged_df1['wait_time'])]
    facet_plot(merged_df1)

    merged_df2 = pd.concat([
        df2_1.assign(Label=alg_names[1]),
        df3_1.assign(Label=alg_names[2]),
        df4_1.assign(Label=alg_names[3])])
    merged_df2 = merged_df2[merged_df2['wait_time'] < 0.85 * max(merged_df2['wait_time'])]
    facet_plot(merged_df2)

    main_plot(
        *[finished_req_df for finished_req_df in (df1_1, df2_1, df3_1, df4_1)],
        request_count=request_number_initial + request_number_with_arrival_time, time_limit=time_limit,
        disk_size=disk_size, max_arrival_time=max_arrival_time,
    )
    plt.show()

    deadline_plot(df5_1, df6_1, request_count=request_number_initial + request_number_with_arrival_time,
                  time_limit=time_limit, disk_size=disk_size, max_arrival_time=max_arrival_time,
                  missed_deadlines=diskScheduler5_1.missed_requests)

    plt.show()


if __name__ == '__main__':
    example()
    main()
