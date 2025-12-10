# Harsh Patel
# 25, November, 2025

from dearpygui import dearpygui as dpg
import tkinter as tk
from tkinter import filedialog




def Choose_file():
    root = tk.Tk()
    root.withdraw()  

    file_path = filedialog.askdirectory(title="Select a file")

    root.destroy()
    return file_path

def take_picture_graph():
    file_path=Choose_file() + "/plot_pic.png"
    dpg.output_frame_buffer(file_path)
    

dpg.create_context()
with dpg.window(label="Data Visuals", width=1500, height=700 ):
    dpg.add_text("Dynamic Line Plot")
    x_data = [0,1,2,3,4,5]
    y_data = [0,3,5,3,7,8]
    
    with dpg.plot(label="line plot", width=1500, height=400):
        dpg.add_plot_legend()
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="X-Axis")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Y-Axis")
        line_series = dpg.add_line_series(x_data, y_data, label="line", parent=y_axis)
        
    dpg.add_button(label="Take picture of graph", callback=take_picture_graph)
    



dpg.create_viewport(title="lineplot graph", width=1500, height=700)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()