import random
import numpy as np


class Process:
    def __init__(self, _id: int, low_ref: int, max_ref: int):
        self._id = _id
        self.max_ref = max_ref
        self.low_ref = low_ref
        self.num_of_refs = random.randint(np.ceil((max_ref - low_ref) * 0.6), max_ref - low_ref)
        self.page_references = [random.randint(low_ref, max_ref) for _ in range(self.num_of_refs)]
        # f to liczba ramek
        self.physical_memory = []
        self.page_breaks = 0
        self.physical_memory_size = 0

    def __str__(self):
        return f"Process id: {self._id}\n" \
               f"References interval: {self.low_ref} - {self.max_ref}\n" \
               f"Number of references: {self.num_of_refs}\n" \
               f"References: {self.page_references}\n"\
               f"Number of frames: {self.physical_memory_size}\n"\
               f"Page breaks: {self.page_breaks}\n"

    def set_physical_memory(self, f):
        self.physical_memory = [0 for _ in range(f)]
        self.physical_memory_size = f

