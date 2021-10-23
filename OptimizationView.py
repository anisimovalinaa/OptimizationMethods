from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from laba1_2 import gauss_seidel_method, simplex_method, draw_func, draw_func_points, draw_triangles

LARGE_FONT = ("Verdana", 10)


class OptimizationView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Генетический алгоритм")

        main_frame = tk.Frame(self, bg='white')

        name_func = tk.Label(main_frame, text='Функция: y(x1, x2) = x1^2 + x2^2 + x1*x2 + x1 - x2 + 1',
                             font=30, bg='white', pady=20)
        name_func.pack()

        select_frame = tk.Frame(main_frame)

        self.var = tk.IntVar()
        self.var.set(0)
        radio_gen_ind = tk.Radiobutton(select_frame, text='Алгоритм покоординатного спуска',
                                       variable=self.var, value=0, font=LARGE_FONT,
                                       command=lambda: self.show_frame(GaussSeidelMethod))
        radio_gen_ros = tk.Radiobutton(select_frame, text='Симплекс метод',
                                       variable=self.var, value=1, font=LARGE_FONT,
                                       command=lambda: self.show_frame(SimplexMethod))

        radio_gen_ind.pack(side='left', padx=10, pady=10)
        radio_gen_ros.pack(side='left', padx=10, pady=10)

        select_frame.pack(fill='x')

        self.frames = {}
        self.graphic = tk.Frame(main_frame)

        for F in [GaussSeidelMethod, SimplexMethod]:
            frame = F(self.graphic, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GaussSeidelMethod)

        self.graphic.pack(side='bottom')

        main_frame.pack(fill='both')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GaussSeidelMethod(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f = plt.figure(figsize=(5, 5))
        X, Z, Y = gauss_seidel_method()

        ax = f.gca()
        ax = draw_func(ax)
        draw_func_points(X, Z, Y, ax)

        canvas = FigureCanvasTkAgg(f, self)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class SimplexMethod(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f = plt.figure()

        triangles = simplex_method()

        ax = f.gca()
        ax = draw_func(ax)
        draw_triangles(triangles, ax)

        canvas = FigureCanvasTkAgg(f, self)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    app = OptimizationView()
    app.mainloop()

