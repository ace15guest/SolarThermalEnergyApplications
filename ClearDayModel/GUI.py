import math
import tkinter as tk
from tkinter import DoubleVar,IntVar, ttk, Label


class ClearDayGui:
    def __init__(self, root=tk.Tk()):
        self.root = root
        self.root.geometry('300x200')

        self.add_slide_bars()




        self.root.mainloop()
        pass

    def add_slide_bars(self):
        x_pos = 10
        label_spacing = 110

        self.day_var = IntVar()
        day = Label(self.root, text="Day: ").place(x=x_pos+label_spacing,y=10)
        day_label = Label(self.root, text=str(self.day_var.get()))
        day_label.place(x=x_pos+label_spacing+50,y=10)
        day_slide = ttk.Scale(self.root, from_=0, to=365, variable=self.day_var, command=lambda x: self.slider_change(slider_var=self.day_var, slider_label=day_label))
        day_slide.place(x=x_pos,y=10)




        self.altitude_var = DoubleVar()
        alt = Label(self.root, text="Altitude(Km): ").place(x=x_pos+label_spacing,y=30)
        alt_label = Label(self.root, text=str(self.altitude_var.get()))
        alt_label.place(x=x_pos + label_spacing + 90, y=30)

        altitude_slide = ttk.Scale(self.root, from_=0, to=10, variable=self.altitude_var, command=lambda x: self.slider_change(slider_var=self.altitude_var, slider_label=alt_label))
        altitude_slide.place(x=x_pos,y=30)



        self.latitude_var = DoubleVar()
        lat = Label(self.root, text="Latitude (deg): ").place(x=x_pos + label_spacing, y=50)
        lat_label = Label(self.root, text=str(self.altitude_var.get()))
        lat_label.place(x=x_pos + label_spacing + 100, y=50)

        latitude_slide = ttk.Scale(self.root, from_=0, to=90, variable=self.latitude_var, command=lambda x: self.slider_change(slider_var=self.latitude_var, slider_label=lat_label))
        latitude_slide.place(x=x_pos,y=50)

    def slider_change(self, slider_var, slider_label):
        slider_label.configure(text = "{:.2f}".format(slider_var.get()))

    def calculation_constants(self):
        self.day_angle = (self.day_var.get()-173)*0.017453
        self.declination_angle = math.asin(.39795*math.cos(self.day_angle))*57.2957
        self.phi = self.latitude_var.get()/87.2957
        self.A0 = .4237-.00821*(6-self.altitude_var.get())**2







ClearDayGui()
