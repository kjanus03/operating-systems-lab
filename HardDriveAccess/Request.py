class Request:
    def __init__(self, position: int, arrival_time: int = 0, deadline: int = 0):
        self.position = position
        self.arrival_time = arrival_time
        self.wait_time = 0
        self.deadline = deadline

    def __eq__(self, other):
        return self.position == other.position and self.arrival_time == other.arrival_time and self.deadline == other.deadline

    def __lt__(self, other):
        return self.position < other.position

    def __le__(self, other):
        return self.position <= other.position

    def __gt__(self, other):
        return self.position > other.position

    def __ge__(self, other):
        return self.position >= other.position

    def __repr__(self):
        return f'Position: {self.position}\nArrival time: {self.arrival_time}\nDeadline: {self.deadline}\n'
