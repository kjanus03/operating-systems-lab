import warnings
from typing import List

import matplotlib.pyplot as plt
import seaborn as sns

from DiskScheduler import DiskScheduler
from Request import Request
from RequestGenerator import RequestGenerator


def adjust_seaborn(style: str) -> None:
    sns.set_style(style)
    sns.color_palette("pastel")


def plot_values(*request_lists: List[Request]) -> None:
    plot_names = ["FCFS", "SSTF", "SCAN", "C-SCAN"]
    plt.figure(figsize=(16, 12))
    for i, values in enumerate(request_lists):
        positions = [r.position for r in values]
        arrival_times = [r.arrival_time for r in values]
        ax = plt.subplot(2, 2, i + 1)
        sns.scatterplot(positions, range(len(values) - 1, -1, -1), s=200, hue=arrival_times, legend=True)

        warnings.simplefilter(action='ignore', category=FutureWarning)
        for j in range(len(values) - 1):
            ind = abs(len(values) - j) - 2
            dy = -1  # adjust this value to set the vertical distance of the line
            line_x = [positions[ind], positions[ind + 1]]
            line_y = [j + 1, j + 1 + dy]
            ax.plot(line_x, line_y, color='black', linewidth=1)

        ax.set_title(plot_names[i])
        ax.set_xlabel("Request position")
        ax.set_ylabel("Order of execution")

        ax.set_ylim([0, len(values) - 1])
        ax.set_yticks([])
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # requests = [Request(98), Request(183), Request(37), Request(122), Request(14), Request(124), Request(65),
    #             Request(67)]
    #
    # diskScheduler1 = DiskScheduler(200, requests.copy(), 53)
    # print(f'Number of head movements: {diskScheduler1.fcfs()}')
    #
    # diskScheduler2 = DiskScheduler(200, requests.copy(), 53)
    # print(f'Number of head movements: {diskScheduler2.sstf()}')
    #
    # diskScheduler3 = DiskScheduler(200, requests.copy(), 53)
    # print(f'Number of head movements: {diskScheduler3.scan()}')
    #
    # diskScheduler4 = DiskScheduler(200, requests.copy(), 53)
    # print(f'Number of head movements: {diskScheduler4.cscan()}')
    #
    # plot_values(*[disk.executed_positions for disk in (diskScheduler1, diskScheduler2, diskScheduler3, diskScheduler4)])

    time_limit = 1500
    request_number_with_arrival_time = 100
    request_number_initial = 35
    max_arrival_time = 800
    disk_size = 200
    initial_head_position = 124
    reqGenerator = RequestGenerator(request_number_with_arrival_time, max_arrival_time, disk_size)
    request_list = [Request(position) for position in
                    reqGenerator.generate_uniform_positions()[:request_number_initial]] + reqGenerator.get_requests(
        time_type="uniform")
    print([r.position for r in request_list])
    # pprint(sorted(request_list, key=lambda x: x.arrival_time))

    adjust_seaborn("white")

    plt.title("Time arrival of processes generated with normal distribution with standard deviation of 350")
    plt.hist(reqGenerator.generate_std_times().reshape((request_number_with_arrival_time, 1)))
    plt.show()

    plt.title("Time arrival of processes generated with uniform distribution")
    plt.hist(reqGenerator.generate_uniform_times().reshape((request_number_with_arrival_time, 1)), color='r')
    plt.show()

    diskScheduler1_1 = DiskScheduler(disk_size, request_list.copy(), initial_head_position, time_limit=time_limit)
    print(f'FCFS number of head movements: {diskScheduler1_1.fcfs()}')
    print(f'Number of executed requests: {diskScheduler1_1.request_count}\n')

    diskScheduler2_1 = DiskScheduler(disk_size, request_list.copy(), initial_head_position, time_limit=time_limit)
    print(f'SSTF number of head movements: {diskScheduler2_1.sstf()}')
    print(f'Number of executed requests: {diskScheduler2_1.request_count}\n')

    diskScheduler3_1 = DiskScheduler(disk_size, request_list.copy(), initial_head_position, time_limit=time_limit)
    print(f'SCAN number of head movements: {diskScheduler3_1.scan()}')
    print(f'Number of executed requests: {diskScheduler3_1.request_count}\n')

    diskScheduler4_1 = DiskScheduler(disk_size, request_list.copy(), initial_head_position, time_limit=time_limit)
    print(f'C-SCAN number of head movements: {diskScheduler4_1.cscan()}')
    print(f'Number of executed requests: {diskScheduler4_1.request_count}\n')

    plot_values(
        *[disk.finished_requests for disk in (diskScheduler1_1, diskScheduler2_1, diskScheduler3_1, diskScheduler4_1)])
    plt.show()
