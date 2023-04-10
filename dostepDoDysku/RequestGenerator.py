from typing import List

import numpy as np
import numpy.typing as npt
from scipy.stats import truncnorm

from Request import Request


class RequestGenerator:
    def __init__(self, number: int, max_arrival_time: int = 1000, disk_size: int = 500):
        self.number = number
        self.max_arrival_time = max_arrival_time
        self.disk_size = disk_size

    def get_requests(self, time_type: str = "uniform") -> List[Request]:
        if time_type == "uniform":
            times = self.generate_uniform_times()
        elif time_type == "normal":
            std_dev = self.max_arrival_time//3
            times = self.generate_std_times(std_dev)
        else:
            print("Wrong distribution type!")
            return None

        positions = self.generate_uniform_positions()
        return [Request(position,time) for position, time in zip(positions, times)]

    # Functions to generate arrival_times of requests
    def generate_std_times(self, std_dev: int = 350) -> List[int]:
        lower_bound = 0
        upper_bound = self.max_arrival_time
        mean = self.max_arrival_time // 2
        a, b = (lower_bound - mean) / std_dev, (upper_bound - mean) / std_dev
        random_times = truncnorm.rvs(a, b, loc=mean, scale=std_dev, size=self.number).astype(int)
        return random_times

    def generate_uniform_times(self) -> npt.NDArray[np.int_]:
        return np.random.uniform(1, self.max_arrival_time, self.number).astype(int)

    def generate_uniform_positions(self) -> npt.NDArray[np.int_]:
        return np.random.uniform(1, self.disk_size, self.number).astype(int)
