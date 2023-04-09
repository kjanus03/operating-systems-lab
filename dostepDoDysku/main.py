from typing import List

import matplotlib.pyplot as plt
import seaborn as sns

from DiskScheduler import DiskScheduler
from Request import Request


def adjust_seaborn(style: str):
    sns.set_style(style)


def plot_values(*value_lists: List[int]):
    plot_names = ["FCFS", "SSTF", "SCAN", "C-SCAN"]
    plt.figure(figsize=(16, 12))
    for i, values in enumerate(value_lists):
        ax = plt.subplot(2, 2, i + 1)
        sns.scatterplot(values, range(len(values) - 1, -1, -1))

        # Plotting the arrows
        # for j in range(len(values) - 1, 0, -1):
        #     ind = abs(len(values) - j) - 1
        #
        #     # Offsetting the arrow so that it doesn't overlap with the dot indicating the data point
        #     arrow_head_length = 1
        #     arrow_x_offset = 0.5 + arrow_head_length
        #
        #     # Arrow coordinates
        #     arrow_x = values[ind]
        #     arrow_y = j
        #     dx = values[ind + 1] - values[ind]
        #     dy = -1
        #     if dx < 0:
        #         dx += arrow_x_offset
        #     else:
        #         dx -= arrow_x_offset
        #
        #     plt.arrow(arrow_x, arrow_y, dx, dy, head_width=0.2, head_length=arrow_head_length,
        #               fc='k', ec='k')

        for j in range(len(values) - 1):
            ind = abs(len(values) - j) - 2
            dy = -1  # adjust this value to set the vertical distance of the line
            line_x = [values[ind], values[ind + 1]]
            line_y = [j + 1, j + 1 + dy]
            plt.plot(line_x, line_y, color='black', linewidth=1)

        plt.title(plot_names[i])
        plt.xlabel("Request position")
        plt.ylabel("Order of execution")

        plt.ylim([0, len(values) - 1])
        plt.yticks([])
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    requests = [Request(98), Request(183), Request(37), Request(122), Request(14), Request(124), Request(65),
                Request(67)]

    diskScheduler1 = DiskScheduler(200, requests.copy(), 53)
    print(f'Number of head movements: {diskScheduler1.fcfs()}')

    diskScheduler2 = DiskScheduler(200, requests.copy(), 53)
    print(f'Number of head movements: {diskScheduler2.sstf()}')

    diskScheduler3 = DiskScheduler(200, requests.copy(), 53)
    print(f'Number of head movements: {diskScheduler3.scan()}')

    diskScheduler4 = DiskScheduler(200, requests.copy(), 53)
    print(f'Number of head movements: {diskScheduler4.cscan()}')

    plot_values(*[disk.executed_positions for disk in (diskScheduler1, diskScheduler2, diskScheduler3, diskScheduler4)])
