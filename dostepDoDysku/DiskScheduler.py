from typing import List

from Request import Request


class DiskScheduler():
    def __init__(self, disk_size: int, requests: List[Request], head_position: int = 0, time_limit: int = 10000):
        self.disk_size = disk_size
        self.requests = requests
        self.head_position = head_position
        self.time_limit = time_limit
        self.head_movements = 0
        self.executed_positions = [head_position]

    def finish_request(self, req: Request):
        self.executed_positions.append(req.position)

    def fcfs(self) -> int:
        self.requests.sort(key=lambda x: x.arrival_time)
        while self.head_movements < self.time_limit and self.requests:
            curr_request = self.requests.pop(0)
            self.head_movements += abs(curr_request.position - self.head_position)
            self.head_position = curr_request.position
            self.finish_request(curr_request)
        return self.head_movements

    def sstf(self):
        original_requests = self.requests.copy()
        self.requests.sort(key=lambda x: abs(x.position - self.head_position))
        while self.head_movements < self.time_limit and self.requests:
            self.requests = [req for req in original_requests if req.arrival_time <= self.head_movements]
            self.requests.sort(key=lambda x: abs(x.position - self.head_position))
            curr_request = self.requests.pop(0)
            original_requests.remove(curr_request)
            self.head_movements += abs(curr_request.position - self.head_position)
            self.head_position = curr_request.position
            self.finish_request(curr_request)
        return self.head_movements

    def scan(self):
        original_requests = self.requests.copy()
        while self.head_movements < self.time_limit and self.requests:
            left_requests = [req for req in self.requests if req.position < self.head_position]
            right_requests = sorted([req for req in self.requests if req.position >= self.head_position])
            for i, direction in enumerate((left_requests, right_requests)):
                for curr_request in direction:
                    if curr_request.arrival_time <= self.head_movements:
                        original_requests.remove(curr_request)
                        self.head_movements += abs(curr_request.position - self.head_position)
                        self.head_position = curr_request.position
                        last_request = curr_request
                        self.finish_request(curr_request)
                self.requests = original_requests
                if self.requests:
                    if i == 0:
                        self.head_position = 0
                        self.executed_positions.append(self.head_position)
                        self.head_movements += abs(last_request.position - self.head_position)
                    if i == 1:
                        self.head_position = self.disk_size
                        self.executed_positions.append(self.head_position)
                        self.head_movements += abs(last_request.position - self.head_position)
        return self.head_movements

    def cscan(self):
        original_requests = self.requests.copy()
        while self.head_movements < self.time_limit and self.requests:
            right_requests = sorted([req for req in self.requests if req.position >= self.head_position])
            for curr_request in right_requests:
                if curr_request.arrival_time <= self.head_movements:
                    original_requests.remove(curr_request)
                    self.head_movements += abs(curr_request.position - self.head_position)
                    self.head_position = curr_request.position
                    last_request = curr_request
                    self.finish_request(curr_request)
            self.requests = original_requests
            if self.requests:
                self.executed_positions.append(self.disk_size)
                self.head_movements += (self.disk_size - last_request.position) - 1
                self.head_position = 0
                self.executed_positions.append(self.head_position)
        return self.head_movements
