


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
from PIL import Image

from modules.CTkXYFrame import ctk_xyframe

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import json
import datetime as dt

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
        self.add("Graph") # THIS WILL BE FOR CHANGING THE GRAPH TYPE
        self.add("Data") #THIS WILL BE FOR EXTRACTING DATA FROM FILE
        self.add("Appearance") # THIS WILL BE FOR CUSTOMIZING THE APPEARANCE OF THE GRAPH
        self.add("Modifiy") #THIS WILL BE FOR MODIFYING THE DATA 

        # add widgets on tabs
        self.label = ctk.CTkLabel(master=self.tab("Graph"))
        self.label.pack(padx=10, pady=10)

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

# class y_frame(ctk.CTkScrollableFrame):
#     def __init__(self, parent, width, height):
#         self.width = width
#         self.height = height
#         super().__init__(parent,
#                         width=self.width,
#                         height=self.height,
#                         fg_color=secondary,
#                         corner_radius = 10,
#                         scrollbar_button_color=accent1,
#                         scrollbar_button_hover_color=accent1_dark,)
#         self.pack_propagate(False)
#         #self.grid_propagate(False)
#         self.initialise_ui()
        
#     def initialise_ui(self):
#         pass

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
        self.frame.pack(padx=10, pady=10)
        
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.plot.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

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
        print(self.width, self.height)
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
        
        print(self.width, self.height)
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
                                    font=("Consolas", 12),
                                    text_color=(accent1, '#FFFFFF'),
                                    scrollbar_button_color=accent1,
                                    scrollbar_button_hover_color=accent1_dark,
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
            #run_tool(root.filename)
            
    def run_tool(self, filename):
        print("guh")
        print(filename)
        
    def close_file(self):
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
            # self.left_frame.main_tabview.close_file_button.configure(text="clear", height = self.height/5/5*2)
            # print("tool active")
            # self.left_frame.main_tabview.main_button.pack_configure(pady=(0, 50))
            # self.left_frame.main_tabview.close_file_button.pack(pady=(0, 10), padx=20)
        elif self.file_active == False:
            
            self.bottom.main_buttons_frame.close_file_button.grid_forget()
            self.bottom.main_buttons_frame.main_button.configure(text="upload file")

            # self.left_frame.main_tabview.close_file_button.pack_forget()
            # self.left_frame.main_tabview.main_button.configure(text="upload file", height = self.height/4) 
            # print("no tool active")
            # self.left_frame.main_tabview.main_button.pack_configure(pady=(0, 10))
            #reverse of first case
            
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
    
    match active_theme_type:
        case 'light':
            theme = themes_data["light"][f"{active_light_theme}"]
            ctk.set_appearance_mode("light") # Modes: "System" (standard), "Dark", "Light"
        case 'dark':
            theme = themes_data["dark"][f"{active_dark_theme}"]
            print('debug i hate this')
            ctk.set_appearance_mode("dark") # Modes: "System" (standard), "Dark", "Light"

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