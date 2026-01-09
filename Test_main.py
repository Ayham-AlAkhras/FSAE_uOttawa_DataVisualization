# Harsh Patel

import dearpygui.dearpygui as dpg
import tkinter as tk
from tkinter import filedialog


def print_me():
     pass


def Choose_file(text_box):
    root = tk.Tk()
    root.withdraw()  

    file_path = filedialog.askopenfilename(title="Select a file")

    root.destroy()
    dpg.set_value(text_box, file_path)


def import_data(file_path):
    pass


def filter_data(unfiltered_x_data, unfiltered_y_data, filter_type):

    if filter_type == "None":

        filtered_x_data = unfiltered_x_data
        filtered_y_data = unfiltered_y_data

    elif filter_type == "High-Pass":
        pass
    elif filter_type == "Low-Pass":
        pass
    elif filter_type == "Band-Pass":
        pass
    
    return (filtered_x_data, filtered_y_data)


def make_graph(name, file_path, graph_type, filter_type):

    unfiltered_x_data, unfiltered_y_data = import_data(file_path)
    filtered_x_data, filtered_y_data = filter_data(unfiltered_x_data, unfiltered_y_data, filter_type)

    if graph_type == "Line Graph":
        pass
    elif graph_type == "Bar Chart":
        pass
    elif graph_type == "Histogram":
        pass
    elif graph_type == "Scatter Plot":
        pass
    elif graph_type == "Pie Chart":
        pass
    elif graph_type == "Heat Map":
        pass


def graph_type_check(user_data):
    
    valid_graph_filter_pairs = {"Line Graph": ["High-Pass","Low-Pass","Band-Pass", "None"],
                                "Bar Chart": ["None"],
                                "Histogram": ["None"],
                                "Scatter Plot": ["High-Pass","Low-Pass","Band-Pass", "None"],
                                "Pie Chart": ["None"],
                                "Heat Map": ["High-Pass","Low-Pass","Band-Pass", "None"]
                                }
    
    name, file_path, graph_type, filter_type = user_data
    graph_type = dpg.get_value(graph_type)
    filter_type = dpg.get_value(filter_type)

    
    if (graph_type not in list(valid_graph_filter_pairs.keys()) or filter_type not in valid_graph_filter_pairs[graph_type]):
        if not dpg.does_item_exist("ask_graph"):
            with dpg.window(label="Type of Graph", modal=True, tag="ask_graph", no_title_bar=True, pos=[200,200] ):
                dpg.add_text("Please Reselect The Type of Graph!")
                dpg.add_separator()
                dpg.add_spacer(height=5)
                graph_type = dpg.add_combo( ["Line Graph","Bar Chart","Histogram","Scatter Plot", "Pie Chart", "Heat Map"],
                                default_value="Choose Type of Graph",)
            
                filter_type = dpg.add_combo( ["High-Pass","Low-Pass","Band-Pass", "None"],
                                default_value="Choose Type of Filter",)
            
                dpg.add_spacer(height=5)
                dpg.add_button(label="OK", width=75, callback=lambda: graph_type_check((name, file_path, graph_type, filter_type)))
    else:

        dpg.delete_item("ask_graph")
        dpg.split_frame()
        make_graph(name, file_path, graph_type, filter_type)


def file_path_check(user_data):

    name, file_path, graph_type, filter_type = user_data
    file_path = dpg.get_value(file_path)

    if (file_path == ""):
        if not dpg.does_item_exist("ask_file"):
            with dpg.window(label="File Path", modal=True, tag="ask_file", no_title_bar=True, pos=[200,200] ):
                dpg.add_text("Please Choose A File For the Graph Data!")
                dpg.add_separator()
                dpg.add_spacer(height=5)
                path_display = dpg.add_input_text(hint = "Selected File Path", readonly = True, width = 300)
                file_path_button = dpg.add_button(label="Choose File", callback=lambda: Choose_file(path_display))
                dpg.add_spacer(height=5)
                dpg.add_button(label="OK", width=75, callback=lambda: file_path_check((name, path_display, graph_type, filter_type)))
    else:

        user_data = (name, file_path, graph_type, filter_type)
        dpg.delete_item("ask_file")
        dpg.split_frame()
        graph_type_check(user_data)


def name_check(sender, app_data, user_data):

    name, file_path, graph_type, filter_type = user_data
    name = dpg.get_value(name)
    
    if (name == ""):
        if not dpg.does_item_exist("ask_name"):
            with dpg.window(label="Name", modal=True, tag="ask_name", no_title_bar=True, pos=[200,200] ):
                dpg.add_text("Please Enter A Name For The Graph!")
                dpg.add_separator()
                dpg.add_spacer(height=5)
                name_input = dpg.add_input_text( hint="Enter Graph Name", width=300)
                dpg.add_spacer(height=5)
                dpg.add_button(label="OK", width=75, callback=lambda: name_check( None, None, (name_input, file_path, graph_type, filter_type)))
    else:

        user_data = (name, file_path, graph_type, filter_type)
        dpg.delete_item("ask_name")
        dpg.split_frame()
        file_path_check(user_data)            


def make_graph_window( x, y, ht, wd):
    with dpg.window(pos=(x,y), height=ht, width=wd):
        with dpg.table(
        header_row=False,
        policy=dpg.mvTable_SizingFixedFit,   # columns can size to contents
        no_host_extendX=True,                # don't force table to fill parent width
        borders_innerV=True,
        borders_innerH=True,
        borders_outerV=True,
        borders_outerH=True,
    ):
        
        # Left spacer column stretches, middle is fixed-fit, right spacer stretches
            dpg.add_table_column(width_stretch=True,  init_width_or_weight=1.0)
            dpg.add_table_column(width_fixed=True,    init_width_or_weight=0.0)
            dpg.add_table_column(width_stretch=True,  init_width_or_weight=1.0)

            for r in range(9):

                with dpg.table_row():
                    dpg.add_spacer()  # left cell (takes remaining space)

                    if r == 3:

                        with dpg.group():
                            path_display = dpg.add_input_text(hint = "Selected File Path", readonly = True, width = 300)
                            file_path = dpg.add_button(label="Choose File", callback=lambda: Choose_file(path_display))

                    elif r == 1:

                        graph_name = dpg.add_input_text(hint="Enter Graph Name", width=300)

                    elif r == 5:

                        graph_type = dpg.add_combo(
                            ["Line Graph","Bar Chart","Histogram","Scatter Plot", "Pie Chart", "Heat Map"],
                            default_value="Choose Type of Graph",
                        )

                    elif r == 7:

                        filter_type = dpg.add_combo(
                            ["High-Pass","Low-Pass","Band-Pass", "None"],
                            default_value="Choose Type of Filter",
                        )

                    else:

                        dpg.add_spacer(height=(ht-150)/5)  # or dpg.add_spacer(height=0)
                    
                    if r != 7 :

                        dpg.add_spacer()

                    else: 

                        dpg.add_button(label="Submit",callback=name_check, user_data = (graph_name, path_display, graph_type, filter_type))

 


dpg.create_context()

dpg.create_viewport(title='Formula uOttawa Telemetry Software', width=800, height=600)




with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10.0)

dpg.bind_theme(global_theme)






with dpg.window(tag="Home Window", no_move=True, no_resize=True, pos=( 0, 0)):
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save", callback=print_me)
            dpg.add_menu_item(label="Save As", callback=print_me)

            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
                dpg.add_menu_item(label="Setting 2", callback=print_me)

        dpg.add_menu_item(label="Help", callback=make_graph_window(0, 18, 450, 775))

        with dpg.menu(label="Widget Items"):
            dpg.add_checkbox(label="Pick Me", callback=print_me)
            dpg.add_button(label="Press Me", callback=print_me)
            dpg.add_color_picker(label="Color Me", callback=print_me)






dpg.set_primary_window("Home Window", True)
dpg.setup_dearpygui()
dpg.set_viewport_pos([0,0])
dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()