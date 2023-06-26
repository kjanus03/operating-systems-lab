import random

import matplotlib.pyplot as plt
import seaborn as sns


def generate_a_ref_chain(length: int, virtual_memory_size: int, locality_count: int, locality_density: float) -> list[int]:
    dzielnik = 50*locality_density
    ref_chain = []
    last_localisty_spot = virtual_memory_size // 2
    for i in range(locality_count):
        # getting the locality spot in our desired range(1, length - 1)
        if last_localisty_spot < virtual_memory_size // 6:
            locality_spot = random.randint(0, virtual_memory_size // 3)
        elif last_localisty_spot > length - virtual_memory_size // 6:
            locality_spot = random.randint(length - virtual_memory_size // 3, length - 1)
        else:
            locality_spot = random.randint(last_localisty_spot - virtual_memory_size // 6,
                                           last_localisty_spot + virtual_memory_size // 6)
        last_localisty_spot = locality_spot
        loc_list = [random.randint(locality_spot - int(virtual_memory_size // dzielnik), locality_spot + int(virtual_memory_size // dzielnik))
                    for _ in range(length // locality_count)]
        loc_list = [1 if x < 1 else length - 1 if x > length - 1 else x for x in loc_list]
        ref_chain += loc_list
    return ref_chain


def visualize_a_ref_chain(ref_chain: list[int]):
    sns.set_theme(style="white")
    fig = plt.figure()
    ax = sns.scatterplot(x=range(len(ref_chain)), y=ref_chain)
    ax.set(xlabel="Numer odwołania", ylabel="Strona")
    plt.show()


class Simulation:
    def __init__(self, virtual_memory_size: int, physical_memory_size: int, ref_chain_length: int,
                 ref_chain: list = None):
        # liczba stron w pamieci wirtualnej
        self.virtual_memory_size = virtual_memory_size
        # liczba ramek
        self.physical_memory_size = physical_memory_size
        # ramki
        self.physical_memory = [0 for i in range(physical_memory_size)]
        # dlugosc lancucha odwolan
        self.ref_chain_length = ref_chain_length
        if ref_chain:
            self.ref_chain = ref_chain
        else:
            self.ref_chain = generate_a_ref_chain(ref_chain_length, virtual_memory_size, 20)
        self.page_faults_per_step: list[int] = []

    def FIFO(self) -> int:
        # page faults
        page_faults = 0
        # indeks najstarszej strony
        oldest = 0
        for page in self.ref_chain:
            self.page_faults_per_step.append(page_faults)
            if page not in self.physical_memory:
                page_faults += 1
                # zastepujemy najstarsza strone
                self.physical_memory[oldest] = page
                oldest = (oldest + 1) % self.physical_memory_size

        return page_faults

    def find_page_to_replace(self, page: int, physical_memory: list[int], ref_chain: list[int]) -> int:
        # domyslny indeks na ostatnia strone
        index = -1
        # jesli jest srona, ktorej nie bedzie uzywac w przyszlosci wcale to wybieramy ja
        for i in range(len(physical_memory)):
            if physical_memory[i] not in ref_chain:
                index = i
                break
        # if all pages in physical memory will be used in the future
        if index == -1:
            # szukamy indeksu strony, ktora najdluzej nie bedzie uzywana
            max = 0
            for i in range(len(physical_memory)):
                page_index = ref_chain.index(physical_memory[i])
                if page_index > max:
                    max = page_index
                    index = i
        return index

    def OPT(self) -> int:
        page_faults = 0

        for i in range(len(self.ref_chain)):
            self.page_faults_per_step.append(page_faults)
            page = self.ref_chain[i]
            # jesli strony nie ma w pamieci fizycznej
            if page not in self.physical_memory:
                page_faults += 1

                # jesli jest jakas wolna ramka
                if len(self.physical_memory) < self.physical_memory_size:
                    self.physical_memory.append(page)

                # jesli nie ma wolnych ramek to wyszukujemy strone do zastapienia (ta ktora najdluzej nie bedzie uzywana)
                else:
                    self.physical_memory[
                        self.find_page_to_replace(page, self.physical_memory, ref_chain=self.ref_chain[i:])] = page
        return page_faults

    def LRU(self) -> int:
        page_breaks = 0
        use_order = []
        for page in self.ref_chain:
            self.page_faults_per_step.append(page_breaks)
            if page not in self.physical_memory:
                page_breaks += 1
                if page_breaks <= self.physical_memory_size:
                    self.physical_memory.append(page)
                    use_order.append(self.physical_memory.index(page))
                else:
                    index = use_order[0]
                    self.physical_memory[index] = page
                    index_to_move = use_order.pop(use_order.index(self.physical_memory.index(page)))
                    use_order.insert(self.virtual_memory_size, index_to_move)
            else:
                index_to_move = use_order.pop(use_order.index(self.physical_memory.index(page)))
                use_order.insert(self.virtual_memory_size, index_to_move)
        return page_breaks

    def ApproximateLRU(self):
        page_breaks = 0
        use_order = []
        use_order_bits = []
        for page in self.ref_chain:
            self.page_faults_per_step.append(page_breaks)
            if page not in self.physical_memory:
                page_breaks += 1
                if page_breaks <= self.physical_memory_size:
                    self.physical_memory.append(page)
                    use_order.append(self.physical_memory.index(page))
                    use_order_bits.append(1)
                else:
                    index = use_order[0]
                    if use_order_bits[0] == 1:
                        use_order_bits[0] = 0
                        use_order.insert(self.virtual_memory_size, use_order.pop(0))
                        self.physical_memory[index] = page
                        use_order_bits.append(1)
                    else:
                        use_order.pop(0)
                        use_order.insert(self.virtual_memory_size, use_order.pop(0))
                        use_order_bits.pop(0)
                        self.physical_memory[index] = page
                        use_order.insert(self.virtual_memory_size, index)
        return page_breaks

    def RAND(self):
        page_breaks = 0
        for page in self.ref_chain:
            self.page_faults_per_step.append(page_breaks)
            if page not in self.physical_memory:
                page_breaks += 1
                index_to_replace_with_the_page = random.randint(0, self.physical_memory_size - 1)
                self.physical_memory[index_to_replace_with_the_page] = page
        return page_breaks


def main() -> None:
    example_sim = Simulation(5, 4, 12, [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5])
    print(example_sim.LRU())

    # LICZBA STRON
    virtual_memory_size = 300
    # LICZBA RAMEK
    physical_memory_size = 20
    # DLUGOSC CIAGU ODWOLAN
    ref_chain_length = 1_000
    # LICZBA LOKALNOSCI
    locality_count = 10
    # GESTOSC LOKALNOSCI (blizej 1-> gesciej)
    locality_density = 0.4
    ref_chain = generate_a_ref_chain(ref_chain_length, virtual_memory_size, locality_count=locality_count, locality_density=locality_density)
    visualize_a_ref_chain(ref_chain)

    sim = Simulation(virtual_memory_size, physical_memory_size, ref_chain_length=0, ref_chain=ref_chain)
    fifo_result = sim.FIFO()
    print("FIFO: ", fifo_result)

    sim2 = Simulation(virtual_memory_size, physical_memory_size, ref_chain_length=0, ref_chain=ref_chain)
    opt_result = sim2.OPT()
    print("OPT: ", opt_result)

    sim3 = Simulation(virtual_memory_size, physical_memory_size, ref_chain_length=0, ref_chain=ref_chain)
    lru_result = sim3.LRU()
    print("LRU: ", lru_result)

    sim4 = Simulation(virtual_memory_size, physical_memory_size, ref_chain_length=0, ref_chain=ref_chain)
    alru_result = sim4.ApproximateLRU()
    print("ARU: ", alru_result)

    sim5 = Simulation(virtual_memory_size, physical_memory_size, ref_chain_length=0, ref_chain=ref_chain)
    rand_result = sim5.RAND()
    print("RAND: ", rand_result)

    page_faults_per_step_per_algorithm = [simulation.page_faults_per_step for simulation in
                                          (sim, sim2, sim3, sim4, sim5)]

    results = [fifo_result, opt_result, alru_result, lru_result, rand_result]
    etiquetas = ["FIFO", "OPT", "ALRU", "LRU", "RAND"]

    sns.barplot(x=etiquetas, y=results)
    plt.title("Page faults")
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 10))
    for i in range(5):
        sns.lineplot(x=range(len(ref_chain)), y=page_faults_per_step_per_algorithm[i], ax=ax, linewidth=2)
    ax.legend(etiquetas)
    plt.title("Page faults per step", fontsize=20)
    plt.savefig("page_faults_per_step.png")
    plt.show()
    plt.show()


main()
