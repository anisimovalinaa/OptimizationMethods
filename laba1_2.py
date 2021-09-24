import numpy as np
import matplotlib.pyplot as plt


def func(x1, x2):
    return x1**2 + x2**2 + x1*x2 + x1 - x2 + 1


def get_left_right_value(x, step, z, flag):
    x1 = round(x + step, 1)
    x2 = round(x - step, 2)

    if flag == 'X':
        return {func(x, z): x, func(x1, z): x1, func(x2, z): x2}
    else:
        return {func(z, x): x, func(z, x1): x1, func(z, x2): x2}


def next_value(x, Y):
    if Y[min(Y.keys())] > x:
        operation = '+'
    else:
        operation = '-'
    return Y[min(Y.keys())], operation


def gauss_seidel_method():
    e = 0.02
    step_x = 0.1
    step_z = 0.1
    x = 4
    z = 10
    check_x = True
    pred_y = 0
    current_y = func(x, z)
    X = [x]
    Z = [z]
    Y = [current_y]

    while abs(pred_y - current_y) > e:
        check = True

        if check_x:
            Ys = get_left_right_value(x, step_x, z, 'X')

            if Ys[min(Ys.keys())] == x:
                step_x /= 2
                continue
            else:
                x, operation = next_value(x, Ys)
        else:
            Ys = get_left_right_value(z, step_z, x, 'Z')

            if Ys[min(Ys.keys())] == z:
                step_z /= 2
                continue
            else:
                z, operation = next_value(z, Ys)

        X.append(x)
        Z.append(z)
        pred_y = current_y
        current_y = min(Ys.keys())
        Y.append(current_y)

        while(check):
            if check_x:
                var = round(eval('x {} step_x'.format(operation)), 1)
                y = func(var, z)
            else:
                var = round(eval('z {} step_z'.format(operation)), 1)
                y = func(x, var)

            if y <= current_y:
                current_y = y
                if check_x:
                    x = var
                else:
                    z = var
            else:
                X.append(x)
                Z.append(z)
                Y.append(current_y)
                check = False
                check_x = not(check_x)
    return X, Z, Y


def init_simplex(x, z):
    alpha = 2
    x1 = (x - alpha / 2, z - 0.29 * alpha)
    x2 = (x + alpha / 2, z - 0.29 * alpha)
    x3 = (x, z + 0.58 * alpha)
    y1 = func(x1[0], x1[1])
    y2 = func(x2[0], x2[1])
    y3 = func(x3[0], x3[1])

    return [[[x1[0], x2[0], x3[0], x1[0]],
            [x1[1], x2[1], x3[1], x1[1]]]],\
            sorted([(y1, x1), (y2, x2), (y3, x3)], key=lambda x: x[0])


def calculate_new_point(Y):
    X = (Y[0][1][0] + Y[1][1][0] - Y[2][1][0],
         Y[0][1][1] + Y[1][1][1] - Y[2][1][1])

    return func(X[0], X[1]), X


def simplex_method():
    e = 0.0
    x, z = 4, 10

    y_pred = 0
    triangles, Ys = init_simplex(x, z)

    while abs(Ys[2][0] - y_pred) > e:
        y_pred = Ys[0][0]
        new_point = calculate_new_point(Ys)
        Ys[2] = new_point
        Ys = sorted(Ys, key=lambda x: x[0])

        triangles.append([[Ys[0][1][0], Ys[1][1][0], Ys[2][1][0], Ys[0][1][0]],
                          [Ys[0][1][1], Ys[1][1][1], Ys[2][1][1], Ys[0][1][1]]])

        if new_point == Ys[2]:
            x1 = ((Ys[0][1][0] + Ys[1][1][0])/2,
                  (Ys[0][1][1] + Ys[1][1][1])/2)
            x1 = (round(func(x1[0], x1[1]), 6), x1)
            x2 = ((Ys[0][1][0] + Ys[2][1][0])/2,
                  (Ys[0][1][1] + Ys[2][1][1])/2)
            x2 = (round(func(x2[0], x2[1]), 6), x2)

            Ys[1], Ys[2] = x1, x2
            Ys = sorted(Ys, key=lambda x: x[0])

    return triangles


def draw_func():
    fig, ax = plt.subplots(1)
    x = np.arange(-6, 5.5, 0.2)
    z = np.arange(-10.5, 12.0, 0.2)

    xgrid, zgrid = np.meshgrid(x, z)
    ygrid = func(xgrid, zgrid)

    ax.contour(xgrid, zgrid, ygrid, levels=20)

    return ax


def draw_func_points(X, Z, Y, ax):
    ax.plot(X, Z, color='black')
    ax.text(-0.7, 1, 'Минимум в точке \n({}; {}; {})'.format(X[-1], Z[-1], Y[-1]))

    plt.show()


def draw_triangles(triangles, ax):
    for points in triangles:
        ax.plot(points[0], points[1], color='black')

    ax.text(0.4, -1, 'Минимум в точке \n({}; {})'.format(triangles[-1][0][0],
                                                         round(triangles[-1][1][0], 1)))

    plt.show()


if __name__ == '__main__':
    X, Z, Y = gauss_seidel_method()
    ax = draw_func()
    draw_func_points(X, Z, Y, ax)

    triangles = simplex_method()
    ax = draw_func()
    draw_triangles(triangles, ax)




