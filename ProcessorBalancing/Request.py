import numpy as np

class Request:
    def __init__(self, request_id: int, arrival_time: int, share_of_CPU_processing_power: float, max_request_length: int):
        self.request_id = request_id
        self.arrival_time = arrival_time
        self.end_time = arrival_time + np.random.randint(2, max_request_length)
        self.migration_time = 0
        self.share_of_CPU_processing_power = share_of_CPU_processing_power
        self.just_given_away = False


    def __repr__(self):
        return f"Request ID: {self.request_id}\n" \
               f"Share of CPU processing power: {self.share_of_CPU_processing_power}\n" \
               f"Arrival time: {self.arrival_time}\n" \
                f"Migration time: {self.migration_time}\n" \
                f"End time: {self.end_time}\n"

    def __eq__(self, other):
        return self.request_id == other.request_id


