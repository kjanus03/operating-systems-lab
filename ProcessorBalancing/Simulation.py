import copy

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Processor import Processor


class Simulation:
    def __init__(self, n_processors: int, time_limit: int, p: float, r:float,  z: int, max_request_length: int):
        self.n_processors: int = n_processors
        self.time: int = 0
        self.time_limit: int = time_limit
        self.p: float = p
        self.r: float = r
        self.processor_list: list[Processor] = []
        self.z: int = z
        self.max_request_length: int = max_request_length
        self.overloads: int = 0

    def generate_processors(self):
        for i in range(self.n_processors):
            mean = np.random.uniform(0.01, 0.3)
            variance = np.random.uniform(0.01, mean)
            frequency = np.random.uniform(0.001, 0.09)

            processor = Processor(i, frequency)
            processor.generate_requests(mean, variance, frequency, self.time_limit, self.max_request_length)
            self.processor_list.append(processor)

    def visualize_processors_by_gpu_share(self, n_processors: int):
        sns.set_palette("viridis")
        num_cols = int(np.ceil(n_processors / 2))  # Calculate number of rows for subplots
        fig, axs = plt.subplots(2, num_cols, figsize=(6 * num_cols, 12))  # Create subplots

        for i, p in enumerate(self.processor_list[:n_processors]):
            row = i % 2  # Calculate row index for subplot
            col = i // 2  # Calculate column index for subplot
            ax = axs[row, col]  # Select the appropriate subplot

            sns.histplot([r.share_of_CPU_processing_power for r in p.request_list], ax=ax, kde=True)
            ax.set_xlim(-0.25, 1)
            ax.set_xlabel("Share of CPU processing power", fontsize=14)
            ax.set_ylabel("Number of requests", fontsize=14)
            ax.set_title(f"Processor {p.id}", fontsize=16)

        plt.tight_layout()  # Adjust spacing between subplots
        plt.show()

    def approach1(self):
        while self.time < self.time_limit:
            for processor in self.processor_list:
                processor.cpu_load_in_time.append(processor.curr_cpu_load)
                if processor.request_list != []:

                    request = processor.request_list[0]

                    if request.arrival_time == self.time:
                        processor.request_list.remove(request)
                        if processor.curr_cpu_load >= self.p:
                            helped_flag = False
                            for _ in range(self.z):
                                random_processor = np.random.randint(0, self.n_processors)
                                processor.migration_queries += 1
                                if self.processor_list[random_processor].curr_cpu_load < self.p:
                                    request.migration_time = self.time
                                    self.processor_list[random_processor].taken_migrations+=1
                                    self.processor_list[random_processor].start_executing_request(request)
                                    helped_flag = True
                                    break
                            if not helped_flag:
                                processor.started_own_requests += 1
                                processor.start_executing_request(request)
                        else:
                            processor.started_own_requests += 1
                            processor.start_executing_request(request)
                        if processor.curr_cpu_load >= 1.0:
                            self.overloads += 1


                requests_to_remove = [request for request in processor.current_requests if request.end_time == self.time]
                for request in requests_to_remove:
                    processor.finish_executing_request(request)

            self.time += 1

    def approach2(self):
        self.z = self.n_processors
        self.approach1()

    def approach3(self):
        self.z = self.n_processors
        while self.time < self.time_limit:
            for i in range(self.n_processors):
                processor = self.processor_list[i]
                processor.cpu_load_in_time.append(processor.curr_cpu_load)
                if processor.request_list != []:
                    request = processor.request_list[0]
                    if request.arrival_time == self.time:
                        processor.request_list.remove(request)
                        if processor.curr_cpu_load >= self.p:
                            helped_flag = False
                            for _ in range(self.z):
                                random_processor = np.random.randint(0, self.n_processors)
                                processor.migration_queries += 1
                                if self.processor_list[random_processor].curr_cpu_load < self.p:
                                    request.migration_time = self.time
                                    self.processor_list[random_processor].taken_migrations+=1
                                    self.processor_list[random_processor].start_executing_request(request)
                                    helped_flag = True
                                    break
                            if not helped_flag:
                                processor.started_own_requests += 1
                                processor.start_executing_request(request)
                        else:
                            processor.started_own_requests += 1
                            processor.start_executing_request(request)
                        if processor.curr_cpu_load >= 1.0:
                            self.overloads += 1


                requests_to_remove = [request for request in processor.current_requests if request.end_time <= self.time]
                for request in requests_to_remove:
                    processor.finish_executing_request(request)

                if processor.curr_cpu_load < self.r:
                    for _ in range(5):
                        random_processor = self.processor_list[np.random.randint(0, self.n_processors)]
                        processor.migration_queries += 1
                        if random_processor.curr_cpu_load < self.p:
                            continue
                        if random_processor == processor:
                            continue
                        first_request = random_processor.current_requests[0]
                        processor.curr_cpu_load = sum([request.share_of_CPU_processing_power for request in processor.current_requests])
                        random_processor.give_away_request(first_request, processor)
                        processor.taken_migrations += 1
                        if processor.curr_cpu_load >= self.r:
                            break
            self.time += 1

    def turn_data_into_df(self) -> pd.DataFrame:
        data = []
        for processor in self.processor_list:
            data.append([processor.id, processor.started_own_requests, processor.taken_migrations, processor.migration_queries])
        df = pd.DataFrame(data, columns=['processor_id', 'started_own_requests', 'taken_migrations', 'migration_queries'])
        return df


    def visualize_processors_by_finished_requests(self):
        df = self.turn_data_into_df()
        df = df.sort_values(by=['started_own_requests'], ascending=True)
        ax = df.plot.barh(x='processor_id', y=['started_own_requests', 'taken_migrations', 'migration_queries'], stacked = True, rot=1, figsize=(20, 10), color=['#1f77b4', '#ff7f0e', '#2ca02c'])

        # make all fonts larger
        plt.setp(ax.get_xticklabels(), fontsize=16)
        plt.setp(ax.get_yticklabels(), fontsize=15)
        ax.set_xlabel("Number of requests", fontsize=24)
        ax.set_ylabel("Processor ID", fontsize=24)
        plt.tight_layout()
        plt.show()

    def visualize_processor_cpu_load_by_time(self, approach: int):
        colours = ["blue", "darkblue", "purple"]
        self.processor_list.sort(key=lambda x: len([i for i in x.cpu_load_in_time if i<0.1]))
        chosen_processor = self.processor_list[38]
        chosen_processor.cpu_load_in_time = [abs(x) for x in chosen_processor.cpu_load_in_time]
        df = pd.DataFrame(chosen_processor.cpu_load_in_time, columns=['cpu_load'])
        ax = df.plot.line(figsize=(20, 10), color=colours[approach-1], linewidth=3)
        ax.set_xlabel("Time", fontsize=24)
        ax.set_ylabel("CPU load", fontsize=24)
        ax.set_title(f"CPU load by time for a sample processor for approach {approach}", fontsize=24)
        # draw a red line on y=1.0
        plt.axhline(y=0.7, color='r', linestyle='-')
        plt.setp(ax.get_xticklabels(), fontsize=16)
        plt.setp(ax.get_yticklabels(), fontsize=15)
        plt.tight_layout()
        plt.show()

    def show_simulation_stats(self):
        cpu_loads_sum = sum([sum(processor.cpu_load_in_time)/self.time_limit for processor in self.processor_list])
        cpu_load_avg = cpu_loads_sum / self.n_processors
        print(f"Average cpu load: {cpu_load_avg}")

        # printing the mean deviation for the above average
        mean_deviation = 0
        for processor in self.processor_list:
            mean_deviation += abs(sum(processor.cpu_load_in_time)/self.time_limit - cpu_load_avg)
        mean_deviation /= self.n_processors
        print(f"Mean deviation: {mean_deviation}")

        all_migration_queries = sum([processor.migration_queries for processor in self.processor_list])
        print(f"Migration queries: {all_migration_queries}")
        all_taken_migrations = sum([processor.taken_migrations for processor in self.processor_list])
        print(f"Taken migrations: {all_taken_migrations}")
        print(f"Overloads: {self.overloads}")
        print(f'\n')


def main():
    n_processors = 40
    time_limit = 10000
    p = 0.7  # CPU load threshold
    r = 0.4 # minimal threshold for asking other CPUs for help in the 3rd approach
    z = 3  # number of attempts to pick a random CPU
    max_request_length = 70
    simulation = Simulation(n_processors, time_limit, p, r, z, max_request_length)
    simulation.generate_processors()
    simulation.visualize_processors_by_gpu_share(n_processors=10)
    sim1= copy.deepcopy(simulation)
    sim2 = copy.deepcopy(simulation)
    sim3 = copy.deepcopy(simulation)

    sim1.approach1()
    sim1.visualize_processors_by_finished_requests()
    sim1.show_simulation_stats()
    sim1.visualize_processor_cpu_load_by_time(1)

    sim2.approach2()
    sim2.visualize_processors_by_finished_requests()
    sim2.show_simulation_stats()
    sim2.visualize_processor_cpu_load_by_time(2)

    sim3.approach3()
    sim3.visualize_processors_by_finished_requests()
    sim3.show_simulation_stats()
    sim3.visualize_processor_cpu_load_by_time(3)
    plt.show()

if __name__ == "__main__":
    main()