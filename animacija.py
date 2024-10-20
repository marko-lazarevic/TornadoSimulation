import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def tornado(ALPHA=45, V0=100, TORNADO=50):
    U0 = TORNADO
    R0 = np.array([-100.0, 0.0, 0.0])
    m = 0.2
    diam = 0.025
    rho = 1.293
    D = 3.0 * rho * diam ** 2
    Dm = D / m
    g = np.array([0.0, 0.0, 9.8])
    u0 = U0
    rast = 5.0
    r0 = R0
    alpha = np.deg2rad(ALPHA)
    v0 = V0 * np.array([np.cos(alpha), 0, np.sin(alpha)])
    time = 100.0
    dt = 0.001
    n = int(round(time / dt))
    r = np.zeros((n, 3), float)
    v = np.zeros((n, 3), float)
    a = np.zeros((n, 3), float)
    t = np.zeros(n, float)
    r[0] = r0
    v[0] = v0
    i = 0
    while (r[i, 2] >= 0.0) and (i < n):
        rr = linalg.norm(r[i])
        if (rr > rast):
            U = u0 * (rast / rr)
        else:
            U = u0 * rr / rast
        u = U * np.array([-r[i, 1] / rr, r[i, 0] / rr, 0.0])
        vrel = v[i] - u
        aa = -g - Dm * linalg.norm(vrel) * vrel
        a[i] = aa
        v[i + 1] = v[i] + dt * aa

        r[i + 1] = r[i] + dt * v[i + 1]
        t[i + 1] = t[i] + dt
        i = i + 1

    imax = i
    ii = r[0:imax]
    tt = t[0:imax]
    rx, ry, rz = [], [], []

    for el in ii:
        rx.append(el[0])
        ry.append(el[1])
        rz.append(el[2])

    return rx, ry, rz, tt

while True:
    root = tk.Tk()
    root.geometry("300x300")
    quit_button = tk.Button(root, text="Animiraj", command=root.destroy)

    button_width = 100
    button_height = 30
    button_x = (400 - button_width) / 2
    button_y = 300 - 50 - button_height

    quit_button.place(relx=button_x/400, rely=button_y/300, relwidth=button_width/400, relheight=button_height/300)

    angle_var = tk.DoubleVar()
    angle_var.set(45)
    speed_var = tk.DoubleVar()
    speed_var.set(100)
    tornado_var = tk.DoubleVar()
    tornado_var.set(50)
    
    angle_slider = tk.Scale(root, from_=10, to=90, variable=angle_var, orient="horizontal", label = "Ugao ispaljivanja")
    angle_slider.pack()

    val1_slider = tk.Scale(root, from_=50, to=150, variable=speed_var, orient="horizontal", label = "Brzina ispaljivanja")
    val1_slider.pack()

    val2_slider = tk.Scale(root, from_=25, to=100, variable=tornado_var, orient="horizontal", label = "Brzina tornada")
    val2_slider.pack()

    root.mainloop()

    angle = angle_var.get()
    value1 = speed_var.get()
    value2 = tornado_var.get()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    x_data, y_data, z_data, tt = tornado(ALPHA = float(angle), V0 = float(value1), TORNADO = value2)


    def prosek(arr):
            new_arr = []
            for i in range(0, len(arr), 5):
                if i + 4 < len(arr):
                    average = sum(arr[i:i+5]) / 5
                    new_arr.append(average)
            return new_arr

    x_novo = prosek(x_data)
    y_novo = prosek(y_data)
    z_novo = prosek(z_data)
    t_novo = prosek(tt)

    line, = ax.plot([], [], [], '-')
    
    ax.set_xlim(min(x_novo)-2,max(x_novo)+2)
    ax.set_ylim(min(y_novo)-2,max(y_novo)+2)
    ax.set_zlim(0,max(z_novo)+2)

    circle, = ax.plot([], [], [], marker='o', markersize=3, color='red')
    def update(frame):
        
        line.set_data(x_novo[:frame+1], y_novo[:frame+1])
        line.set_3d_properties(z_novo[:frame+1])

        circle.set_data(x_novo[frame], y_novo[frame])
        circle.set_3d_properties(z_novo[frame])

        if frame == len(t_novo) - 1:
            # schedule a function call to close the window after a delay
            root.after(2500, lambda: plt.close(fig))
        return line, circle

    ani = FuncAnimation(fig, update, frames=len(t_novo),repeat = False, interval=1, blit=True)


    plt.show()
