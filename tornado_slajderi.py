from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import Tk
import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def tornado(ALPHA = 45 ,V0 = 100 , TORNADO = 50):
    U0 = TORNADO
    R0 = np.array([-100.0,0.0,0.0])
    m = 0.2
    diam = 0.025
    rho = 1.293
    D = 3.0*rho*diam**2
    Dm = D/m
    g = np.array([0.0,0.0,9.8])
    u0 = U0
    rast = 5.0
    r0 = R0
    alpha = np.deg2rad(ALPHA);
    v0 = V0*np.array([np.cos(alpha),0,np.sin(alpha)])
    time = 100.0
    dt = 0.001
    n = int(round(time/dt))
    r = np.zeros((n,3),float)
    v = np.zeros((n,3),float)
    a = np.zeros((n,3),float)
    t = np.zeros(n,float)
    r[0] = r0
    v[0] = v0
    i = 0
    while (r[i,2]>=0.0) and (i<n):
        rr = linalg.norm(r[i])
        if (rr>rast):
            U = u0*(rast/rr)
        else:
            U = u0*rr/rast
        u = U*np.array([-r[i,1]/rr,r[i,0]/rr,0.0])
        vrel = v[i] - u
        aa = -g - Dm*linalg.norm(vrel)*vrel
        a[i] = aa
        v[i+1] = v[i] + dt*aa

        r[i+1] = r[i] + dt*v[i+1]
        t[i+1] = t[i] + dt
        i = i + 1

    imax = i
    ii = r[0:imax]
    tt = t[0:imax]
    rx,ry,rz = [],[],[]


    for el in ii:
        rx.append(el[0])
        ry.append(el[1])
        rz.append(el[2])
    
    return rx,ry,rz,tt



class App:
    def __init__(self, master):
        # Create a container
        frame = ttk.Frame(master)

        # Horizontalni box za slajder brzine i ugla
        hbox1 = ttk.Frame(frame)
        hbox1.pack(side="top", pady=5)
        self.label_brzine = ttk.Label(hbox1, text="Pocetna brzina:")
        self.label_brzine.pack(side="left")
        self.slider_brzina = ttk.Scale(hbox1, from_=50, to=150, orient='horizontal', command=self.promena_brzine)
        self.slider_brzina.pack(side="left")
        self.slider_brzina.set(100)

        # Horizontalni box za slajder ugao i labelu
        hbox2 = ttk.Frame(frame)
        hbox2.pack(side="top", pady=5)
        self.label_ugao = ttk.Label(hbox2, text="Ugao:")
        self.label_ugao.pack(side="left")
        self.slider_ugao = ttk.Scale(hbox2, from_=10, to=90, orient='horizontal', command=self.promena_ugla)
        self.slider_ugao.pack(side="left")
        self.slider_ugao.set(45)

        # Horizontalni boks sa opcionom listom
        hbox3 = ttk.Frame(frame)
        hbox3.pack(side="top", pady=5)
        options_list = [25, 50, 75, 100]
        self.vrednost_tornada = tk.StringVar(root)
        self.vrednost_tornada.set(options_list[1])
        self.label_tornado = ttk.Label(hbox3, text="Jacina tornada:")
        self.label_tornado.pack(side="left")
        self.cb_tornado = ttk.OptionMenu(hbox3, self.vrednost_tornada, *options_list, command=self.promena_tornada)
        self.cb_tornado.pack(side="left")

        

        self.ax = plt.subplots()
        fig = Figure()
        self.ax = fig.add_subplot(111,projection="3d")
        self.ax.set_xlabel("X osa")
        self.ax.set_ylabel("Y osa")
        self.ax.set_zlabel("Z osa")
        
		 # Create the ball
        self.ball = self.ax.scatter([], [], [], color='red', marker='o')

        x_data, y_data, z_data, tt  = tornado()

        # Calculate the concentric circles in the XY plane
        radii = np.arange(15, 105, 10)  # Radii of the concentric circles
        
        # Add tornado lines in the XY plane using quiver
        for radius in radii:
            arrow_length = 2*(1-1/ radius )# Fixed arrow length with decreasing length towards the center
            num_points = int(np.pi * radius / arrow_length)  # Number of points on each circle
            thetas = np.linspace(0, 2 * np.pi, num_points)  # Angles for the points on each circle
            x_circle = radius * np.cos(thetas)
            y_circle = radius * np.sin(thetas)
            z_circle = np.zeros_like(x_circle)
            #self.ax.quiver(x_circle[:-1], y_circle[:-1], z_circle[:-1], x_circle[1:] - x_circle[:-1], y_circle[1:] - y_circle[:-1], z_circle[1:], length=arrow_length, normalize=True, color="blue", arrow_length_ratio=0.3)

        x_novo = self.prosek(x_data)
        y_novo = self.prosek(y_data)
        z_novo = self.prosek(z_data)
        t_novo = self.prosek(tt)
	
        self.line, = self.ax.plot(x_novo,y_novo,z_novo)
        
        self.ax.set_xlim(min(x_novo)-2,max(x_novo)+2)
        self.ax.set_ylim(min(y_novo)-2,max(y_novo)+2)
        self.ax.set_zlim(0,max(z_novo)+2)

        self.canvas = FigureCanvasTkAgg(fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        frame.pack()

        self.ani = animation.FuncAnimation(fig, self.update_animation, frames=len(x_novo),repeat=True, interval=1)

    
    def update_animation(self, i):
        # Update the position of the ball
        if(i<len(self.line.get_data_3d()[0]) and i<len(self.line.get_data_3d()[1]) and len(self.line.get_data_3d()[2])):
            self.ball._offsets3d = ([self.line.get_data_3d()[0][i]], [self.line.get_data_3d()[1][i]], [self.line.get_data_3d()[2][i]])
    
    def prosek(self,arr):
            new_arr = []
            for i in range(0, len(arr), 5):
                if i + 4 < len(arr):
                    average = sum(arr[i:i+5]) / 5
                    new_arr.append(average)
            return new_arr

        
    def promena_brzine(self,value):
        x_data, y_data, z_data, tt   = tornado(ALPHA=float(self.slider_ugao.get()),V0=float(value), TORNADO=float(self.vrednost_tornada.get()))
        print("V0:" +str(value))
        print("ALPHA:" +str(self.slider_ugao.get()))
        print("TORNADO:" +str(self.vrednost_tornada.get()))
        x_novo = self.prosek(x_data)
        y_novo = self.prosek(y_data)
        z_novo = self.prosek(z_data)
        t_novo = self.prosek(tt)
        self.ax.set_xlim(min(x_novo)-2,max(x_novo)+2)
        self.ax.set_ylim(min(y_novo)-2,max(y_novo)+2)
        self.ax.set_zlim(0,max(z_novo)+2)
        self.line.set_data_3d(x_novo,y_novo,z_novo)
        self.canvas.draw()
    
    def promena_ugla(self,value):
        x_data, y_data, z_data, tt  = tornado(ALPHA=float(value),V0=float(self.slider_brzina.get()),TORNADO=float(self.vrednost_tornada.get()))
        print("V0:" +str(self.slider_brzina.get()))
        print("ALPHA:" +str(value))
        print("TORNADO:" +str(self.vrednost_tornada.get()))
        x_novo = self.prosek(x_data)
        y_novo = self.prosek(y_data)
        z_novo = self.prosek(z_data)
        t_novo = self.prosek(tt)
        self.ax.set_xlim(min(x_novo)-2,max(x_novo)+2)
        self.ax.set_ylim(min(y_novo)-2,max(y_novo)+2)
        self.ax.set_zlim(0,max(z_novo)+2)
        self.line.set_data_3d(x_novo,y_novo,z_novo)
        self.canvas.draw()
    
    def promena_tornada(self,value):
        x_data, y_data, z_data, tt  = tornado(ALPHA=float(self.slider_ugao.get()),V0=float(self.slider_brzina.get()),TORNADO=float(value))
        print("V0:" +str(self.slider_brzina.get()))
        print("ALPHA:" +str(self.slider_ugao.get()))
        print("TORNADO:" +str(value))
        x_novo = self.prosek(x_data)
        y_novo = self.prosek(y_data)
        z_novo = self.prosek(z_data)
        t_novo = self.prosek(tt)
        self.ax.set_xlim(min(x_novo)-2,max(x_novo)+2)
        self.ax.set_ylim(min(y_novo)-2,max(y_novo)+2)
        self.ax.set_zlim(0,max(z_novo)+2)
        self.line.set_data_3d(x_novo,y_novo,z_novo)
        self.canvas.draw()

root = Tk()
app = App(root)
root.mainloop()