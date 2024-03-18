


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
import platform
import math

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
try:
    import pywinstyles
#if import error
except ImportError:
    pass

from modules.CTkXYFrame import ctk_xyframe
from modules.CTkScrollableDropdown import *
from tabview_options import x_axis_selector_frame, y_axis_selector_frame

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from matplotlib import gridspec as gs

import json
import datetime as dt
import csv

from settings import active_light_theme, active_dark_theme, active_theme_type, primary, secondary, accent1, accent2, spare, primary_light, secondary_light, accent1_light, accent2_light, primary_dark, secondary_dark, accent1_dark, accent2_dark
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
                                        command=lambda: self.root.add_fig_callback(f"plot-{fig_counter}"))
        self.plot_button.pack(pady=20, padx=20)
        
        self.update()
        self.grab_set() # make window modal

class current_figure_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width / 2
        self.height = height / 30
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=primary,
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
        self.grid_columnconfigure(1, weight=2000000) # this is a hacky way to make the dropdown fill the space
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=2000000) # idk what is going on really - it shouldnt need to be this big, and it should be the other way round
        
        self.initialise_ui()
    
    def initialise_ui(self):
        
        self.current_figure_dropdown = ctk.CTkOptionMenu(master=self,
                                                        width=self.width,
                                                        height=self.height,
                                                        values=self.root.current_figures,
                                                        fg_color=(accent1, secondary),
                                                        button_color=(accent1, secondary),
                                                        button_hover_color=(accent1_light, accent2),
                                                        dropdown_fg_color=(accent1, secondary),
                                                        dropdown_hover_color=(accent1_light, accent2), 
                                                        dropdown_text_color="#FFFFFF",
                                                        corner_radius=10,
                                                        font=("Arial", 14),
                                                        state='disabled',
                                                        command=self.root.change_fig)
        self.current_figure_dropdown.grid(row=0, column=0, padx=(0, 5), pady=(0, 0))
        
        print(self.root.current_figures)
        
        self.current_figure_dropdown_test = CTkScrollableDropdown(self.current_figure_dropdown,
                                                                    values=self.root.current_figures,
                                                                    fg_color=(primary, secondary),
                                                                    hover_color=(secondary_dark, primary_light),
                                                                    #hover_color=('#ff0000'),
                                                                    frame_corner_radius=15,
                                                                    frame_border_width=2,
                                                                    frame_border_color=(accent1, primary),
                                                                    button_color=(secondary, primary),
                                                                    scrollbar_button_color=(accent1, primary),
                                                                    resize=True,
                                                                    state='disabled',
                                                                    command=self.root.change_fig)
        
        self.add_figure_button = ctk.CTkButton(master=self,
                                                width=self.width,
                                                height=self.height,
                                                fg_color=(primary, secondary),
                                                hover_color=(primary_dark, secondary_dark),
                                                border_width=0,
                                                border_color=(accent1, spare),
                                                corner_radius=10,
                                                text='+',
                                                text_color=(accent1, '#FFFFFF'),
                                                font=("Roboto", 20),
                                                state='disabled',
                                                command=self.add_figure_callback)
        self.add_figure_button.grid(row=0, column=1, padx=(0, 5), pady=(0, 0))
        
        self.remove_figure_button = ctk.CTkButton(master=self,
                                                width=self.width,
                                                height=self.height,
                                                fg_color=(primary, secondary),
                                                hover_color=(primary_dark, secondary_dark),
                                                border_width=0,
                                                border_color=(accent1, spare),
                                                corner_radius=10,
                                                text='x',
                                                text_color=(accent1, '#FFFFFF'),
                                                font=("Roboto", 20),
                                                state='disabled',
                                                command=self.root.remove_fig)
        self.remove_figure_button.grid(row=0, column=2, padx=(0, 0), pady=(0, 0))
        
    def add_figure_callback(self):
        
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = new_figure_popup(self, root = self.root)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()

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
        
        self.test_label = ctk.CTkLabel(master=self,
                                        width=self.width,
                                        height=self.height/40,
                                        fg_color=secondary,
                                        #fg_color="#FF0000",
                                        text_color=(accent1, '#FFFFFF'),
                                        corner_radius=10,
                                        font=("Arial", 14),
                                        text="TEST",
                                        anchor="w")
        self.test_label.pack(padx=(10, 10), pady=(20, 0))

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
        self.editing_label.pack(padx=(10, 10), pady=(20, 0))
        
        self.current_figure_frame = current_figure_frame(parent = self, root = self.root, width = self.width, height = self.height)
        self.current_figure_frame.pack(padx=(10, 10), pady=(5, 0), expand = True, fill = "both")
        
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
        self.frame = ctk.CTkFrame(master=self.tab("Graph"), fg_color=secondary)
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
        self.resizable(False, False) # disable resizing
        if platform.system() == "Windows":
            #pywinstyles.apply_style(self, "mica")
            pywinstyles.change_header_color(self, primary)
        
        self.geometry(f'{self.width}x{self.height}+50+50')
        #self.iconbitmap('classes/empty.ico') #change icon
        #ctk.set_appearance_mode("Light")
        
        #create some lists
        self.current_figures = ['No figures created']
        self.fig_data = {}

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
            
            self.run_tool(self.filename)
            self.right_frame.top_right_frame.data_tabview.table.pack(padx = (0, 0), pady = (0, 00))
            
            #clear the fig_data json file
            with open('fig_data.json', 'w') as file:
                file.write("{}")
            
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
        #self.column_data = []
        
        # table data
        # translate csv data into a format that can be used by the table
        
        with open(filename, 'r', encoding='utf-8-sig') as csvfile:
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
        print(f'column data: {self.column_data}')
        
        self.right_frame.top_right_frame.data_tabview.table = CTkTable(master = self.right_frame.top_right_frame.data_tabview.xy_table_frame,
                                                                        font=("Arial", width/75),
                                                                        values = self.raw_data,
                                                                        width = width/14,
                                                                        height = height/14,
                                                                        colors=(primary, primary_dark),
                                                                        border_width=0,
                                                                        border_color=(contrast_colour),
                                                                        padx=0,
                                                                        pady=0)

        self.right_frame.top_right_frame.data_tabview.table.update_values(self.raw_data)
        
        # graph stuff
        
        # clear all current graphs
        for widget in self.right_frame.top_right_frame.data_tabview.frame.winfo_children():
            widget.pack_forget()
        
        #put data into list
        try:
            self.column_headers = self.raw_data[0]
            print(f'column headers: {self.column_headers}')
            
            if self.left_frame.current_figure_frame.current_figure_dropdown.get() != "No figures created":
                
                self.selected_figure = self.left_frame.current_figure_frame.current_figure_dropdown.get()
                self.fig_data[self.selected_figure] = {}
                self.fig_data[self.selected_figure]['x_axis'] = str(self.left_frame.main_tabview.graph_tab_frame.x_axis_selector_frame.x_axis_selector_dropdown.get())
                self.fig_data[self.selected_figure]['y_axis'] = str(self.left_frame.main_tabview.graph_tab_frame.y_axis_selector_frame.y_axis_selector_dropdown.get())
                
                self.fig_data[self.selected_figure]['x_data'] = self.column_data[self.column_headers.index(self.fig_data[self.selected_figure]['x_axis'])]
                self.fig_data[self.selected_figure]['y_data'] = self.column_data[self.column_headers.index(self.fig_data[self.selected_figure]['y_axis'])]
                print(f'DEBUG AAAA\n\n{self.fig_data}\n\n')
                
                self.json_data = json.dumps(self.fig_data)
                with open('fig_data.json', 'w') as file:
                    file.write(self.json_data)
        except AttributeError:
            print("test")
        
        #go through each figure in fig_data and add a figure to a canvas for each one
        
        #use number of figures to determine how many subplots to create
        
        # #check if the length of fig_data is a square nuner
        # if math.sqrt(len(self.fig_data)).is_integer():
        #     self.graph_columns = int(math.sqrt(len(self.fig_data)))
        #     self.graph_rows = int(math.sqrt(len(self.fig_data)))
        #     print("length of list is square")
        # else:
        #     #always round up 
        #     self.graph_columns = int(math.ceil(math.sqrt(len(self.fig_data))))
        #     self.graph_rows = int(self.graph_columns)
        #     print("length of list is not square")
        
        # print(f'graph columns: {self.graph_columns}')
        # print(f'graph rows: {self.graph_rows}')
        
        # self.current_graph = 0
        # print(self.graph_columns)
        # print(self.graph_rows)
        
        # #get the size of the graph holder frame
        # self.graph_holder_width = self.right_frame.top_right_frame.data_tabview.frame.winfo_width()
        # print(f'graph holder width: {self.graph_holder_width}')
        
        #TODO
        
        try:
            self.columns = math.ceil(math.sqrt(len(self.fig_data)))
            self.base_rows = len(self.fig_data)//self.columns
            self.extra_rows = len(self.fig_data)%self.columns
        except ZeroDivisionError:
            self.columns = 1
            self.base_rows = 1
            self.extra_rows = 0
        
        print(f'columns: {self.columns}')
        print(f'base rows: {self.base_rows}')
        print(f'extra rows: {self.extra_rows}')
        
        self.total_rows = self.base_rows + (self.extra_rows > 0)
        
        self.fig = plt.Figure(figsize=(5, 5), dpi=100)
        self.plot_num = 1
        
        # UNFINISHED
        
        if self.current_figures[0] != 'No figures created':
        
            for row in range(self.base_rows):
                for column in range(self.columns):
                    self.ax = self.fig.add_subplot(self.total_rows, self.columns, self.plot_num)
                    
                    print(f'plot num: {self.plot_num}\n\n')
                    print(f'fig_data: {self.fig_data}\n\n')
                    print(f'current figures: {self.current_figures}\n\n')
                    print(f'current figure: {self.current_figures[self.plot_num - 1]}\n\n')
                    print(f'current figure x data: {self.fig_data[self.current_figures[self.plot_num - 1]]['x_data']}\n\n')
                    
                    try:
                        pass
                    except KeyError:
                        print("no data")
                    
                    self.x_axis_data_list = self.fig_data[self.current_figures[self.plot_num - 1]]['x_data']
                    self.y_axis_data_list = self.fig_data[self.current_figures[self.plot_num - 1]]['y_data']
                    self.x_axis_data_title = self.x_axis_data_list.pop(0)
                    self.y_axis_data_title = self.y_axis_data_list.pop(0)
                    print(f'x axis data: {self.x_axis_data_list}')
                    print(f'y axis data: {self.y_axis_data_list}')
                    
                    self.ax.plot(self.x_axis_data_list, self.y_axis_data_list)
                    
                    #add titles
                    self.ax.set_title(self.current_figures[self.plot_num - 1])
                    self.ax.set_xlabel(self.x_axis_data_title)
                    self.ax.set_ylabel(self.y_axis_data_title)
                    
                    self.plot_num += 1
                    
            if self.extra_rows > 0:
                for column in range(self.extra_rows):
                    self.ax = self.fig.add_subplot(self.total_rows, self.columns, self.plot_num)
                    
                    print(f'plot num: {self.plot_num}\n\n')
                    print(f'fig_data: {self.fig_data}\n\n')
                    print(f'current figures: {self.current_figures}\n\n')
                    print(f'current figure: {self.current_figures[self.plot_num - 1]}\n\n')
                    print(f'current figure x data: {self.fig_data[self.current_figures[self.plot_num - 1]]['x_data']}\n\n')
                    
                    try:
                        #use plot num to read from fig_data
                        #print(self.fig_data[self.current_figures[self.plot_num-1]])
                        pass
                    except KeyError:
                        print("no data")
                        
                    self.x_axis_data_list = self.fig_data[self.current_figures[self.plot_num - 1]]['x_data']
                    self.y_axis_data_list = self.fig_data[self.current_figures[self.plot_num - 1]]['y_data']
                    self.x_axis_data_title = self.x_axis_data_list.pop(0)
                    self.y_axis_data_title = self.y_axis_data_list.pop(0)
                    print(f'x axis data: {self.x_axis_data_list}')
                    print(f'y axis data: {self.y_axis_data_list}')
                    
                    self.ax.plot(self.x_axis_data_list, self.y_axis_data_list)
                    
                    #add titles
                    self.ax.set_title(self.current_figures[self.plot_num - 1])
                    self.ax.set_xlabel(self.x_axis_data_title)
                    self.ax.set_ylabel(self.y_axis_data_title)
                    
                    self.plot_num += 1
            
            #remove unused axes
            if self.plot_num < self.total_rows*self.columns:
                for i in range(self.plot_num, self.total_rows*self.columns + 1):
                    self.fig.delaxes(self.fig.axes[i-1])
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame.top_right_frame.data_tabview.frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(expand = True, fill = "both")
            
            #switch tab to table tab
            self.right_frame.top_right_frame.data_tabview.set("Graph")
        
        
    def close_file(self):
        
        #clean up
        self.right_frame.top_right_frame.data_tabview.table.pack_forget()
        self.current_figures = ['No figures created']
        
        #empty the json file
        with open('fig_data.json', 'w') as file:
            file.write("{}")
            
        #clear all tabs
        for widget in self.left_frame.main_tabview.graph_tab_frame.winfo_children():
            widget.pack_forget()
        # for widget in self.right_frame.top_right_frame.data_tab_frame.winfo_children():
        #     widget.pack_forget()
        # for widget in self.right_frame.top_right_frame.appearance_tab_frame.winfo_children():
        #     widget.pack_forget()
        # for widget in self.right_frame.top_right_frame.modify_tab_frame.winfo_children():
        #     widget.pack_forget()
        
        
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
            self.left_frame.current_figure_frame.add_figure_button.configure(state = 'normal')
            self.left_frame.current_figure_frame.remove_figure_button.configure(state = 'normal')

        elif self.file_active == False:
            
            self.bottom.main_buttons_frame.close_file_button.grid_forget()
            self.bottom.main_buttons_frame.main_button.configure(text="upload file")
            
            self.left_frame.current_figure_frame.add_figure_button.configure(state = 'disabled')
            self.left_frame.current_figure_frame.remove_figure_button.configure(state = 'disabled')
            
    def change_fig(self, plot):
        
        self.run_tool(self.filename)
        print(f"debug: {plot}")
        self.left_frame.current_figure_frame.current_figure_dropdown.set(plot)
        
        #split the string at the first hyphen and take the first part
        self.plot_type = plot
        print(self.plot_type)
        
        self.show_fig_options(self.plot_type)
        
    def update_json_callback(self, field_to_edit, new_value_widget):
        self.selected_figure = self.left_frame.current_figure_frame.current_figure_dropdown.get()
        self.fig_data[self.selected_figure] = {}
        self.fig_data[self.selected_figure][field_to_edit] = str(new_value_widget.get())
        print(self.fig_data)
        
        self.json_data = json.dumps(self.fig_data)
        with open('fig_data.json', 'w') as file:
            file.write(self.json_data)

    def add_fig_callback(self, fig_name):
        
        if self.current_figures[0] == 'No figures created':
            self.current_figures.pop(0)
            self.left_frame.current_figure_frame.current_figure_dropdown.configure(state='normal')
            self.left_frame.current_figure_frame.current_figure_dropdown_test.configure(state='normal')
        
        self.current_figures.append(fig_name)
        self.left_frame.current_figure_frame.current_figure_dropdown.configure(values=self.current_figures)
        self.left_frame.current_figure_frame.current_figure_dropdown_test.configure(values=self.current_figures)
        print(self.current_figures)
        
        global fig_counter
        fig_counter+=1
        self.left_frame.current_figure_frame.toplevel_window.destroy()
        self.left_frame.current_figure_frame.current_figure_dropdown.set(fig_name)
        
        #split the string at the first hyphen and take the first part
        self.plot_type = fig_name
        print(self.plot_type)
        
        self.show_fig_options(self.plot_type)
    
    def remove_fig(self):
        
        self.current_figures.remove(self.left_frame.current_figure_frame.current_figure_dropdown.get())
        
        #clear the figures json file
        with open('fig_data.json', 'r') as file:
            self.temp_data = json.load(file)
        
        if self.left_frame.current_figure_frame.current_figure_dropdown.get() in self.temp_data:
            del self.temp_data[self.left_frame.current_figure_frame.current_figure_dropdown.get()]
        
        with open('fig_data.json', 'w') as file:
            json.dump(self.temp_data, file)
            
        #remove the figure data from the fig_data list
        self.fig_data = self.temp_data
        
        # set the dropdown to the figure before
        try:
            self.change_fig_options = True
            self.left_frame.current_figure_frame.current_figure_dropdown.set(self.current_figures[-1])
        except IndexError:
            try:
                self.change_fig_options = True
                self.left_frame.current_figure_frame.current_figure_dropdown.set(self.current_figures[+1])
            except IndexError:
                self.change_fig_options = False
                self.current_figures.append('No figures created')
                self.left_frame.current_figure_frame.current_figure_dropdown.set(self.current_figures[0])
                self.left_frame.current_figure_frame.current_figure_dropdown.configure(state='disabled')
                self.left_frame.current_figure_frame.current_figure_dropdown_test.configure(state='disabled')
        
        
        self.left_frame.current_figure_frame.current_figure_dropdown.configure(values=self.current_figures)
        self.left_frame.current_figure_frame.current_figure_dropdown_test.configure(values=self.current_figures)
        
        print(self.left_frame.current_figure_frame.current_figure_dropdown.get())
        print(self.current_figures)
        
        if self.change_fig_options == True:
            print(self.left_frame.current_figure_frame.current_figure_dropdown.get())
            self.show_fig_options((self.left_frame.current_figure_frame.current_figure_dropdown.get()))
            
        self.run_tool(self.filename)
        
    def show_fig_options(self, fig):
        
        fig = fig.split("-", 1)[0]
        
        # clear the frame
        for widget in self.left_frame.main_tabview.graph_tab_frame.winfo_children():
            widget.pack_forget()
        
        match fig:
            case "plot":
                
                with open('fig_data.json', 'r') as file:
                    self.fig_data = json.load(file)
                
                # GRAPH TAB
                
                self.graph_tab = self.left_frame.main_tabview.graph_tab_frame
                
                self.graph_tab.x_axis_selector_frame = x_axis_selector_frame(parent = self.graph_tab, root = self, width = self.width, height = self.height)
                self.graph_tab.x_axis_selector_frame.pack(padx=(0, 10), pady=(10, 10), expand = True, fill = "x")
                self.graph_tab.x_axis_selector_frame.x_axis_selector_dropdown_test.configure(values = self.column_headers)
                
                #set the dropdown to the value in the json file
                try:
                    self.graph_tab.x_axis_selector_frame.x_axis_selector_dropdown.set(self.fig_data[self.left_frame.current_figure_frame.current_figure_dropdown.get()]['x_axis'])
                except KeyError:
                    self.graph_tab.x_axis_selector_frame.x_axis_selector_dropdown.set("No data")
                
                
                self.graph_tab.y_axis_selector_frame = y_axis_selector_frame(parent = self.graph_tab, root = self, width = self.width, height = self.height)
                self.graph_tab.y_axis_selector_frame.pack(padx=(0, 10), pady=(0, 10), expand = True, fill = "x")
                self.graph_tab.y_axis_selector_frame.y_axis_selector_dropdown_test.configure(values = self.column_headers)
                
                #set the dropdown to the value in the json file
                try:
                    self.graph_tab.y_axis_selector_frame.y_axis_selector_dropdown.set(self.fig_data[self.left_frame.current_figure_frame.current_figure_dropdown.get()]['y_axis'])
                except KeyError:
                    self.graph_tab.y_axis_selector_frame.y_axis_selector_dropdown.set("No data")
                
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
    
    root = root()
    root.protocol("WM_DELETE_WINDOW", root.exit_app_callback)
    root.mainloop()