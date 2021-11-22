import math
import random

import numpy as np
from numpy import linalg


def rosenbrock_func(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


class AIS:
    def __init__(self, func):
        self.func = func
        self.s_b = 50
        self.__COUNT_GENES = 16
        self.__min = -5
        self.__max = 5

        self.__SIZE_BEST_ANTIBODIES = 10
        self.__COUNT_CLONES = 5
        self.__SELECTION_RATE = 10
        self.__DISTRIBUTION_CLONES = self.__calc_distribution_clones()
        self.__COEFF_MUTATION = 0.02
        self.__COEFF_DEATH = 9.5
        self.__COEFF_COMPRESSION = 0.02

        self.__SIZE_ANTIBODIES = 50
        self.__antibodies = []

        self.__SIZE_ANTIGENS = 10
        self.__antigens = []

        self.__population_of_clones = []
        self.__population_of_memory = []

        self.__best_agent = [None, None, None]

        self.__init_ais()

    def get_antibodies(self):
        return self.__antibodies

    def get_antigens(self):
        return self.__antigens

    def max_bg_affinity(self):
        matrix_affinity = self.__bg_affinity()

        max_affinity_els = []
        for line in matrix_affinity:
            dict_affinity = {}
            ind_max = np.argpartition(line, -self.__SIZE_BEST_ANTIBODIES)[-self.__SIZE_BEST_ANTIBODIES:]

            for ind in ind_max:
                dict_affinity[line[ind]] = np.array(self.__antibodies)[ind]

            max_affinity_els.append(dict_affinity)

        return max_affinity_els

    def clone_best_antibodies(self, affinity_best):
        self.__population_of_clones = []

        for d in affinity_best:
            cur_clones = []
            for aff, distrib in zip(sorted(d.keys(), reverse=True), self.__DISTRIBUTION_CLONES):
                for _ in range(distrib):
                    cur_clones.append(d[aff].copy())

            self.__population_of_clones.append(cur_clones)

    def mutation_clones(self):
        for cur_clones in self.__population_of_clones:
            for point in cur_clones:
                for i in range(len(point)):
                    cod = self.__code_point(point[i])

                    cod_mut = ''
                    for ch in cod:
                        if random.random() < self.__COEFF_MUTATION:
                            cod_mut += str(int(not(int(ch))))
                        else:
                            cod_mut += ch

                    cod_mut = int(cod_mut, 2)

                    point[i] = self.__decoding_agent(cod_mut)

    def create_population_of_memory(self):
        self.__population_of_memory = []
        for i in range(len(self.__antigens)):
            affinity = self.__affinity(self.__antigens[i], self.__population_of_clones[i])
            ind_max = np.argpartition(affinity, -self.__SELECTION_RATE)[-self.__SELECTION_RATE:]

            for ind in ind_max:
                if affinity[ind] > self.__COEFF_DEATH:
                    self.__population_of_memory.append(self.__population_of_clones[i][ind])

    def clonal_compression(self):
        selected_agents = self.__compression(self.__population_of_memory)

        for agent in selected_agents:
            self.__antibodies.append(agent)

    def network_compression(self):
        selected_agents = self.__compression(self.__antibodies)
        self.__antibodies = selected_agents

    def regeneration(self):
        if len(self.__antibodies) < self.__SIZE_ANTIBODIES:
            while len(self.__antibodies) != self.__SIZE_ANTIBODIES:
                x = round(np.random.uniform(self.__min, self.__max), 4)
                y = round(np.random.uniform(self.__min, self.__max), 4)
                self.__antibodies.append([x, y])
        else:
            while len(self.__antibodies) != self.__SIZE_ANTIBODIES:
                matrix_affinity = self.__bb_affinity(self.__antibodies)
                min_affinity = 100
                min_index = None

                for line in matrix_affinity:
                    ind, _ = min(enumerate(line), key=lambda i_v: i_v[1])
                    if line[ind] < min_affinity:
                        min_affinity = line[ind]
                        min_index = ind

                del self.__antibodies[min_index]

    def get_best_agent(self):
        for agent in self.__antibodies:
            new_val = self.func(agent[0], agent[1])
            if self.__best_agent[2] is None or new_val < self.__best_agent[2]:
                self.__best_agent[0] = agent[0]
                self.__best_agent[1] = agent[1]
                self.__best_agent[2] = new_val

        return tuple(self.__best_agent)

    def __init_ais(self):
        for _ in range(self.__SIZE_ANTIBODIES):
            x = round(np.random.uniform(self.__min, self.__max), 4)
            y = round(np.random.uniform(self.__min, self.__max), 4)
            self.__antibodies.append([x, y])

        for _ in range(self.__SIZE_ANTIGENS):
            x = round(np.random.uniform(self.__min, self.__max), 4)
            y = round(np.random.uniform(self.__min, self.__max), 4)
            self.__antigens.append(np.array([x, y]))

    def __hamming_distance(self, first_value, second_value):
        ham_dist = 0
        for ch1, ch2 in zip(first_value, second_value):
            if ch1 != ch2:
                ham_dist += 1

        return ham_dist

    def __calc_distribution_clones(self):
        distribution = [0 for _ in range(self.__SIZE_BEST_ANTIBODIES)]
        count_clones_all = self.__COUNT_CLONES * self.__SIZE_BEST_ANTIBODIES
        cur_count_clones = 0
        bound = self.__SIZE_BEST_ANTIBODIES

        while cur_count_clones != count_clones_all:
            for i in range(bound):
                if cur_count_clones == count_clones_all:
                    break

                distribution[i] += 1
                cur_count_clones += 1

            bound -= 1

        return distribution

    def __bb_affinity(self, antibodies):
        affinity_matrix = []

        for first_antibody in antibodies:
            distances = self.__affinity(first_antibody, antibodies)

            affinity_matrix.append(np.array(distances))

        return affinity_matrix

    def __bg_affinity(self):
        affinity_matrix = []

        for antigen in self.__antigens:
            distances = self.__affinity(antigen, self.__antibodies)

            affinity_matrix.append(np.array(distances))

        return affinity_matrix

    def __affinity(self, agent, agents):
        affinity = []

        cod_antigen_x = self.__code_point(agent[0])
        cod_antigen_y = self.__code_point(agent[1])

        for el in agents:
            cod_antibody_x = self.__code_point(el[0])
            cod_antibody_y = self.__code_point(el[1])

            ham_x = self.__hamming_distance(cod_antigen_x, cod_antibody_x)
            ham_y = self.__hamming_distance(cod_antigen_y, cod_antibody_y)

            affinity.append(ham_x + ham_y)

        return affinity

    def __compression(self, population):
        affinity_memory = self.__bb_affinity(population)
        cur_population = []

        for affinity in affinity_memory:
            for cell_memory, cur_affinity in zip(self.__population_of_memory, affinity):
                if cur_affinity > self.__COEFF_COMPRESSION and (list(cell_memory) not in cur_population):
                    cur_population.append(list(cell_memory))

        return cur_population

    def __code_point(self, point):
        cod = format(self.__coding_agent(point), 'b')
        return '0' * (self.__COUNT_GENES - len(cod)) + cod

    def __coding_agent(self, agent):
        return math.trunc(((agent - self.__min) * (2 ** self.__COUNT_GENES - 1)) / (self.__max - self.__min))

    def __decoding_agent(self, agent):
        return round((agent * (self.__max - self.__min)) / (2 ** self.__COUNT_GENES - 1) + self.__min, 4)


# o = AIS(rosenbrock_func)
#
# for i in range(50):
#     best_affinity = o.max_bg_affinity()
#     o.clone_best_antibodies(best_affinity)
#     o.mutation_clones()
#     o.create_population_of_memory()
#     o.clonal_compression()
#     o.network_compression()
#     o.regeneration()
#     print(i, o.get_best_agent())
