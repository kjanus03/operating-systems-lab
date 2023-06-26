import random
import warnings

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import Process


class Simulation:
    def __init__(self, num_of_processes: int, num_of_frames: int, num_of_pages: int, time_window: int):
        self.processes_done: set[Process] = set()
        self.num_of_processes = num_of_processes
        self.num_of_frames = num_of_frames
        self.num_of_pages = num_of_pages
        self.time_window = time_window
        self.page_faults_per_step = []
        self.all_page_faults = 0
        self.processes_aborted = set()
        self.processes_suspended = set()
        self.faults_table: list[bool] = []

        # processes currently executing
        self.current_processes: set[Process] = set()

    def generate_current_processes(self) -> None:
        curr_id = len(self.processes_done)
        current_processes_size = 20
        page_intervals = Simulation.divide_range(self.num_of_pages, current_processes_size, 0.7)
        if len(page_intervals) != current_processes_size:
            page_intervals[-1] = (page_intervals[-1][0], page_intervals[-1][0] + int(
                np.ceil((self.num_of_pages - page_intervals[-1][0]) * 0.7)))
            page_intervals.append((page_intervals[-1][0] + int(
                np.ceil((self.num_of_pages - page_intervals[-1][0]) * 0.7)) + 1, self.num_of_pages))
        for i in range(current_processes_size):
            _id = curr_id + i
            self.current_processes.add(Process.Process(_id, page_intervals[i][0], page_intervals[i][1]))

    @staticmethod
    def divide_range(num_of_pages, num_intervals, min_span_percentage):
        num_intervals += 1
        intervals = []
        remaining_range = num_of_pages
        remaining_intervals = num_intervals
        total_span = int(num_of_pages * min_span_percentage)

        while remaining_intervals >= 0:
            # Calculate the minimum and maximum span values for the current interval
            min_span = max(total_span - remaining_range * (remaining_intervals - 1), 1)
            if remaining_intervals == 1:
                max_span = remaining_range
            else:
                max_span = min(remaining_range // (remaining_intervals - 1), total_span)

            # Ensure the minimum and maximum values are valid
            if min_span > max_span:
                break

            # Generate a random interval within the calculated bounds
            interval_span = random.randint(min_span, max_span)
            interval = num_of_pages - remaining_range + 1

            # Add the interval to the list
            intervals.append((interval, interval + interval_span - 1))

            # Update the remaining range and intervals
            remaining_range -= interval_span
            remaining_intervals -= 1

        # Add the last interval to span the remaining range
        intervals.append((num_of_pages - remaining_range + 1, num_of_pages))

        return intervals

    # function for drawing the reference chain of each of the current processes
    # the fuction should employ a scatterplot with each process getting a unique colour
    def visualize_processes(self):
        p_list = sorted([p for p in self.current_processes], key=lambda x: x._id)
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(10, 10))
        for p in p_list:
            if p.page_references:
                ax.scatter(p.page_references,
                           range(min(p.page_references), min(p.page_references) + len(p.page_references)),
                           label=f"Process {p._id}")
        plt.legend()
        plt.show()

    def LRU(self, process: Process):
        page_breaks = 0
        use_order = []
        physical_memory_size = len(process.physical_memory)
        for page in process.page_references:
            self.page_faults_per_step.append(page_breaks)
            if page not in process.physical_memory:
                page_breaks += 1
                self.faults_table.append(True)
                if page_breaks <= physical_memory_size:
                    process.physical_memory.append(page)
                    use_order.append(process.physical_memory.index(page))
                else:
                    index = use_order[0]
                    process.physical_memory[index] = page
                    index_to_move = use_order.pop(use_order.index(process.physical_memory.index(page)))
                    use_order.insert(self.num_of_pages, index_to_move)
            else:
                index_to_move = use_order.pop(use_order.index(process.physical_memory.index(page)))
                use_order.insert(self.num_of_pages, index_to_move)
                self.faults_table.append(False)
        self.all_page_faults += page_breaks
        process.page_breaks = page_breaks

    def Control_LRU(self, process: Process, low: int, u: int, high: int) -> int:
        page_breaks = 0
        use_order = []
        physical_memory_size = len(process.physical_memory)
        abort_falg = False
        for page in process.page_references:
            self.page_faults_per_step.append(page_breaks)
            if page not in process.physical_memory:
                page_breaks += 1

                self.faults_table.append(True)
                if page_breaks <= physical_memory_size:
                    process.physical_memory.append(page)
                    use_order.append(process.physical_memory.index(page))
                else:
                    index = use_order[0]
                    process.physical_memory[index] = page
                    index_to_move = use_order.pop(use_order.index(process.physical_memory.index(page)))
                    use_order.insert(self.num_of_pages, index_to_move)
            else:
                self.faults_table.append(False)
                index_to_move = use_order.pop(use_order.index(process.physical_memory.index(page)))
                use_order.insert(self.num_of_pages, index_to_move)
            ppf = page_breaks / self.time_window
            if ppf < low:
                process.physical_memory_size -= 1
            elif ppf > high:
                self.processes_aborted.add(process)
                abort_falg = True
                break
            elif ppf > u:
                process.physical_memory_size += 1
        if not abort_falg:
            self.all_page_faults += page_breaks
        process.page_breaks = page_breaks

    def WorkingSet_LRU(self):

        # Obliczanie WSS dla każdego procesu
        for process in self.current_processes:
            WSS = len(set(process.page_references))
            process.set_physical_memory(WSS)

        # Obliczanie liczby dostępnych ramek w systemie
        available_frames = self.num_of_frames - sum(process.physical_memory_size for process in self.current_processes)

        while True:
            if not self.current_processes:
                break
            # Obliczanie liczby aktualnie potrzebnych ramek dla każdego procesu
            D = sum(process.physical_memory_size for process in self.current_processes)
            if D <= available_frames:
                # Przydzielanie ramek do procesów proporcjonalnie do ich WSS
                for process in self.current_processes:
                    if sum(p.physical_memory_size for p in self.current_processes) == 0:
                        process_frames = 0
                    else:
                        process_frames = int(
                            process.physical_memory_size * D / sum(
                                p.physical_memory_size for p in self.current_processes))
                    process.set_physical_memory(process_frames)
                    self.LRU(process)
                    self.processes_done.add(process)
                self.current_processes = set()
            else:
                # znajduje najwiekszy wss i zatrzymuje
                process_to_suspend = max(self.current_processes, key=lambda p: p.physical_memory_size)
                self.current_processes.remove(process_to_suspend)
                self.processes_suspended.add(process_to_suspend)
                available_frames += process_to_suspend.physical_memory_size

                process_to_suspend.page_breaks += 1
                self.all_page_faults += 1

    def equal_allocation(self):
        self.processes_done = set()
        self.all_page_faults = 0
        self.faults_table = []
        # f is the number of frames given to each process
        f = self.num_of_frames // len(self.current_processes)

        while len(self.processes_done) < self.num_of_processes:
            for p in self.current_processes:
                p.set_physical_memory(f)
                self.LRU(p)
                self.processes_done.add(p)
            self.current_processes = set()
            self.generate_current_processes()

    def proportional_allocation(self):
        self.processes_done = set()
        self.faults_table = []
        self.all_page_faults = 0
        while len(self.processes_done) < self.num_of_processes:
            for p in self.current_processes:
                f = np.ceil(len(p.page_references) / len(self.current_processes)).astype(int)
                p.set_physical_memory(f)
                self.LRU(p)
                self.processes_done.add(p)
            self.current_processes = set()
            self.generate_current_processes()

    def pageFaultFrequencyControl(self, low: int, u: int, high: int):
        self.processes_done = set()
        self.faults_table = []
        self.processes_aborted = set()
        self.all_page_faults = 0
        # f is the number of frames given to each process
        f = self.num_of_frames // len(self.current_processes)

        while len(self.processes_done) + len(self.processes_aborted) < self.num_of_processes:
            for p in self.current_processes:
                p.set_physical_memory(f)
                self.Control_LRU(p, low, u, high)
                self.processes_done.add(p)
            self.current_processes = set()
            self.generate_current_processes()

    def workingSetModel(self):
        self.processes_done = set()
        self.faults_table = []
        self.all_page_faults = 0
        while len(self.processes_done) < self.num_of_processes:
            self.WorkingSet_LRU()
            self.current_processes = set()
            self.generate_current_processes()


def visualize_results(alg1: int, alg2: int, alg3: int, alg4: int):
    labels = ['Equal Allocation', 'Proportional Allocation', 'Page Fault Frequency Control', 'Working Set Model']
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))
    rects1 = ax.bar(x - width / 2, [alg1, alg2, alg3, alg4], width, label='Page Breaks Per Process')
    ax.set_ylabel('Page Breaks Per Process')
    ax.set_title('Page Breaks Per Process')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.show()


def policz_szamotania(fault_table1: list[bool], fault_table2: list[bool], fault_table3: list[bool], fault_table4: list[bool], time_window: int):
    szamotania = [[], [], [], []]
    for i, ft in enumerate([fault_table1, fault_table2, fault_table3, fault_table4]):
        for j in range(0, len(ft), time_window):
            szamotania[i].append(sum(ft[j:j+time_window]))
    return szamotania


def visualize_faults(szamotania: list[list[int]]):
    #lineplot of the szamotania per list
    plt.figure(figsize=(24, 14))
    labels = ['Equal Allocation', 'Proportional Allocation', 'Page Fault Frequency Control', 'Working Set Model']
    x = np.arange(len(szamotania[0]))
    for i, s in enumerate(szamotania):
        sns.scatterplot(x, s, label=labels[i], s=100)
        sns.lineplot(x, s)

    plt.xlabel('Time', fontsize=26)
    plt.ylabel('Page Breaks', fontsize=26)
    plt.title('Szamotania', fontsize=40)
    plt.legend(prop = { "size": 28 }, loc='lower left', fontsize=26)
    plt.savefig('szamotania.png')
    plt.show()


def main():
    warnings.simplefilter(action='ignore', category=FutureWarning)

    num_of_pages = 2000
    num_of_frames = 200
    num_of_processes = 1000
    time_window = 10
    szamotania_time_window = 800

    sim1 = Simulation(num_of_processes, num_of_frames, num_of_pages, time_window)
    sim1.generate_current_processes()
    sim1.visualize_processes()

    sim1.equal_allocation()
    print(list(sim1.processes_done)[0])
    print(list(sim1.processes_done)[1])

    result1 = sim1.all_page_faults / num_of_processes
    fault_table1 = sim1.faults_table
    print(f"Equal allocation page breaks per process: {result1}")

    sim1.proportional_allocation()
    result2 = sim1.all_page_faults / num_of_processes
    fault_table2 = sim1.faults_table
    print(f"Proportional allocation page breaks per process: {result2}")

    sim1.pageFaultFrequencyControl(2, 6, 10)
    result3 = sim1.all_page_faults / len(sim1.processes_done)
    fault_table3 = sim1.faults_table
    print(f"Page faults frequency control page breaks per process: {result3}")
    print(f"Number of aborted processes: {len(sim1.processes_aborted)} out of {num_of_processes}\n")

    sim1.workingSetModel()
    result4 = sim1.all_page_faults / num_of_processes
    fault_table4 = sim1.faults_table
    print(f"Working set model page breaks per process: {result4}")
    print(f"Number of process suspensions: {len(sim1.processes_suspended)}")

    visualize_results(result1, result2, result3, result4)

    for ft in [fault_table1, fault_table2, fault_table3, fault_table4]:
        if len(ft)<len(max([fault_table1, fault_table2, fault_table3, fault_table4], key=lambda x: len(x))):
            ft.extend([False]*(len(max([fault_table1, fault_table2, fault_table3, fault_table4], key=lambda x: len(x)))-len(ft)))


    szamotania = policz_szamotania(fault_table1, fault_table2, fault_table3, fault_table4, szamotania_time_window)
    szamotanie_limit = int(0.7*szamotania_time_window)
    print(f"\nNumber of szamotanias for equal allocation: {len([a for a in szamotania[0] if a>szamotanie_limit])}")
    print(f"Number of szamotanias for proportional allocation: {len([a for a in szamotania[1] if a>szamotanie_limit])}")
    print(f"Number of szamotanias for page fault frequency control: {len([a for a in szamotania[2] if a>szamotanie_limit])}")
    print(f"Number of szamotanias for working set model: {len([a for a in szamotania[3] if a>szamotanie_limit])}")
    visualize_faults(szamotania)


main()


