import math
import tkinter as tk
from tkinter import DoubleVar, IntVar, ttk, Label, StringVar, Entry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline


class ClearDayGui:
    def __init__(self, root=tk.Tk()):
        self.root = root
        self.root.geometry('1250x750')
        self.root.resizable(False, False)
        self.slide_bars_place()

        self.solar_time = np.arange(-12, 12.1, .5)
        self.Inso_b_n = 0
        self.plot_place()
        self.caculation_static_labels()
        self.solar_time_func()

        self.root.mainloop()

        pass

    # Building GUI

    def slide_bars_place(self):
        x_pos = 10
        label_spacing = 110

        self.day_var = IntVar()
        self.day_var.set(1)

        day = Label(self.root, text="Day: ").place(x=x_pos + label_spacing, y=10)
        day_label = Label(self.root, text=str(self.day_var.get()))
        # day_label.place(x=x_pos + label_spacing + 50, y=10)
        day_slide = ttk.Scale(self.root, from_=1, to=365, variable=self.day_var,
                              command=lambda x: self.slider_change(slider_var=self.day_var, slider_label=day_label))
        day_slide.place(x=x_pos, y=10)
        day_e = Entry(self.root, textvariable=self.day_var)
        day_e.place(x=x_pos + label_spacing + 50, y=10, )

        self.altitude_var = DoubleVar()
        self.altitude_var.set(0.1)
        alt = Label(self.root, text="Altitude(Km): ").place(x=x_pos + label_spacing, y=30)
        alt_label = Label(self.root, text=str(self.altitude_var.get()))
        # alt_label.place(x=x_pos + label_spacing + 90, y=30)
        alt_entry = Entry(self.root, textvariable=self.altitude_var, width=10)
        alt_entry.place(x=x_pos + label_spacing + 90, y=30, )

        altitude_slide = ttk.Scale(self.root, from_=0.001, to=.5, variable=self.altitude_var,
                                   command=lambda x: self.slider_change(slider_var=self.altitude_var,
                                                                        slider_label=alt_label))
        altitude_slide.place(x=x_pos, y=30)

        self.latitude_var = DoubleVar()
        lat = Label(self.root, text="Latitude (deg): ").place(x=x_pos + label_spacing, y=50)
        lat_label = Label(self.root, text=str("{:.2f}".format(self.altitude_var.get())))
        # lat_label.place(x=x_pos + label_spacing + 100, y=50)
        lat_entry = Entry(self.root, textvariable=self.latitude_var, width=10)
        lat_entry.place(x=x_pos + label_spacing + 100, y=53, )

        latitude_slide = ttk.Scale(self.root, from_=-90, to=90, variable=self.latitude_var,
                                   command=lambda x: self.slider_change(slider_var=self.latitude_var,
                                                                        slider_label=lat_label))
        latitude_slide.place(x=x_pos, y=50)

        self.longiitude_var = DoubleVar()
        longi = Label(self.root, text="lat from GMT: ").place(x=x_pos + label_spacing, y=72)
        longi_label = Label(self.root, text=str("{:.2f}".format(self.altitude_var.get())))
        # longi_label.place(x=x_pos + label_spacing + 100, y=50)
        longi_entry = Entry(self.root, textvariable=self.longiitude_var, width=10)
        longi_entry.place(x=x_pos + label_spacing + 100, y=73, )

        longiitude_slide = ttk.Scale(self.root, from_=-180, to=180, variable=self.longiitude_var,
                                     command=lambda x: self.slider_change(slider_var=self.longiitude_var,
                                                                          slider_label=longi_label))
        longiitude_slide.place(x=x_pos, y=70)

        self.root.bind("<Return>", lambda x: self.slider_change(slider_var=self.latitude_var, slider_label=lat_label))

    def plot_place(self):
        self.fig = Figure(figsize=(8, 7), )
        self.plot1 = self.fig.add_subplot(111)
        self.fig.suptitle('Clear Day Insolation Factor')
        self.fig.supxlabel('Solar Hour (GMT)')
        self.fig.supylabel('Insolation Factor')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        # placing the self.canvas on the Tkinter window
        self.canvas.get_tk_widget().place(x=300, y=10)

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        toolbar.place(x=590, y=710)

        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().place(x=400, y=10)

    def caculation_static_labels(self):
        inso_label = Label(self.root, text="Bean Normal Insolation:")
        inso_label.place(x=0, y=100)
        self.inso_label = Label(self.root, text=str("{:.2f}".format(self.Inso_b_n * 1370) + "W/m^2"))
        self.inso_label.place(x=170, y=100)

    def calculation_labels(self):
        try:
            self.inso_label.configure(text="{:.2f}".format(self.Inso_b_n * 1370) + " W-h/m^2")
        except:
            pass

    def slider_change(self, slider_var, slider_label):
        slider_label.configure(text="{:.2f}".format(slider_var.get()))
        self.calculation_constants()
        self.varying_params()
        self.update_plot()
        self.calculation_labels()
        self.local_to_gmt()
    def solar_time_func(self):
        self.begin_time_var = IntVar()
        start = Label(self.root, text="Start (EST)")
        start.place(x=20, y=180)
        begin = Entry(self.root, textvariable=self.begin_time_var)
        begin.place(x=20, y=200)

        self.end_time_var = IntVar()
        end = Label(self.root, text="End (EST)")
        end.place(x=150, y=180)
        finish = Entry(self.root, textvariable=self.end_time_var)
        finish.place(x=150, y=200)

        self.begin_time_gmt_var = IntVar()
        start = Label(self.root, text="Start (GMT)")
        start.place(x=20, y=230)
        begin = Entry(self.root, textvariable=self.begin_time_gmt_var)
        begin.place(x=20, y=250)

        self.end_time_gmt_var = IntVar()
        end = Label(self.root, text="End (GMT)")
        end.place(x=150, y=230)
        finish = Entry(self.root, textvariable=self.end_time_gmt_var)
        finish.place(x=150, y=250)

    def varying_params(self):
        try:
            self.omega = self.solar_time * .2618
            self.sin_alpha = self.sin_delta * math.sin(self.phi) + math.cos(math.asin(self.sin_delta)) * np.cos(
                self.omega) * math.cos(self.phi)
            self.k_sin_alpha = -self.K / self.sin_alpha
            self.raw_cd_factor = self.A0 + self.A1 * np.exp(self.k_sin_alpha)
            self.cd_factor = []
            for el in self.raw_cd_factor:
                if el > 1:
                    self.cd_factor.append(0)
                else:
                    self.cd_factor.append(el)
            self.cd_factor = np.asarray(self.cd_factor)
        except:
            pass

    def calculation_constants(self):
        self.day_angle = (self.day_var.get() - 173) * 0.017453
        self.declination_angle = math.asin(.39795 * math.cos(self.day_angle)) * 57.2957
        self.phi = self.latitude_var.get() / 87.2957
        self.sin_delta = .39795 * math.cos(self.day_angle)
        self.A0 = .4237 - .00821 * (6 - self.altitude_var.get()) ** 2
        self.A1 = .5055 - .00595 * (6 - self.altitude_var.get()) ** 2
        self.K = .2711 + .1858 * (2.5 - self.altitude_var.get()) ** 2

    def update_plot(self):
        try:
            self.plot1.clear()
            f = InterpolatedUnivariateSpline(list(self.solar_time), list(self.cd_factor), k=1)
            xs = np.linspace(-12, 12, 500)
            self.plot1.plot(xs, f(xs))

            self.plot1.scatter(list(self.solar_time), list(self.cd_factor))
            self.fig.legend(['Spline for integration', 'Discrete Points'], loc='upper left')
            self.Inso_b_n = f.integral(0, 4)
            self.plot1.set_ylim([0, .4])

            self.canvas.draw()
        except AttributeError:
            pass

    def local_to_gmt(self):
        self.mu = self.longiitude_var.get()
        local = 12+self.begin_time_gmt_var.get() + self.mu / 15
        local_hr = math.floor(local)
        local_min = round((local % 1) * 60, 2)
        self.begin_time_var.set(str(local_hr) + ':' + str(int(local_min)))

        self.mu = self.longiitude_var.get()
        local = 12+self.end_time_gmt_var.get() + self.mu / 15
        local_hr = math.floor(local)
        local_min = round((local % 1) * 60, 2)
        self.end_time_var.set(str(local_hr) + ':' + str(int(local_min)))

        pass


ClearDayGui()
