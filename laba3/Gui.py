from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import numpy as np


def func(x, y):
    return x**2 + y**2


def rosenbrock_func(x, y):
    return (1 - x)**2 + 100*(y - x**2)**2


LARGE_FONT = ("Verdana", 12)


class OptimizationGui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Генетический алгоритм")

        main_frame = tk.Frame(self, bg='yellow')

        select_frame = tk.Frame(main_frame)

        radio_gen_ind = tk.Radiobutton(select_frame, text='Генетический алгоритм. \n z(x, y) = x^2 + y^2', value=1,
                                       command=lambda: self.show_frame(GeneticInd))
        radio_gen_ros = tk.Radiobutton(select_frame, text='Генетический алгоритм.\n Функция Розенброка', value=0,
                                       command=lambda: self.show_frame(GeneticRosenbrock))
        radio_gen_ros.pack(side='left', padx=10, pady=10)
        radio_gen_ind.pack(side='left', padx=10, pady=10)

        select_frame.pack(fill='x')

        work_frame = tk.Frame(main_frame)

        container_params = tk.Frame(work_frame)
        lab_count_generation = tk.Label(container_params, text="Количество поколений:")
        lab_count_generation.grid(pady=5, padx=10)
        txt_count_generation = tk.Entry(container_params, width=20)
        txt_count_generation.grid(pady=5, padx=10)

        lab_count_agent = tk.Label(container_params, text="Количество особей в популяции:")
        lab_count_agent.grid(pady=5, padx=10)
        txt_count_agent = tk.Entry(container_params, width=20)
        txt_count_agent.grid(pady=5, padx=10)

        lab_interval = tk.Label(container_params, text="Интервал:")
        lab_interval.grid(pady=5, padx=10)

        block_interval = tk.Frame(container_params)
        lab_interval_from = tk.Label(block_interval, text="От:")
        lab_interval_to = tk.Label(block_interval, text="До:")
        txt_interval_from = tk.Entry(block_interval, width=7)
        txt_interval_from.insert(0, -4)
        txt_interval_to = tk.Entry(block_interval, width=7)
        txt_interval_to.insert(0, 4)

        lab_interval_from.pack(side='left')
        txt_interval_from.pack(side='left')

        lab_interval_to.pack(side='left')
        txt_interval_to.pack(side='right')

        block_interval.grid()

        start_button = tk.Button(container_params, text='Старт', width=30, pady=5)
        start_button.grid(pady=10)

        container_params.pack(side="left")

        self.three_d_frame = tk.Frame(work_frame, width=600)
        self.three_d_frame.pack(side='left')
        self.frames = {}

        for F in [GeneticRosenbrock, GeneticInd]:
            frame = F(self.three_d_frame, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GeneticRosenbrock)

        container_out = tk.Frame(main_frame)
        out_info = tk.Text(container_out, width=20,
                font="Arial 14")
        out_info.pack(fill='both')
        container_out.pack(side='right')

        work_frame.pack()

        main_frame.pack(fill='both')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GeneticRosenbrock(tk.Frame):
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


class GeneticInd(tk.Frame):
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
