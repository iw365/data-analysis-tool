


#   _____        _                               _           _       _______          _ 
#  |  __ \      | |            /\               | |         (_)     |__   __|        | |
#  | |  | | __ _| |_ __ _     /  \   _ __   __ _| |_   _ ___ _ ___     | | ___   ___ | |
#  | |  | |/ _` | __/ _` |   / /\ \ | '_ \ / _` | | | | / __| / __|    | |/ _ \ / _ \| |
#  | |__| | (_| | || (_| |  / ____ \| | | | (_| | | |_| \__ \ \__ \    | | (_) | (_) | |
#  |_____/ \__,_|\__\__,_| /_/    \_\_| |_|\__,_|_|\__, |___/_|___/    |_|\___/ \___/|_|
#                                                   __/ |                               
#                                                  |___/                                


#-------- MODULES --------#

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(script_dir, "root")
sys.path.append(root_dir)

import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
from CTkMenuBar import *
from CTkToolTip import *
from CTkTable import *
from PIL import Image

from modules.CTkXYFrame import ctk_xyframe
from modules.CTkScrollableDropdown import *

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

import json
import datetime as dt
import csv

from settings import active_light_theme, active_dark_theme, active_theme_type
from launcher_functions import *




# -------- RESOLUTION -------- #

#open settings file
with open('current-settings.json', 'r') as file:
    settings_data = json.load(file)
    
#set width and height from settings file
width = int(settings_data["window_width"])
height = int(settings_data["window_height"])

#close settings file
file.close()




# -------- COLOUR SCHEME FUNCTIONS -------- #

def hex_to_rgb(hex):
    return tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

rgb_to_hex = lambda rgb: '#{0:02x}{1:02x}{2:02x}'.format(rgb[0], rgb[1], rgb[2])

def lighten_color(hex_color, factor=0.25):
    rgb_color = hex_to_rgb(hex_color)
    lighter_rgb = tuple(int((255 - val) * factor + val) for val in rgb_color)
    return rgb_to_hex(lighter_rgb)

def darken_color(hex_color, factor=0.25):
    rgb_color = hex_to_rgb(hex_color)
    darker_rgb = tuple(int(val * (1 - factor)) for val in rgb_color)
    return rgb_to_hex(darker_rgb)



# UNUSED
# class middle_sub_frame_top(ctk.CTkFrame):
#     def __init__(self, parent, width, height):
#         self.width = width
#         self.height = height/6
#         super().__init__(parent, width=self.width, height=self.height, fg_color='#FFFF00', corner_radius = 0)
#         self.grid_propagate(False)
#         self.initialise_ui()
        
#     def initialise_ui(self):
#         pass

# class middle_sub_frame_middle(ctk.CTkFrame):
#     def __init__(self, parent, width, height):
#         self.width = width
#         self.height = (height/6)*4
#         super().__init__(parent, width=self.width, height=self.height, fg_color=primary, corner_radius = 0)
#         self.initialise_ui()
        
#     def initialise_ui(self):
#         pass

# class middle_sub_frame_bottom(ctk.CTkFrame):
#     def __init__(self, parent, width, height):
#         self.width = width
#         self.height = height/6
#         super().__init__(parent, width=self.width, height=self.height, fg_color='#00FFFF', corner_radius = 0)
#         self.initialise_ui()

#     def initialise_ui(self):
#         pass

class new_figure_popup(ctk.CTkToplevel):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.geometry('360x640')
        self.root = root
        self.initialise_ui()
        
    def initialise_ui(self):
        self.title("Exit")
        self.resizable(False, False) # disable resizing
        self.focus_force() # make window focused
        self.grab_set() # make window modal
        
        self.background = ctk.CTkFrame(master=self,
                                        width=360,
                                        height=640,
                                        fg_color=primary,
                                        corner_radius = 0)
        self.background.pack_propagate(False)
        self.background.grid_propagate(False)
        self.background.pack(padx=0, pady=0)
        
        self.plot_button = ctk.CTkButton(master=self.background,
                                        text="Plot",
                                        fg_color=primary,
                                        text_color=accent1,
                                        font=("Arial", 20),
                                        command=lambda: self.add_fig_callback(f"plot {fig_counter}"))
        self.plot_button.pack(pady=20, padx=20)
        
    def add_fig_callback(self, fig_name):
        self.root.update_current_figs(fig_name)
        global fig_counter
        fig_counter+=1
        self.destroy()
        

class current_figure_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width / 2
        self.height = height / 30
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        #fg_color="#FF0000",
                        corner_radius = 10)
        self.root = root
        
        global fig_counter
        fig_counter=1
        
        self.toplevel_window = None
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=5)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=5)
        
        self.initialise_ui()
    
    def initialise_ui(self):
        
        self.current_figure_dropdown = ctk.CTkOptionMenu(master=self,
                                                        width=self.width,
                                                        height=self.height,
                                                        values=self.root.current_figures,
                                                        fg_color=(accent1, primary),
                                                        button_color=(accent1, primary),
                                                        button_hover_color=(accent1_light, accent2),
                                                        dropdown_fg_color=(accent1, primary),
                                                        dropdown_hover_color=(accent1_light, accent2), 
                                                        dropdown_text_color="#FFFFFF",
                                                        corner_radius=10,
                                                        font=("Arial", 14))
        self.current_figure_dropdown.grid(row=0, column=0, padx=(0, 5), pady=(0, 0))
        
        print(self.root.current_figures)
        
        self.current_figure_dropdown_test = CTkScrollableDropdown(self.current_figure_dropdown,
                            values=self.root.current_figures,
                            fg_color=(primary, primary),
                            hover_color=(secondary_dark, secondary_light),
                            #hover_color=('#ff0000'),
                            frame_corner_radius=15,
                            frame_border_width=0,
                            button_color=(secondary, secondary),
                            scrollbar_button_color=(accent1, secondary),
                            resize=True)
        
        self.add_figure_button = ctk.CTkButton(master=self,
                                                width=self.width,
                                                height=self.height,
                                                fg_color=(primary, primary),
                                                hover_color=(primary_dark, primary_dark),
                                                border_width=0,
                                                border_color=(accent1, spare),
                                                corner_radius=10,
                                                text='+',
                                                text_color=(accent1, '#FFFFFF'),
                                                font=("Roboto", 20),
                                                command=self.add_figure_callback)
        self.add_figure_button.grid(row=0, column=1, padx=(0, 5), pady=(0, 0))
        
        self.remove_figure_button = ctk.CTkButton(master=self,
                                                width=self.width,
                                                height=self.height,
                                                fg_color=(primary, primary),
                                                hover_color=(primary_dark, primary_dark),
                                                border_width=0,
                                                border_color=(accent1, spare),
                                                corner_radius=10,
                                                text='x',
                                                text_color=(accent1, '#FFFFFF'),
                                                font=("Roboto", 20),
                                                command=self.debug)
        self.remove_figure_button.grid(row=0, column=2, padx=(0, 0), pady=(0, 0))
        
    def add_figure_callback(self):
        
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = new_figure_popup(self, root = self.root)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()
            
    def debug(self):
        print(self.root.current_figures)

class graph_tab_frame(ctk.CTkScrollableFrame):
    def __init__(self, parent, root, width, height):
        self.width = width
        self.height = height
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        #fg_color='#FF0000',
                        corner_radius = 10,
                        scrollbar_button_color=(accent1, primary),
                        scrollbar_button_hover_color=(accent1_light, primary_dark),)
        self.root = root
        #self.pack_propagate(False)
        #self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.editing_label = ctk.CTkLabel(master=self,
                                        width=self.width,
                                        height=self.height/40,
                                        fg_color=secondary,
                                        #fg_color="#FF0000",
                                        text_color=(accent1, '#FFFFFF'),
                                        corner_radius=10,
                                        font=("Arial", 14),
                                        text="Editing: ",
                                        anchor="w")
        self.editing_label.pack(padx=(22, 30), pady=(10, 0))
        
        self.current_figure_frame = current_figure_frame(parent = self, root = self.root, width = self.width, height = self.height)
        self.current_figure_frame.pack(padx=(30, 30), pady=(5, 0), expand = True, fill = "both")

class main_tabview(ctk.CTkTabview):
    def __init__(self, root, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(master=parent,
                        width=self.width,
                        height=self.height,
                        text_color=accent1,
                        fg_color=secondary,
                        corner_radius=10,
                        border_width=0,
                        border_color=accent1,
                        segmented_button_fg_color=(secondary, secondary),
                        segmented_button_selected_color=accent2,
                        segmented_button_unselected_color=(primary, primary),
                        segmented_button_selected_hover_color=accent2,
                        segmented_button_unselected_hover_color=(secondary_dark, primary_dark))
        
        self.root = root

        # create tabs
        self.add("Graph") # THIS WILL BE FOR CHANGING THE GRAPH TYPE + PARAMETERS
        self.add("Data") #THIS WILL BE FOR EXTRACTING DATA FROM FILE
        self.add("Appearance") # THIS WILL BE FOR CUSTOMIZING THE APPEARANCE OF THE GRAPH
        self.add("Modifiy") #THIS WILL BE FOR MODIFYING THE DATA 

        self.inititalise_ui()
        
    def inititalise_ui(self):
        
        # add a scrollabe frame instance to each of the tabs
        
        self.graph_tab_frame = graph_tab_frame(parent = self.tab("Graph"), root = self.root, width = self.width, height = self.height)
        # self.data_tab_frame = data_tab_frame(parent = self.tab("Data"), width = self.width, height = self.height)
        # self.appearance_tab_frame = appearance_tab_frame(parent = self.tab("Appearance"), width = self.width, height = self.height)
        # self.modify_tab_frame = modify_tab_frame(parent = self.tab("Modifiy"), width = self.width, height = self.height)
        
        # add widgets on tabs
        self.graph_tab_frame.pack(padx=0, pady=(0, 0), expand = True, fill = "both")
        # self.data_tab_frame.pack(padx=10, pady=(0, 10), expand = True, fill = "both")
        # self.appearance_tab_frame.pack(padx=10, pady=(0, 10), expand = True, fill = "both")
        # self.modify_tab_frame.pack(padx=10, pady=(0, 10), expand = True, fill = "both")

# CURRENTLY UNUSED
# --------------------------------------------------------------- #

class top_left_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = (height/4)*3
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        #fg_color=primary,
                        fg_color=primary,
                        corner_radius = 0)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.main_tabview = main_tabview(parent = self, width = self.width, height = self.height)
        self.main_tabview.pack(pady=(0, 10), padx=(10, 10))

class bottom_left_panel(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, 
                        width=(self.width),
                        height=(self.height),
                        border_width=0,
                        border_color=(accent1, accent1),
                        fg_color=(secondary),
                        corner_radius=10)
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass

class bottom_left_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = (height/4)
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=primary,
                        corner_radius = 0)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass
        
        #self.bottom_left_panel = bottom_left_panel(parent = self, width = self.width, height = self.height)
        #self.bottom_left_panel.pack(padx=(10, 10), pady=(10, 10))

# --------------------------------------------------------------- #

class left_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width/4
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color=primary, corner_radius = 0)
        self.pack_propagate(False)
        self.root=root
        self.initialise_ui()

    def initialise_ui(self):
        
        self.main_tabview = main_tabview(parent = self, root=self.root, width = self.width, height = self.height)
        self.main_tabview.pack(pady=(0, 10), padx=(10, 10))

class data_tabview(ctk.CTkTabview):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(master=parent,
                        width=self.width,
                        height=self.height,
                        text_color=accent1,
                        fg_color=secondary,
                        corner_radius=10,
                        border_width=0,
                        border_color=accent1,
                        segmented_button_fg_color=(secondary, secondary),
                        segmented_button_selected_color=accent2,
                        segmented_button_unselected_color=(primary, primary),
                        segmented_button_selected_hover_color=accent2,
                        segmented_button_unselected_hover_color=(secondary_dark, primary_dark))

        # create tabs
        self.add("Graph")
        self.add("Table")

        # add widgets on tabs
        self.frame = ctk.CTkFrame(master=self.tab("Graph"))
        self.frame.pack(padx=10, pady=(0, 10), expand = True, fill = "both")
        
        # self.fig = Figure(figsize=(5, 5), dpi=100)
        # self.plot = self.fig.add_subplot(111)
        # self.plot.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])
        
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack(expand = True, fill = "both")
        
        self.xy_table_frame = ctk_xyframe.CTkXYFrame(master = self.tab("Table"), 
                                                    fg_color=(secondary),
                                                    scrollbar_button_color=accent1,
                                                    scrollbar_button_hover_color=accent1_dark)
        self.xy_table_frame.pack(padx=(10, 10), pady=(0, 10), expand = True, fill = "both")
        
        self.values = [[0], [0]]
        
        self.table = CTkTable(master=self.xy_table_frame,
                                    font=("Arial", width/75),
                                    values = self.values,
                                    width = width/14,
                                    height = height/14,
                                    colors=(primary, primary_dark),
                                    border_width=0,
                                    border_color=(contrast_colour),
                                    padx=0,
                                    pady=0)
        
        #self.table.pack(padx = 10, pady = (0, 10))
        
        #cell_tooltip = CTkToolTip(self.table.frame[row, column], message="50") #! no idea
        # https://github.com/Akascape/CTkTable/discussions/15

class top_right_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = (height/4)*3
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=primary,
                        #fg_color="#FF0000",
                        corner_radius = 0)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.data_tabview = data_tabview(parent = self, width = self.width, height = self.height)
        self.data_tabview.pack(pady=(0, 10), padx=(10, 10))

class main_buttons_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, 
                        width=(self.width),
                        height=(self.height),
                        border_width=0,
                        border_color=(accent1, accent1),
                        fg_color=secondary,
                        corner_radius=10)
        self.grid_propagate(True)
        self.pack_propagate(True)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.root=root
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.main_button = ctk.CTkButton(master=self,
                                    #width = self.width,
                                    #height = self.height,
                                    fg_color=(primary, primary),
                                    hover_color=(primary_dark, primary_dark),
                                    border_width=0,
                                    border_color=(accent1, spare),
                                    corner_radius=10,
                                    text='upload file',
                                    text_color=(accent1, '#FFFFFF'),
                                    font=("Roboto", 20),
                                    command = self.main_button_callback)
        
        self.main_button.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        
        self.close_file_button = ctk.CTkButton(master=self,
                                    # width = self.width,
                                    # height = self.height,
                                    fg_color=(primary, primary),
                                    hover_color=(primary_dark, primary_dark),
                                    border_width=0,
                                    border_color=(accent1, spare),
                                    corner_radius=10,
                                    text='close file',
                                    text_color=(accent1, '#FFFFFF'),
                                    font=("Roboto", 20),
                                    command = self.close_file_callback)
        
    def main_button_callback(self):
        self.root.main_button_callback()
    
    def close_file_callback(self):
        self.root.close_file()

class bottom_options_panel(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, 
                        width=(self.width),
                        height=(self.height),
                        border_width=0,
                        border_color=(accent1, accent1),
                        fg_color=(secondary),
                        corner_radius=10)
        self.grid_propagate(False)
        self.pack_propagate(False)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.root=root
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.main_buttons_frame = main_buttons_frame(parent = self, root = self.root, width = self.width, height = self.height)
        self.main_buttons_frame.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky="nsew")
        self.main_buttons_frame.grid(row=0, column=0, sticky="nsew")
        
        self.button1 = ctk.CTkButton(master=self,
                                    #width = self.width,
                                    #height = self.height,
                                    fg_color=(primary, primary),
                                    hover_color=(primary_dark, primary_dark),
                                    border_width=0,
                                    border_color=(accent1, spare),
                                    corner_radius=10,
                                    text='button 1',
                                    text_color=(accent1, '#FFFFFF'),
                                    font=("Roboto", 20),
                                    command = self.button1_callback)
        
        self.button2 = ctk.CTkButton(master=self,
                                    #width = self.width,
                                    #height = self.height,
                                    fg_color=(primary, primary),
                                    hover_color=(primary_dark, primary_dark),
                                    border_width=0,
                                    border_color=(accent1, spare),
                                    corner_radius=10,
                                    text='button 2',
                                    text_color=(accent1, '#FFFFFF'),
                                    font=("Roboto", 20),
                                    command = self.button2_callback)
        
        self.button3 = ctk.CTkButton(master=self,
                                    #width = self.width,
                                    #height = self.height,
                                    fg_color=(primary, primary),
                                    hover_color=(primary_dark, primary_dark),
                                    border_width=0,
                                    border_color=(accent1, spare),
                                    corner_radius=10,
                                    text='button 3',
                                    text_color=(accent1, '#FFFFFF'),
                                    font=("Roboto", 20),
                                    command = self.button3_callback)
        
        self.button1.grid(row=0, column=1, padx=(5, 20), pady=(20, 5), sticky="nsew")
        self.button2.grid(row=1, column=0, padx=(20, 5), pady=(5, 20), sticky="nsew")
        self.button3.grid(row=1, column=1, padx=(5, 20), pady=(5, 20), sticky="nsew")
        
        # self.button1.grid(row=0, column=1, sticky="nsew")
        # self.button2.grid(row=1, column=0, sticky="nsew")
        # self.button3.grid(row=1, column=1, sticky="nsew")
        
    def button1_callback(self):
        print("button 1")
    
    def button2_callback(self):
        print("button 2")
    
    def button3_callback(self):
        print("button 3")

class bottom_options_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = ((width)/3)*2
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color=primary, corner_radius = 0)
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.root = root
        self.initialise_ui()
        
    def initialise_ui(self):
        self.bottom_options_panel = bottom_options_panel(parent = self, root = self.root, width = self.width, height = self.height)
        self.bottom_options_panel.pack(padx=(10, 10), pady=(10, 10))
        
class terminal_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = (width)/3
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color=primary, corner_radius = 0)
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.terminal_header_frame = ctk.CTkFrame(master=self,
                                                width=(self.width),
                                                height=(self.height/6)*1,
                                                border_width=0,
                                                fg_color=primary,
                                                corner_radius=10)
        
        self.terminal_header_frame.pack_propagate(False)
        self.terminal_header_frame.grid_propagate(False)
        self.terminal_header_frame.pack(padx=(0, 10), pady=(10, 5))
        
        # Add first frame with primary color
        self.terminal_header_frame_1 = ctk.CTkFrame(master=self.terminal_header_frame,
                                                    width=((self.width/8)*6)-20,
                                                    height=(self.height/6)*1,
                                                    fg_color="#0000FF",
                                                    corner_radius=10,
                                                    border_width=0)
        self.terminal_header_frame_1.grid(row=0, column=0, padx=(0, 5), pady=0)
        
        self.terminal_header_title_frame = ctk.CTkFrame(master=self.terminal_header_frame_1,
                                                        width=((self.width/8)*6)-20,
                                                        height=(self.height/6)*1,
                                                        bg_color=primary,
                                                        fg_color=secondary,
                                                        corner_radius=10,
                                                        border_width=0)

        self.terminal_header_title_frame.grid_propagate(False)
        self.terminal_header_title_frame.grid(row=0, column=0, padx=0, pady=0)
        
        self.terminal_header_title_label = ctk.CTkLabel(master=self.terminal_header_title_frame,
                                                        text="Terminal",
                                                        text_color=(accent1, '#FFFFFF'),
                                                        font=("Arial", 20))
        self.terminal_header_title_label.grid(row=0, column=0, padx=20, pady=5)
        
        # Add second frame with secondary color
        self.terminal_header_frame_2 = ctk.CTkFrame(master=self.terminal_header_frame,
                                                    width=(self.width/8)*1,
                                                    height=(self.height/6)*1,
                                                    fg_color=primary,
                                                    corner_radius=10,
                                                    border_width=0)
        self.terminal_header_frame_2.grid(row=0, column=1, padx=(0,5), pady=0)
        
        self.bin_icon = ctk.CTkImage(light_image=Image.open("assets/bin_icon_light.png"), dark_image=Image.open("assets/bin_icon_dark.png"), size=(round(width/64), round(height/36)))
        
        self.terminal_clear_button = ctk.CTkButton(master=self.terminal_header_frame_2,
                                    width = (self.width/8)*1,
                                    height = (self.height/6)*1,
                                    fg_color=secondary,
                                    hover_color=(secondary_dark, secondary_dark),
                                    border_width=0,
                                    border_color=(accent1, accent1),
                                    corner_radius=10,
                                    text='',
                                    image=self.bin_icon,
                                    text_color=accent1,
                                    font=("Arial", 14),
                                    command = self.clear_terminal)
        self.terminal_clear_button.pack(padx=(0, 0), pady=(0, 0))
        
        self.terminal_clear_tooltip = CTkToolTip(self.terminal_clear_button,
                                                corner_radius=10,
                                                message="Clear terminal") #!NEED TO ADD OTHER TOOLTIPS
        
        # Add third frame with tertiary color
        self.terminal_header_frame_3 = ctk.CTkFrame(master=self.terminal_header_frame,
                                                    width=(self.width/8)*1,
                                                    height=(self.height/6)*1,
                                                    fg_color=primary,
                                                    corner_radius=10,
                                                    border_width=0)
        self.terminal_header_frame_3.grid(row=0, column=2, padx=0, pady=0)
        
        self.download_icon = ctk.CTkImage(light_image=Image.open("assets/download_icon_light.png"), dark_image=Image.open("assets/download_icon_dark.png"), size=(round(width/64), round(height/36)))
        
        self.terminal_save_button = ctk.CTkButton(master=self.terminal_header_frame_3,
                                                width = (self.width/8)*1,
                                                height = (self.height/6)*1,
                                                fg_color=secondary,
                                                hover_color=(secondary_dark, secondary_dark),
                                                border_width=0,
                                                border_color=(accent1, accent1),
                                                corner_radius=10,
                                                text='',
                                                text_color=accent1,
                                                font=("Arial", 14),
                                                image=self.download_icon,
                                                command = self.save_terminal_to_file)
        self.terminal_save_button.pack(padx=(0, 0), pady=(0, 0))
        
        self.terminal_save_tooltip = CTkToolTip(self.terminal_save_button,
                                                corner_radius=10,
                                                message="Save terminal data to file") #!NEED TO ADD OTHER TOOLTIPS
        
        self.terminal = ctk.CTkTextbox(master=self,
                                    width=(self.width),
                                    height=((self.height/6)*5)-20,
                                    state="normal",
                                    font=("Consolas", round(width/128)),
                                    text_color=(accent1, '#FFFFFF'),
                                    scrollbar_button_color=(accent1, primary),
                                    scrollbar_button_hover_color=(accent1_light, primary_dark),
                                    fg_color=secondary,
                                    border_color=(accent1, accent1),
                                    border_width=0,
                                    corner_radius=10)
        # self.terminal.pack(padx=30, pady=(0,0), fill = "both", expand = False)
        self.terminal.pack(padx=(0, 10), pady=(0,10), expand = False)
        self.terminal.configure(state = "normal")
        self.terminal.insert("end", f"> APP START\n\n----------\n\n")
        self.terminal.configure(state = "disabled")
        
    def clear_terminal(self):
        self.terminal.configure(state = "normal")
        self.terminal.delete("0.0", "end")
        self.terminal.configure(state = "disabled")
        root.terminal_callback("TERMINAL CLEARED", "hard")
    
    def debug_callback(self):
        root.terminal_callback("DEBUG", "soft")
        print("debug")
        
    def save_terminal_to_file(self):
        directory = 'exports/terminal_data'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, f'terminal_data_{dt.datetime.now().strftime("%Y-%m-%d")}.txt'), 'w') as file:
            file.write(self.terminal.get('1.0', 'end'))
        root.terminal_callback("Terminal data saved", "hard")


class bottom_right_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width
        self.height = (height/4)
        super().__init__(parent, width=self.width, height=self.height, fg_color=(primary), corner_radius = 0)
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.root = root
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.bottom_options_frame = bottom_options_frame(parent = self, root = self.root, width = self.width, height = self.height)
        self.bottom_options_frame.grid(row=0, column=0, padx=0, pady=0)
        
        self.terminal_frame = terminal_frame(parent = self, width = self.width, height = self.height)
        self.terminal_frame.grid(row=0, column=1, padx=0, pady=0)

class right_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = (width/4)*3
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color=primary, corner_radius = 0)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.root = root
        self.initialise_ui()

    def initialise_ui(self):
        
        self.top_right_frame = top_right_frame(parent = self, width = self.width, height = self.height)
        self.top_right_frame.pack(padx=0, pady=(0, 0))
        
        self.bottom_right_frame = bottom_right_frame(parent = self, root = self.root, width = self.width, height = self.height)
        self.bottom_right_frame.pack(padx=0, pady=(0, 0))

class exit_dialogue_window(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('640x360')
        self.initialise_ui()
        
    def initialise_ui(self):
        self.title("Exit")
        self.resizable(False, False) # disable resizing
        self.focus_force() # make window focused
        self.grab_set() # make window modal
        
        self.exit_label = ctk.CTkLabel(master=self, text="Return to Launcher?", fg_color=primary, text_color=accent1, font=("Arial", 20))
        self.exit_label.pack(pady=20, padx=20)
        
        self.exit_yes_button = ctk.CTkButton(master=self, text="Yes", fg_color=accent1, text_color=primary, font=("Arial", 20), command=self.exit_yes_callback)
        self.exit_yes_button.pack(pady=20, padx=20)
        
        self.exit_no_button = ctk.CTkButton(master=self, text="No", fg_color=accent1, text_color=primary, font=("Arial", 20), command=self.exit_no_callback)
        self.exit_no_button.pack(pady=20, padx=20)
        
        self.cancel_button = ctk.CTkButton(master=self, text="Cancel", fg_color=accent1, text_color=primary, font=("Arial", 20), command=self.cancel_callback)
        self.cancel_button.pack(pady=20, padx=20)
        
    def exit_yes_callback(self):
        root.destroy()
        launch_app_reg('launcher.py')
        
    def exit_no_callback(self):
        root.destroy()
        
    def cancel_callback(self):
        self.destroy()

class root(tk.Tk):
    def __init__(self):
        self.width = width
        self.height = height
        self.file_active = False
        super().__init__()
        self.title("Data Analysis Tool")
        
        self.geometry(f'{self.width}x{self.height}+50+50')
        #self.iconbitmap('classes/empty.ico') #change icon
        #ctk.set_appearance_mode("Light")
        
        #create some lists
        self.current_figures = []

        self.initialise_ui()

    def initialise_ui(self):
        
        self.left_frame = left_frame(parent = self, root = self, width = self.width, height = self.height)
        #self.middle_frame = middle_frame(parent = self,  width = self.width, height = self.height)
        self.right_frame = right_frame(parent = self, root = self, width = self.width, height = self.height)

        self.left_frame.grid(row=0, column=0, padx=0, pady=0)
        #self.middle_frame.grid(row=0, column=1, padx=0, pady=0)
        self.right_frame.grid(row=0, column=2, padx=0, pady=0)
        
        self.toplevel_window = None
    
    def main_button_callback(self):
        if self.file_active == False:
            self.upload_file()
        elif self.file_active == True:
            self.run_tool(self.filename)
    
    def upload_file(self):
        root.terminal_callback(f"File Dialogue opened", "soft")
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File", filetypes=((("CSV files", "*.csv"), ("All files", "*.*"))))
        print(self.filename)
        
        if not self.filename:
            print("No file selected.")
            self.terminal_callback("No file selected", "soft")
        elif not os.path.isfile(self.filename):
            print("File not found.")
            self.terminal_callback("File not found", "soft")
        elif not self.filename.endswith('.csv'):
            print("File is not a CSV file.")
            self.terminal_callback("File is not a CSV file", "soft")
        else:
            root.terminal_callback(f"FILE SELECTED: {self.filename}", "hard")
            self.file_active = True
            self.refresh_ui()
            
            self.right_frame.top_right_frame.data_tabview.table.pack(padx = (0, 0), pady = (0, 00))
            
            self.run_tool(self.filename)
            
            #switch tab to table tab
            self.right_frame.top_right_frame.data_tabview.set("Table")
    
    
    # ---- MAIN RUNNING METHOD --------------------------------------------------------------- #
    def run_tool(self, filename):
        print("guh")
        print(filename)
        
        # Initialise arrays
        
        self.raw_x_data = [] #will be changed when user selects axis data
        self.raw_y_data = []
        self.raw_z_data = []
        
        self.raw_data = []
        
        self.table_data = []
        self.graph_data = []
        
        # table data
        # translate csv data into a format that can be used by the table
        
        with open(filename, 'r') as csvfile:
            self.csvreader = csv.reader(csvfile)
            # self.headers = next(self.csvreader)
            # self.x_label = self.headers[0]
            # self.y_label = self.headers[1]
            for row in self.csvreader:
                # self.raw_x_data.append(row[0])
                # self.raw_y_data.append(row[1])
                self.raw_data.append(row)
        print(self.raw_data)
        
        #split data into pairs of x and y values - e.g. [[x1, y1], [x2, y2], [x3, y3]]
        #self.table_data = list(zip(self.raw_x_data, self.raw_y_data, self.raw_z_data))
        #print(self.table_data)
        
        self.column_data = list(map(list, zip(*self.raw_data)))
        print(self.column_data)
        
        # calculate new number of rows and columns for table
        self.new_rows = len(self.raw_data)
        self.new_columns = len(self.raw_data[0])
        
        # check if table already exists
        if self.right_frame.top_right_frame.data_tabview.table is not None:
            # if it does, get its current number of rows and columns
            self.old_rows = self.right_frame.top_right_frame.data_tabview.table.rows
            self.old_columns = self.right_frame.top_right_frame.data_tabview.table.columns
            
            print(self.old_rows, self.old_columns, self.new_rows, self.new_columns)
            
            #compare old and new number of rows
            if self.old_rows == self.new_rows:
                pass
            elif self.old_rows < self.new_rows:
                #if new rows are greater than old rows, add new rows
                for i in range(self.new_rows - self.old_rows):
                    self.right_frame.top_right_frame.data_tabview.table.add_row(list(self.raw_data[i]))
            elif self.old_rows > self.new_rows:
                #if new rows are less than old rows, remove rows
                for i in range(self.old_rows - self.new_rows):
                    print('if this runs something is horribly wrong')
                    self.right_frame.top_right_frame.data_tabview.table.delete_row()
                
            #compare old and new number of columns
            if self.old_columns == self.new_columns:
                pass
            elif self.old_columns < self.new_columns:
                #if new columns are greater than old columns, add new columns
                for i in range(self.new_columns - self.old_columns):
                    self.right_frame.top_right_frame.data_tabview.table.add_column((self.raw_data[i]))
            elif self.old_columns > self.new_columns:
                #if new columns are less than old columns, remove columns
                for i in range(self.old_columns - self.new_columns):
                    self.right_frame.top_right_frame.data_tabview.table.delete_column()
        
        self.right_frame.top_right_frame.data_tabview.table.update_values(self.raw_data)
        
        # graph data
        
    def close_file(self):
        
        self.right_frame.top_right_frame.data_tabview.table.pack_forget()
        
        self.file_active = False
        print("closed file")
        self.refresh_ui()
    
    def refresh_ui(self): #! set file_active to its new value BEFORE running this function
        
        self.bottom = self.right_frame.bottom_right_frame.bottom_options_frame.bottom_options_panel
        
        if self.file_active == True:
            
            self.bottom.main_buttons_frame.close_file_button.grid(row=0, column=1, padx=(5, 0), pady=(0, 0), sticky="nsew")
            self.grid_columnconfigure(0, weight=3)
            self.grid_columnconfigure(1, weight=1)
            self.bottom.main_buttons_frame.main_button.configure(text="RUN")
            
            self.bottom.grid_rowconfigure(0, weight=1)
            self.bottom.grid_rowconfigure(1, weight=1)
            
            self.bottom.grid_columnconfigure(0, weight=1)
            self.bottom.grid_columnconfigure(1, weight=1)
            
            #self.right_frame.top_right_frame.data_tabview.xy_table_frame.configure(fg_color=contrast_colour)

        elif self.file_active == False:
            
            self.bottom.main_buttons_frame.close_file_button.grid_forget()
            self.bottom.main_buttons_frame.main_button.configure(text="upload file")
            
    def exit_app_callback(self):
        #root.destroy()
        
        with open('current-settings.json', 'r') as file:
            settings_data = json.load(file)
        
        if settings_data["keep_launcher_open_on_app_launch"] == "False": #will cause error if value is changed from launcher while app is running
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = exit_dialogue_window(self)  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()
        else:
            root.destroy()
    
    def terminal_callback(self, text, type):
        
        with open('current-settings.json', 'r') as file:
            settings_data = json.load(file)
            
        if settings_data["show_date_in_terminal"] == "True":
            date_if_enabled = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_date_if_enabled = f"[{date_if_enabled}]"
        else:
            formatted_date_if_enabled = ""
            
        match type:
            case "soft":
                self.right_frame.bottom_right_frame.terminal_frame.terminal.configure(state = "normal")
                self.right_frame.bottom_right_frame.terminal_frame.terminal.insert("end", f"{formatted_date_if_enabled} > {text}\n\n")
                self.right_frame.bottom_right_frame.terminal_frame.terminal.configure(state = "disabled")
            case "hard":
                self.right_frame.bottom_right_frame.terminal_frame.terminal.configure(state = "normal")
                self.right_frame.bottom_right_frame.terminal_frame.terminal.insert("end", f"{formatted_date_if_enabled} > {text}\n\n----------\n\n")
                self.right_frame.bottom_right_frame.terminal_frame.terminal.configure(state = "disabled")
                
    def update_current_figs(self, fig):
        self.current_figures.append(fig)
        self.left_frame.main_tabview.graph_tab_frame.current_figure_frame.current_figure_dropdown.configure(values=self.current_figures)
        self.left_frame.main_tabview.graph_tab_frame.current_figure_frame.current_figure_dropdown_test.configure(values=self.current_figures)
        print(self.current_figures)

if __name__ == "__main__":
    
    with open('themes.json', 'r') as file:
        themes_data = json.load(file)
    
    global contrast_colour
    
    match active_theme_type:
        case 'light':
            theme = themes_data["light"][f"{active_light_theme}"]
            ctk.set_appearance_mode("light") # Modes: "System" (standard), "Dark", "Light"
            contrast_colour = "#000000"
        case 'dark':
            theme = themes_data["dark"][f"{active_dark_theme}"]
            print('debug i hate this')
            ctk.set_appearance_mode("dark") # Modes: "System" (standard), "Dark", "Light"
            contrast_colour = "#FFFFFF"
            

    primary = theme['primary']
    secondary = theme['secondary']
    accent1 = theme['accent1']
    accent2 = theme['accent2']
    spare = theme['spare']
    
    primary_light = lighten_color(primary)
    secondary_light = lighten_color(secondary)
    accent1_light = lighten_color(accent1)
    accent2_light = lighten_color(accent2)
    print(primary, secondary, accent1, accent2, spare)

    primary_dark = darken_color(primary)
    secondary_dark = darken_color(secondary)
    accent1_dark = darken_color(accent1)
    accent2_dark = darken_color(accent2)
    
    root = root()
    root.protocol("WM_DELETE_WINDOW", root.exit_app_callback)
    root.mainloop()