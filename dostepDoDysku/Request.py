class Request:
    def __init__(self, position: int, arrival_time: int = 0, real_time: bool = False):
        self.position = position
        self.arrival_time = arrival_time
        self.real_time = real_time

    def __eq__(self, other):
        return self.position == other.position and self.arrival_time == other.arrival_time and\
               self.real_time == other.real_time

    def __lt__(self, other):
        return self.position < other.position

    def __le__(self, other):
        return self.position <= other.position

    def __gt__(self, other):
        return self.position > other.position

    def __ge__(self, other):
        return self.position >= other.position

    def __repr__(self):
        return f'Position: {self.position}\nArrival time: {self.arrival_time}\nReal time: {self.real_time}\n'
