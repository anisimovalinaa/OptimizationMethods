import numpy as np
import copy
import math


def func(point):
    sum = 10 * len(point)
    for x in point:
        sum += x ** 2 - 10 * math.cos(2 * math.pi * x)

    return sum


class Particle:
    def __init__(self, min_start_position, max_start_position, min_speed, max_speed,  dimensions, func):
        self.__particle = np.random.uniform(min_start_position, max_start_position, dimensions)
        self.__round3()
        self.__speed = np.random.uniform(min_speed, max_speed, dimensions)
        self.__min_speed, self.__max_speed = min_speed, max_speed
        self.best = None
        self.__func = func

    def get_particle(self):
        return self.__particle

    def get_func(self):
        return self.__func

    def get_speed(self):
        return self.__speed

    def get_min_speed(self):
        return self.__min_speed

    def get_max_speed(self):
        return self.__max_speed

    def value(self):
        return self.__func(self.__particle)

    def update(self, best):
        local_update_factor = np.random.uniform(0, 1, self.__particle.size)
        global_update_factor = np.random.uniform(0, 1, self.__particle.size)

        local_speed_update = local_update_factor * (self.best - self)
        global_speed_update = global_update_factor * (best - self)
        # print(best, self, best-self)
        # print()

        self.__speed = self.__speed + (local_speed_update + global_speed_update)

        self.__speed = np.clip(self.__speed, self.__min_speed, self.__max_speed)
        self.__particle[:] = self.__particle + self.__speed
        self.__round3()

    def __round3(self):
        for i in range(self.__particle.size):
            self.__particle[i] = round(self.__particle[i], 2)

    def __add__(self, other):
        if isinstance(other, Particle):
            res = []
            for i in range(len(self.__particle)):
                res.append(self.__particle[i] + other.get_particle()[i])

            return res

    def __sub__(self, other):
        if isinstance(other, Particle):
            res = []
            for i in range(len(self.__particle)):
                res.append(self.__particle[i] - other.get_particle()[i])

            return res

    def __str__(self):
        res = '-- Точка ' + str(self.__particle) + ' -- Значение ' + str(self.value()) \
               + ' -- Скорость ' + str(self.__speed)
        if isinstance(self.best, Particle):
            res += '-- Лучший ' + str(self.best.get_particle()) + ' ' + str(self.best.value())

        return res


class PSO:
    def __init__(self, size_population, range_f, dimensions, func):
        self.__size_population = size_population
        self.__min_start_position, self.__max_start_position = range_f[0], range_f[1]
        self.__min_speed, self.__max_speed = -0.9, 0.9
        self.__dimensions = dimensions
        self.__func = func
        self.__best = None

        self.__population = self.__create_populations()

    def get_best(self):
        if isinstance(self.__best, Particle):
            return tuple([self.__best.get_particle()[0], self.__best.get_particle()[1], self.__best.value()])

    def __create_populations(self):
        population = []
        for _ in range(self.__size_population):
            population.append(Particle(self.__min_start_position, self.__max_start_position, self.__min_speed,
                                       self.__max_speed, self.__dimensions, func))

        return population

    def get_population(self):
        res = ''
        for particle in self.__population:
            res += str(particle) + '\n'

        return res

    def create_new_generation(self):
        for particle in self.__population:
            if particle.best is None or particle.best.value() > particle.value():
                particle.best = copy.deepcopy(particle)

            if self.__best is None or self.__best.value() > particle.value():
                self.__best = copy.deepcopy(particle)

        for particle in self.__population:
            particle.update(self.__best)
