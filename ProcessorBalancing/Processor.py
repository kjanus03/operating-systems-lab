import numpy as np
from Request import Request


class Processor:
    def __init__(self, id: int, frequency: float = 1):
        self.id = id
        self.frequency = frequency
        self.req_gap = 1//frequency
        self.request_list: list[Request] = []
        self.current_requests: list[Request] = []
        self.finished_requests: list[Request] = []
        self.curr_cpu_load: float = 0
        self.migration_queries: int = 0
        self.started_own_requests: int = 0
        self.taken_migrations: int = 0
        self.given_away_requests: int = 0
        self.cpu_load_in_time: list[float] = []

    def generate_requests(self, mean: float, variance: float, frequency: float, time_limit: int, max_request_length: int):
        n_requests = int(time_limit * self.frequency)
        req_gap = 1 // frequency
        mu = np.log(mean ** 2 / np.sqrt(variance + mean ** 2))
        sigma = np.sqrt(np.log(variance / mean ** 2 + 1))
        # procesy  losowane zgodnie z rozkladem normalnym
        self.request_list = [Request(i, int(i*req_gap), np.random.lognormal(mu, sigma), max_request_length) for i in range(n_requests)]

    def start_executing_request(self, request: Request):
        self.current_requests.append(request)
        self.curr_cpu_load += request.share_of_CPU_processing_power

    def finish_executing_request(self, request: Request):
        self.current_requests.remove(request)
        self.curr_cpu_load -= request.share_of_CPU_processing_power
        self.finished_requests.append(request)

    def give_away_request(self, request: Request, processor):
        self.current_requests.remove(request)
        self.curr_cpu_load -= request.share_of_CPU_processing_power
        request.just_given_away = True
        processor.start_executing_request(request)
        processor.taken_migrations += 1
        self.given_away_requests += 1

    def __eq__(self, other):
        return self.id == other.id


    def __repr__(self):
        return f"Processor ID: {self.id}\n" \
               f"Frequency: {self.frequency}\n" \
                f"Current CPU load: {self.curr_cpu_load}\n" \
                f"Migration queries: {self.migration_queries}\n" \
                f"Started own requests: {self.started_own_requests}\n" \
                f"Taken migrations: {self.taken_migrations}\n" \
                f"Started but not finished requests: {len(self.current_requests)}\n" \
                f"Given away requests: {self.given_away_requests}\n" \
                f"Finished requests: {len(self.finished_requests)}\n" \
