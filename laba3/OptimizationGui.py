from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from GeneticAlgorithm import GeneticAlgorithm
from ParticleSwarmOptimization import PSO
from BeesAlgorithm.beefunc import HimmelblauFunc
from BeesAlgorithm.hive import Hive
import numpy as np
import math


def func(x, y):
    return x ** 2 + y ** 2


def rosenbrock_func(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


def rastrigin_func(args):
    sum = 10 * len(args)
    for x in args:
        sum += x ** 2 - 10 * math.cos(2 * math.pi * x)

    return sum


def himmelblau_func(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


LARGE_FONT = ("Verdana", 10)


class OptimizationGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Генетический алгоритм")

        main_frame = tk.Frame(self, bg='white')

        select_frame = tk.Frame(main_frame)

        self.var = tk.IntVar()
        self.var.set(0)
        radio_gen_ind = tk.Radiobutton(select_frame, text='Генетический алгоритм. \n z(x, y) = x^2 + y^2',
                                       variable=self.var, value=1, font=LARGE_FONT,
                                       command=lambda: self.show_frame(IndFuncPage))
        radio_gen_ros = tk.Radiobutton(select_frame, text='Генетический алгоритм.\n Функция Розенброка',
                                       variable=self.var, value=0, font=LARGE_FONT,
                                       command=lambda: self.show_frame(RosenbrockPage))
        radio_pso = tk.Radiobutton(select_frame, text='Алгоритм роя частиц.\n Функция Растригина',
                                   variable=self.var, value=2, font=LARGE_FONT,
                                   command=lambda: self.show_frame(RastriginPage))
        radio_bees = tk.Radiobutton(select_frame, text='Пчелиный алгоритм.\n Функция Химмельблау',
                                    variable=self.var, value=3, font=LARGE_FONT,
                                    command=lambda: self.show_frame(HimmelblauPage))
        radio_gen_ros.pack(side='left', padx=10, pady=10)
        radio_gen_ind.pack(side='left', padx=10, pady=10)
        radio_pso.pack(side='left', padx=10, pady=10)
        radio_bees.pack(side='left', padx=10, pady=10)

        select_frame.pack(fill='x')

        work_frame = tk.Frame(main_frame)

        container_params = tk.Frame(work_frame)
        lab_count_generation = tk.Label(container_params, text="Количество поколений:", font=LARGE_FONT)
        lab_count_generation.grid(pady=5, padx=10)
        self.txt_count_generation = tk.Entry(container_params, width=20, font=LARGE_FONT)
        self.txt_count_generation.insert(0, 100)
        self.txt_count_generation.grid(pady=5, padx=10)

        lab_count_agent = tk.Label(container_params, text="Количество особей в популяции:", font=LARGE_FONT)
        lab_count_agent.grid(pady=5, padx=10)
        self.txt_count_agent = tk.Entry(container_params, width=20, font=LARGE_FONT)
        self.txt_count_agent.insert(0, 50)
        self.txt_count_agent.grid(pady=5, padx=10)

        lab_interval = tk.Label(container_params, text="Интервал:", font=LARGE_FONT)
        lab_interval.grid(pady=5, padx=10)

        block_interval = tk.Frame(container_params)
        lab_interval_from = tk.Label(block_interval, text="От:", font=LARGE_FONT)
        lab_interval_to = tk.Label(block_interval, text="До:", font=LARGE_FONT)
        self.txt_interval_from = tk.Entry(block_interval, width=7, font=LARGE_FONT)
        self.txt_interval_from.insert(0, -4)
        self.txt_interval_to = tk.Entry(block_interval, width=7, font=LARGE_FONT)
        self.txt_interval_to.insert(0, 4)

        lab_interval_from.pack(side='left')
        self.txt_interval_from.pack(side='left')

        lab_interval_to.pack(side='left')
        self.txt_interval_to.pack(side='right')

        block_interval.grid()

        start_button = tk.Button(container_params, text='Старт', width=30, pady=5,
                                 command=self.change, font=LARGE_FONT)
        start_button.grid(pady=10)

        container_params.pack(side="left")

        self.three_d_frame = tk.Frame(work_frame, width=600)
        self.three_d_frame.pack(side='left')
        self.frames = {}

        for F in [RosenbrockPage, IndFuncPage, RastriginPage, HimmelblauPage]:
            frame = F(self.three_d_frame, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(RosenbrockPage)

        container_out = tk.Frame(main_frame, bg='white')
        self.res = tk.Label(container_out, bg='white', font=LARGE_FONT, fg='#272343')
        self.res.pack(side='top')
        self.out_info = tk.Text(container_out, width=50, borderwidth=0, wrap=tk.WORD, font=LARGE_FONT, fg='#272343')
        self.out_info.pack(fill='both')
        container_out.pack(side='right')

        work_frame.pack()

        main_frame.pack(fill='both')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def change(self):
        if self.var.get() == 0:
            self.genetic_algorithm(rosenbrock_func)
        elif self.var.get() == 1:
            self.genetic_algorithm(func)
        elif self.var.get() == 2:
            self.pso_algorithm(rastrigin_func)
        elif self.var.get() == 3:
            self.bees_algorithm(HimmelblauFunc)

    def genetic_algorithm(self, func):
        self.out_info.delete('1.0', tk.END)
        self.res.config(text='')
        ga = GeneticAlgorithm(int(self.txt_count_agent.get()), 16, func,
                              [int(self.txt_interval_from.get()), int(self.txt_interval_to.get())])
        ga.clear()
        ga.create_population()

        count = self.txt_count_generation.get()

        for i in range(int(count)):
            couple = ga.selection_the_best()
            new = ga.crossover(couple)

            ga.choice_the_best(new)
            ga.mutation()
            self.out_info.insert("0.0", str(i) + ' ' + str(ga.best_agent()) + '\n')
            self.update()

        self.res.config(text='Минимум = ' + str(ga.best_agent()))

        del ga

    def pso_algorithm(self, func):
        self.out_info.delete('1.0', tk.END)
        self.res.config(text='')

        pso = PSO(int(self.txt_count_agent.get()),
                  [float(self.txt_interval_from.get()), float(self.txt_interval_to.get())], 2, func)
        for i in range(int(self.txt_count_generation.get())):
            pso.create_new_generation()
            self.out_info.insert("0.0", str(i) + ' ' + str(pso.get_best()) + '\n')
            self.update()

        self.res.config(text='Минимум = ' + str(pso.get_best()))

    def bees_algorithm(self, func):
        self.out_info.delete('1.0', tk.END)
        self.res.config(text='')

        # Количество пчел-разведчиков
        scout_bee_count = int(self.txt_count_agent.get())

        # Количество пчел, отправляемых на выбранные, но не лучшие участки
        selected_bee_count = 10

        # Количество пчел, отправляемые на лучшие участки
        best_bee_count = 30

        # Количество выбранных, но не лучших, участков
        sel_sites_count = 15

        # Количество лучших участков
        best_sites_count = 5

        # Через такое количество итераций без нахождения лучшего решения уменьшим область поиска
        max_func_counter = 10

        # Во столько раз будем уменьшать область поиска
        koeff = func.get_range_koeff()

        hive = Hive(scout_bee_count, selected_bee_count, best_bee_count,
                    sel_sites_count, best_sites_count,
                    func.get_start_range(), func,
                    [float(self.txt_interval_from.get()), float(self.txt_interval_to.get())])

        # Начальное значение целевой функции
        best_func = -1.0e9

        # Количество итераций без улучшения целевой функции
        func_counter = 0

        for n in range(int(self.txt_count_generation.get())):
            hive.next_step()

            if hive.get_best_fitness() != best_func:
                # Найдено место, где целевая функция лучше
                best_func = hive.get_best_fitness()
                func_counter = 0

            else:
                func_counter += 1
                if func_counter == max_func_counter:
                    hive.range = [hive.range[m] * koeff[m] for m in range(len(hive.range))]
                    func_counter = 0

            self.out_info.insert("0.0", str(n) + ' ' + str(hive.get_best()) + '\n')
            self.update()

        self.res.config(text='Минимум = ' + str(hive.get_best()))


class RosenbrockPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        x, y = np.mgrid[-4:4:20j, -4:4:10j]
        z = rosenbrock_func(x, y)
        f = plt.figure(figsize=(5, 5))
        ax = f.gca(projection='3d')
        ax.plot_surface(x, y, z)
        ax.view_init(30, 45)

        canvas = FigureCanvasTkAgg(f, self)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class IndFuncPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        x, y = np.mgrid[-4:4:20j, -4:4:10j]
        z = func(x, y)
        f = plt.figure()
        ax = f.gca(projection='3d')
        ax.plot_surface(x, y, z)
        ax.view_init(30, 45)

        canvas = FigureCanvasTkAgg(f, self)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class RastriginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        x, y = np.mgrid[-5.12:5.12:50j, -5.12:5.12:40j]
        z = []
        for i in range(len(x)):
            points = []
            for j in range(len(x[i])):
                v = rastrigin_func([x[i][j], y[i][j]])
                points.append(v)

            z.append(points)

        z = np.array(z)

        f = plt.figure()
        ax = f.gca(projection='3d')
        ax.plot_surface(x, y, z)
        ax.view_init(20, 60)

        canvas = FigureCanvasTkAgg(f, self)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class HimmelblauPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        x, y = np.mgrid[-4:4:20j, -4:4:10j]
        z = himmelblau_func(x, y)
        f = plt.figure()
        ax = f.gca(projection='3d')
        ax.plot_surface(x, y, z)
        ax.view_init(30, 45)

        canvas = FigureCanvasTkAgg(f, self)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
