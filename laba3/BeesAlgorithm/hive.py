# -*- coding: utf-8 -*-
"""
Реализация алгоритма роя пчел
"""


class Hive:
    def __init__(self, scout_bee_count, selected_bee_count, best_bee_count,
                 sel_sites_count, best_sites_count, range_list, bee_type, interval):
        self.__scout_bee_count = scout_bee_count
        self.__selected_bee_count = selected_bee_count
        self.__best_bee_count = best_bee_count

        self.__sel_sites_count = sel_sites_count
        self.__best_sites_count = best_sites_count

        self.__bee_type = bee_type

        self.range = range_list

        # Лучшая на данный момент позиция
        self.__best_position = None

        # Лучшее на данный момент здоровье пчелы (чем больше, тем лучше)
        self.__best_fitness = None

        # Начальное заполнение роя пчелами со случайными координатами
        bee_count = scout_bee_count + selected_bee_count * sel_sites_count + best_bee_count * best_sites_count
        self.swarm = [bee_type(interval) for _ in range(bee_count)]

        # Лучшие и выбранные места
        self.best_sites = []
        self.sel_sites = []

        self.swarm = sorted(self.swarm, key=lambda x: x.get_fitness(), reverse=True)
        self.__best_position = self.swarm[0].get_position()
        self.__best_fitness = self.swarm[0].fitness

    """ Послать пчел на позицию.
    Возвращает номер следующей пчелы для вылета """
    def send_bees(self, position, index, count):
        for n in range(count):
            # Чтобы не выйти за пределы улея
            if index == len(self.swarm):
                break

            curr_bee = self.swarm[index]

            if curr_bee not in self.best_sites and curr_bee not in self.sel_sites:
                # Пчела не на лучших или выбранных позициях
                curr_bee.goto(position, self.range)

            index += 1

        return index

    """Новая итерация"""
    def next_step(self):
        # Выбираем самые лучшие места и сохраняем ссылки на тех, кто их нашел
        self.best_sites = [self.swarm[0]]

        curr_index = 1
        for curr_bee in self.swarm[curr_index:]:
            # Если пчела находится в пределах уже отмеченного лучшего участка, то ее положение не считаем
            if curr_bee.other_patch(self.best_sites, self.range):
                self.best_sites.append(curr_bee)

                if len(self.best_sites) == self.__best_sites_count:
                    break

            curr_index += 1

        self.sel_sites = []

        for curr_bee in self.swarm[curr_index:]:
            if curr_bee.other_patch(self.best_sites, self.range) and curr_bee.other_patch(self.sel_sites, self.range):
                self.sel_sites.append(curr_bee)

                if len(self.sel_sites) == self.__sel_sites_count:
                    break

        # Отправляем пчел на задание :)
        # Отправляем сначала на лучшие места

        # Номер очередной отправляемой пчелы. 0-ую пчелу никуда не отправляем
        bee_index = 1

        for best_site in self.best_sites:
            bee_index = self.send_bees(best_site.get_position(), bee_index, self.__best_bee_count)

        for sel_site in self.sel_sites:
            bee_index = self.send_bees(sel_site.get_position(), bee_index, self.__selected_bee_count)

        # Оставшихся пчел пошлем куда попадет
        for curr_bee in self.swarm[bee_index:]:
            curr_bee.goto_random()

        self.swarm = sorted(self.swarm, key=lambda x: x.get_fitness(), reverse=True)
        self.__best_position = self.swarm[0].get_position()
        self.__best_fitness = self.swarm[0].fitness

    def get_best_position(self):
        return self.__best_position

    def get_best_fitness(self):
        return self.__best_fitness

    def get_best(self):
        return tuple([round(self.__best_position[0], 5), round(self.__best_position[1], 5),
                      -round(self.__best_fitness, 5)])
