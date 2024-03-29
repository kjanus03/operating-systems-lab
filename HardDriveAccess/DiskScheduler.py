from typing import List

import numpy as np

from Request import Request


class DiskScheduler:
    # disk_size: int - size of the disk
    def __init__(self, disk_size: int, requests: List[Request], head_position: int = 0, time_limit: int = 10000):
        self.disk_size = disk_size
        self.requests = requests
        self.head_position = head_position
        self.time_limit = time_limit
        self.head_movements = 0
        self.request_count = 0
        self.finished_requests = [Request(head_position)]
        self.missed_requests = []

    def finish_request(self, req: Request) -> None:
        self.request_count += 1
        req.wait_time = self.head_movements - req.arrival_time
        self.finished_requests.append(req)

    def any_deadlines(self) -> bool:
        return any([req.deadline > 0 for req in self.requests if req.arrival_time <= self.head_movements])

    def fcfs(self) -> int:
        self.requests.sort(key=lambda x: x.arrival_time)
        while self.head_movements < self.time_limit and self.requests:
            curr_request = self.requests.pop(0)
            self.head_movements += abs(curr_request.position - self.head_position)
            self.head_position = curr_request.position
            self.finish_request(curr_request)
        return self.head_movements

    def sstf(self) -> int:
        original_requests = self.requests.copy()
        while self.head_movements < self.time_limit:
            self.requests = [req for req in original_requests if req.arrival_time <= self.head_movements]
            if self.requests:
                curr_request = min(self.requests, key=lambda x: abs(x.position - self.head_position))
                original_requests.remove(curr_request)
                self.head_movements += abs(curr_request.position - self.head_position)
                self.head_position = curr_request.position
                self.finish_request(curr_request)
            else:
                break
        return self.head_movements

    def traverse_requests(self, requests_to_do: List[Request]) -> Request:
        last_request = Request(self.head_position, self.head_movements)
        for curr_request in requests_to_do:
            if curr_request.arrival_time <= self.head_movements:
                self.requests.remove(curr_request)
                self.head_movements += abs(curr_request.position - self.head_position)
                self.head_position = curr_request.position
                last_request = curr_request
                self.finish_request(curr_request)
        return last_request

    def scan(self) -> int:
        direction = 'l'
        requests_to_do = sorted([req for req in self.requests if req.position < self.head_position],
                                reverse=True)
        while self.head_movements < self.time_limit and self.requests:
            last_request = self.traverse_requests(requests_to_do)
            if self.requests:
                if direction == 'l':
                    self.head_position = 0
                    self.finished_requests.append(Request(self.head_position))
                    self.head_movements += abs(last_request.position - self.head_position)
                    requests_to_do = sorted([req for req in self.requests if req.position >= self.head_position],
                                            key=lambda x: x.position)
                    direction = 'r'
                elif direction == 'r':
                    self.head_position = self.disk_size
                    self.finished_requests.append(Request(self.head_position))
                    self.head_movements += abs(last_request.position - self.head_position)
                    requests_to_do = sorted([req for req in self.requests if req.position < self.head_position],
                                            key=lambda x: x.position, reverse=True)
                    direction = 'l'
        return self.head_movements

    def cscan(self) -> int:
        while self.head_movements < self.time_limit and self.requests:
            right_requests = sorted([req for req in self.requests if req.position >= self.head_position])
            last_request = self.traverse_requests(right_requests)
            if self.requests:
                self.finished_requests.append(Request(self.disk_size))
                self.head_movements += (self.disk_size - last_request.position) - 1
                self.head_position = 0
                self.finished_requests.append(Request(0))
        return self.head_movements

    """edf scan algorithm for request execution, works only for requests with deadlines, chooses the request with 
    the shortest deadline and tries to finish it. If the deadline is missed, the request is removed from the list of 
    requests and added to missed requests list."""

    def edf(self, original_requests: List[Request]) -> List[Request]:
        time = self.head_movements
        requests_to_do = [req for req in original_requests if
                          req.deadline > 0 and req.arrival_time <= self.head_movements]
        while requests_to_do and time < self.time_limit:
            curr_request = min(requests_to_do, key=lambda x: x.deadline)
            moves_per_request = 0
            while self.head_position != curr_request.position and moves_per_request <= curr_request.deadline:
                if self.head_position < curr_request.position:
                    self.head_position += 1
                    self.head_movements += 1
                elif self.head_position > curr_request.position:
                    self.head_position -= 1
                    self.head_movements += 1
                time += 1
                moves_per_request += 1
                if time > self.time_limit:
                    break

            original_requests.remove(curr_request)
            requests_to_do.remove(curr_request)
            if self.head_position == curr_request.position:
                self.finish_request(curr_request)
                self.head_position = curr_request.position
            else:
                self.missed_requests.append(curr_request)
        return original_requests

    def sstf_edf(self) -> int:
        original_requests = self.requests.copy()
        while self.head_movements < self.time_limit:
            self.requests = [req for req in original_requests if req.arrival_time <= self.head_movements]
            if self.requests:
                if self.any_deadlines():
                    original_requests = self.edf(original_requests)
                curr_request = min(self.requests, key=lambda x: abs(x.position - self.head_position))
                if curr_request in original_requests:
                    original_requests.remove(curr_request)
                self.head_movements += abs(curr_request.position - self.head_position)
                self.head_position = curr_request.position
                self.finish_request(curr_request)
            else:
                break
        return self.head_movements

    def fd_scan(self, original_requests: List[Request]) -> List[Request]:
        requests_to_do = [req for req in original_requests if
                          req.deadline > 0 and req.arrival_time <= self.head_movements]
        while requests_to_do and self.head_movements < self.time_limit:
            requests_to_do = [req for req in original_requests if
                              req.deadline > 0 and req.arrival_time <= self.head_movements]
            curr_request = min(requests_to_do, key=lambda x: x.deadline)
            # ignoring unfeasible requests
            if curr_request.deadline > abs(curr_request.position - self.head_position):
                original_requests.remove(curr_request)
                requests_to_do.remove(curr_request)
                self.missed_requests.append(curr_request)
                continue
            while self.head_position != curr_request.position and self.head_movements < self.time_limit:
                for request in original_requests:
                    if request.position == self.head_position and request.arrival_time <= self.head_movements:
                        if request in requests_to_do:
                            requests_to_do.remove(request)
                        original_requests.remove(request)
                        self.finish_request(request)
                if self.head_position < curr_request.position:
                    self.head_position += 1
                    self.head_movements += 1
                elif self.head_position > curr_request.position:
                    self.head_position -= 1
                    self.head_movements += 1
            if self.head_movements > self.time_limit:
                break
            original_requests.remove(curr_request)
            requests_to_do.remove(curr_request)
            self.finish_request(curr_request)
        return original_requests

    def sstf_fd_scan(self) -> int:
        original_requests = self.requests.copy()
        while self.head_movements < self.time_limit:
            self.requests = [req for req in original_requests if req.arrival_time <= self.head_movements]
            if self.requests:
                if self.any_deadlines():
                    original_requests = self.fd_scan(original_requests)
                curr_request = min(self.requests, key=lambda x: abs(x.position - self.head_position))
                if curr_request in original_requests:
                    original_requests.remove(curr_request)
                self.head_movements += abs(curr_request.position - self.head_position)
                self.head_position = curr_request.position
                self.finish_request(curr_request)
            else:
                break
        return self.head_movements

    def moves_per_request(self) -> float:
        return self.head_movements / self.request_count

    def mean_wait_time(self) -> float:
        return float(np.mean([req.wait_time for req in self.finished_requests]))

    def finished_deadline_requests(self) -> int:
        return len([req for req in self.finished_requests if req.deadline > 0])

    def missed_deadline_requests(self) -> int:
        return len(self.missed_requests)
