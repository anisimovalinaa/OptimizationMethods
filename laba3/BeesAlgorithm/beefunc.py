# -*- coding: utf-8 -*-
import random


class FloatBee:
    """Класс пчел, где в качестве координат используется список дробных чисел"""

    def __init__(self):
        # Положение пчелы (искомые величины)
        self.position = None

        # Интервалы изменений искомых величин (координат)
        self.min_val = None
        self.max_val = None

        # Значение целевой функции
        self.fitness = 0.0

    """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
    Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
    Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
    def calc_fitness(self):
        pass

    """Проверить находится ли пчела на том же участке, что и одна из пчел в bee_list.
    range_list - интервал изменения каждой из координат"""
    def other_patch(self, bee_list, range_list):
        if not (len(bee_list)):
            return True

        for curr_bee in bee_list:
            position = curr_bee.get_position()

            for n in range(len(self.position)):
                if abs(self.position[n] - position[n]) > range_list[n]:
                    return True

        return False

    """Вернуть копию (!) своих координат"""
    def get_position(self):
        return [val for val in self.position]

    """Перелет в окрестность места, которое нашла другая пчела. Не в то же самое место! """
    def goto(self, other_pos, range_list):
        # К каждой из координат добавляем случайное значение
        self.position = [other_pos[n] + random.uniform(-range_list[n], range_list[n])
                         for n in range(len(other_pos))]

        # Проверим, чтобы не выйти за заданные пределы
        self.check_position()

        # Расчитаем и сохраним целевую функцию
        self.calc_fitness()

    def goto_random(self):
        # Заполним координаты случайными значениями
        self.position = [random.uniform(self.min_val[n], self.max_val[n]) for n in range(len(self.position))]
        self.check_position()
        self.calc_fitness()

    """Скорректировать координаты пчелы, если они выходят за установленные пределы"""
    def check_position(self):
        for n in range(len(self.position)):
            if self.position[n] < self.min_val[n]:
                self.position[n] = self.min_val[n]

            elif self.position[n] > self.max_val[n]:
                self.position[n] = self.max_val[n]


class HimmelblauFunc(FloatBee):
    """Функция - сумма квадратов по каждой координате"""

    # Количество координат
    count = 2

    @staticmethod
    def get_start_range():
        return [10.0] * HimmelblauFunc.count

    @staticmethod
    def get_range_koeff():
        return [0.25] * HimmelblauFunc.count

    def __init__(self, interval):
        FloatBee.__init__(self)

        self.min_val = [interval[0]] * HimmelblauFunc.count
        self.max_val = [interval[1]] * HimmelblauFunc.count

        self.position = [random.uniform(self.min_val[n], self.max_val[n]) for n in range(HimmelblauFunc.count)]
        self.calc_fitness()

    def calc_fitness(self):
        x, y = self.position[0], self.position[1]
        self.fitness = -((x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2)

    def get_fitness(self):
        return self.fitness
