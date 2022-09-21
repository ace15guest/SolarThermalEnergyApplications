import math
import tkinter as tk
from tkinter import DoubleVar, IntVar, ttk, Label
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np


class ClearDayGui:
    def __init__(self, root=tk.Tk()):
        self.root = root
        self.root.geometry('1000x750')
        self.root.resizable(False, False)
        self.add_slide_bars()
        self.plot_place()
        self.gmt = np.arange(-12,12.1,.5)
        self.root.mainloop()

        pass

    def add_slide_bars(self):
        x_pos = 10
        label_spacing = 110

        self.day_var = IntVar()
        self.day_var.set(1)
        day = Label(self.root, text="Day: ").place(x=x_pos + label_spacing, y=10)
        day_label = Label(self.root, text=str(self.day_var.get()))
        day_label.place(x=x_pos + label_spacing + 50, y=10)
        day_slide = ttk.Scale(self.root, from_=1, to=365, variable=self.day_var,
                              command=lambda x: self.slider_change(slider_var=self.day_var, slider_label=day_label))
        day_slide.place(x=x_pos, y=10)

        self.altitude_var = DoubleVar()
        self.altitude_var.set(0.1)
        alt = Label(self.root, text="Altitude(Km): ").place(x=x_pos + label_spacing, y=30)
        alt_label = Label(self.root, text=str(self.altitude_var.get()))
        alt_label.place(x=x_pos + label_spacing + 90, y=30)

        altitude_slide = ttk.Scale(self.root, from_=0.01, to=10, variable=self.altitude_var,
                                   command=lambda x: self.slider_change(slider_var=self.altitude_var,
                                                                        slider_label=alt_label))
        altitude_slide.place(x=x_pos, y=30)

        self.latitude_var = DoubleVar()
        lat = Label(self.root, text="Latitude (deg): ").place(x=x_pos + label_spacing, y=50)
        lat_label = Label(self.root, text=str(self.altitude_var.get()))
        lat_label.place(x=x_pos + label_spacing + 100, y=50)

        latitude_slide = ttk.Scale(self.root, from_=0, to=90, variable=self.latitude_var,
                                   command=lambda x: self.slider_change(slider_var=self.latitude_var,
                                                                        slider_label=lat_label))
        latitude_slide.place(x=x_pos, y=50)


    def slider_change(self, slider_var, slider_label):
        slider_label.configure(text="{:.2f}".format(slider_var.get()))
        self.calculation_constants()
        self.varying_params()
        self.update_plot()

    def varying_params(self):
        self.omega = self.gmt*.2618
        self.sin_alpha = self.sin_delta*math.sin(self.phi) + math.cos(math.asin(self.sin_delta))*np.cos(self.omega)*math.cos(self.phi)
        self.k_sin_alpha = -self.K/self.sin_alpha
        self.raw_cd_factor = self.A0+self.A1*np.exp(self.k_sin_alpha)
        self.cd_factor=[]
        for el in self.raw_cd_factor:
            if el > 1:
                self.cd_factor.append(0)
            else:
                self.cd_factor.append(el)
        self.cd_factor = np.asarray(self.cd_factor)





    def calculation_constants(self):
        self.day_angle = (self.day_var.get() - 173) * 0.017453
        self.declination_angle = math.asin(.39795 * math.cos(self.day_angle)) * 57.2957
        self.phi = self.latitude_var.get() / 87.2957
        self.sin_delta = .39795*math.cos(self.day_angle)
        self.A0 = .4237 - .00821 * (6 - self.altitude_var.get()) ** 2
        self.A1 = .5055 - .00595 * (6 - self.altitude_var.get()) ** 2
        self.K = .2711 + .1858 * (2.5 - self.altitude_var.get()) ** 2

    def plot_place(self):
        self.fig = Figure(figsize = (8, 7), dpi = 100)
        x = [30,4,5,6]
        y = [1,2,3,4]
        self.plot1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        # placing the self.canvas on the Tkinter window
        self.canvas.get_tk_widget().place(x=250, y=10)

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas,self.root)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().place(x=250, y=10)

    def update_plot(self):
        try:
            self.plot1.clear()
            self.plot1.scatter(list(self.gmt), list(self.cd_factor))
            self.canvas.draw()
        except AttributeError:
            pass




ClearDayGui()
