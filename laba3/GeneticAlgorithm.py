import math
import random
import numpy as np


class GeneticAlgorithm:
    __population = []
    __p_mutation = 0.2

    def __init__(self, size_population, count_genes, function, range_f):
        self.__SIZE_POPULATION = size_population
        self.__COUNT_GENES = count_genes
        self.__function = function
        self.__min = range_f[0]
        self.__max = range_f[1]

    def get_population(self):
        return self.__population

    def get_func_value(self, agent):
        x = self.decoding_agent(int(''.join(str(e) for e in agent[0]), base=2))
        y = self.decoding_agent(int(''.join(str(e) for e in agent[1]), base=2))

        return self.__function(x, y), x, y

    def best_agent(self):
        min = 100
        points = []
        for agent in self.__population:
            z, x, y = self.get_func_value(agent)

            if z < min:
                min = z
                points = (x, y, z)

        return points

    def create_population(self):
        for i in range(self.__SIZE_POPULATION):
            agent_x = list(np.random.randint(0, 2, self.__COUNT_GENES))
            agent_y = list(np.random.randint(0, 2, self.__COUNT_GENES))
            self.__population.append([agent_x, agent_y])

        # self.__population[0][0], self.__population[0][1] = [1 for _ in range(self.__COUNT_GENES)], \
        #                                                    [1 for _ in range(self.__COUNT_GENES)]

    def min_hamming_distance(self, num_agent):
        min_ham = self.__COUNT_GENES
        ind = 0

        for i in range(self.__SIZE_POPULATION):
            if self.__population[i] != self.__population[num_agent]:
                ham_dist = 0
                for j in range(self.__COUNT_GENES):
                    if self.__population[i][0][j] != self.__population[num_agent][0][j]: ham_dist += 1
                    if self.__population[i][1][j] != self.__population[num_agent][1][j]: ham_dist += 1

                if ham_dist < min_ham:
                    min_ham = ham_dist
                    ind = i
        return ind

    def selection_inbreeding(self):
        indexes = np.arange(0, self.__SIZE_POPULATION, 1)
        couples = []

        for _ in range(int(self.__SIZE_POPULATION/2)):
            first_agent = random.choice(indexes)
            second_agent = self.min_hamming_distance(first_agent)
            couples.append((first_agent, second_agent))

        return couples

    def selection_random(self, indexes=None):
        if not(indexes):
            indexes = np.arange(0, self.__SIZE_POPULATION, 1)

        couples = []

        for _ in range(int(self.__SIZE_POPULATION / 2)):
            first_agent = random.choice(indexes)
            second_agent = random.choice(indexes)
            couples.append((first_agent, second_agent))

        return couples

    def selection_the_best(self):
        mean = 0
        for agent in self.__population:
            z, _, _ = self.get_func_value(agent)
            mean += z

        mean /= self.__SIZE_POPULATION

        indexes = []
        for i in range(self.__SIZE_POPULATION):
            z, _, _ = self.get_func_value(self.__population[i])

            if z <= mean:
                indexes.append(i)

        return self.selection_random(indexes)

    def crossover(self, couples):
        new_generation = []
        points = np.arange(1, self.__COUNT_GENES, 1)
        for coup in couples:
            num_first = coup[0]
            num_second = coup[1]
            new_first_agent = []
            new_second_agent = []
            for i in range(2):
                first_point = random.choice(points)
                second_point = random.choice(points)
                first_point, second_point = min(first_point, second_point), max(first_point, second_point)

                new_first_agent.append(self.__population[num_first][i][:first_point] + \
                                   self.__population[num_second][i][first_point:second_point+1] + \
                                   self.__population[num_first][i][second_point+1:])

                new_second_agent.append(self.__population[num_second][i][:first_point] + \
                                   self.__population[num_first][i][first_point:second_point + 1] + \
                                   self.__population[num_second][i][second_point+1:])

            new_generation.append(new_first_agent)
            new_generation.append(new_second_agent)

        return new_generation

    def choice_the_best(self, new_generation):
        value_func = {}

        for i in range(self.__SIZE_POPULATION):
            agent = self.__population[i]
            z, _, _ = self.get_func_value(agent)
            value_func[z] = agent

            agent = new_generation[i]
            z, _, _ = self.get_func_value(agent)
            value_func[z] = agent

        for i, key in zip(range(self.__SIZE_POPULATION), sorted(value_func.keys())):
            self.__population[i] = value_func[key]

    def mutation(self):
        indexes = np.arange(0, self.__COUNT_GENES, 1)
        for agent in self.__population:
            if random.random() < self.__p_mutation:
                a = random.choice([0, 1])
                i = random.choice(indexes)
                j = agent[a][i]
                agent[a][i] = int(not(j))

        if self.__p_mutation > 0:
            self.__p_mutation -= 0.03

    def coding_agent(self, agent):
        return math.trunc(((agent - self.__min) * (2 ** self.__COUNT_GENES - 1)) / (self.__max - self.__min))

    def decoding_agent(self, agent):
        return round((agent * (self.__max - self.__min)) / (2 ** self.__COUNT_GENES - 1) + self.__min, 2)

    def clear(self):
        self.__population = []
