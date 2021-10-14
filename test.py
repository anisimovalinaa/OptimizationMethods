def func(x, y):
    return x**2 + y**2


def rosenbrock_func(x, y):
    return (1 - x)**2 + 100*(y - x**2)**2

a = GeneticAlgorithm(50, 16, func, [-4, 4])
a.create_population()

for _ in range(100):
    couple = a.selection_the_best()
    new = a.crossover(couple)

    a.choice_the_best(new)
    a.mutation()
    print(a.best_agent())

# b = GeneticAlgorithm(100, 16, rosenbrock_func, [-3, 3])
# b.create_population()
#
# for _ in range(150):
#     couple = b.selection_random()
#     new = b.crossover(couple)
#
#     b.choice_the_best(new)
#     b.mutation()
#     print(b.best_agent())

# print(rosenbrock_func(1, 1))
