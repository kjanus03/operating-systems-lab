from typing import List

from Request import Request


class DiskScheduler():
    def __init__(self, disk_size: int, requests: List[Request], head_position: int = 0, time_limit: int = 10000):
        self.disk_size = disk_size
        self.requests = requests
        self.head_position = head_position
        self.time_limit = time_limit
        self.head_movements = 0
        self.visited_positions = [head_position]
        self.finished_requests = []

    def finish_request(self, req: Request):
        self.visited_positions.append(req.position)
        self.finished_requests.append(req)

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

    def traverser_requests(self, requests_to_do: List[Request]) -> Request:
        for curr_request in requests_to_do:
            if curr_request.arrival_time <= self.head_movements:
                self.requests.remove(curr_request)
                self.head_movements += abs(curr_request.position - self.head_position)
                self.head_position = curr_request.position
                last_request = curr_request
                self.finish_request(curr_request)
        return last_request


    def scan(self):
        direction = 'l'
        requests_to_do = sorted([req for req in self.requests if req.position < self.head_position],
                                key=lambda x: x.position, reverse=True)
        while self.head_movements < self.time_limit and self.requests:
            last_request = self.traverser_requests(requests_to_do)
            if self.requests:
                if direction == 'l':
                    self.head_position = 0
                    self.visited_positions.append(self.head_position)
                    self.head_movements += abs(last_request.position - self.head_position)
                    requests_to_do = sorted([req for req in self.requests if req.position >= self.head_position],
                                            key=lambda x: x.position)
                    direction='r'
                elif direction == 'r':
                    self.head_position = self.disk_size
                    self.visited_positions.append(self.head_position)
                    self.head_movements += abs(last_request.position - self.head_position)
                    requests_to_do = sorted([req for req in self.requests if req.position < self.head_position],
                                            key=lambda x: x.position, reverse=True)
                    direction='l'
        return self.head_movements

    def cscan(self):
        while self.head_movements < self.time_limit and self.requests:
            right_requests = sorted([req for req in self.requests if req.position >= self.head_position])
            last_request = self.traverser_requests(right_requests)
            if self.requests:
                self.visited_positions.append(self.disk_size)
                self.head_movements += (self.disk_size - last_request.position) - 1
                self.head_position = 0
                self.head_movements += self.disk_size
                self.visited_positions.append(self.head_position)
        return self.head_movements
