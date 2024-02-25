import tkinter as tk
import customtkinter as ctk
from modules.CTkScrollableDropdown import *

from settings import primary, secondary, accent1, accent2, spare, primary_light, secondary_light, accent1_light, accent2_light, primary_dark, secondary_dark, accent1_dark, accent2_dark

# GRAPH OPTIONS #
class x_axis_selector_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height): #take in arguements when it is packed in other file
        self.width = width / 2
        self.height = height / 30
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        #fg_color="#FF0000",
                        corner_radius = 10)
        self.root = root
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.initialise_ui()
    
    def initialise_ui(self):
        
        self.x_axis_selector_dropdown = ctk.CTkOptionMenu(master=self,
                                                        values=['test', 'test2'],
                                                        fg_color=(accent1, primary),
                                                        button_color=(accent1, primary),
                                                        button_hover_color=(accent1_light, accent2),
                                                        dropdown_fg_color=(accent1, primary),
                                                        dropdown_hover_color=(accent1_light, accent2), 
                                                        dropdown_text_color="#FFFFFF",
                                                        corner_radius=10,
                                                        font=("Arial", 14))
        self.x_axis_selector_dropdown.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')
        
        self.x_axis_selector_dropdown_test = CTkScrollableDropdown(self.x_axis_selector_dropdown,
                                                                    values=['test', 'test2'],
                                                                    fg_color=(primary, primary),
                                                                    hover_color=(secondary_dark, primary_light),
                                                                    #hover_color=('#ff0000'),
                                                                    frame_corner_radius=10,
                                                                    #frame_border_width=2,
                                                                    frame_border_color=(accent1, primary),
                                                                    button_color=(secondary, primary),
                                                                    scrollbar_button_color=(accent1, primary),
                                                                    #command = self.root.update_json_and_list,
                                                                    resize=True)
        
        self.x_axis_selector_label = ctk.CTkLabel(master=self,
                                                fg_color=(primary, secondary),
                                                text='  X-Axis Field',
                                                text_color=(accent1, '#FFFFFF'),
                                                font=("Roboto", 12),
                                                anchor='center')
                                                #command=lambda: self.root.update_json_callback('x_axis', self))
        self.x_axis_selector_label.grid(row=0, column=1, padx=(0, 5), pady=(0, 0), sticky='ew')
        
class y_axis_selector_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height): #take in arguements when it is packed in other file
        self.width = width / 2
        self.height = height / 30
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        #fg_color="#FF0000",
                        corner_radius = 10)
        self.root = root
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.initialise_ui()
    
    def initialise_ui(self):
        
        self.y_axis_selector_dropdown = ctk.CTkOptionMenu(master=self,
                                                        values=['test', 'test2'],
                                                        fg_color=(accent1, primary),
                                                        button_color=(accent1, primary),
                                                        button_hover_color=(accent1_light, accent2),
                                                        dropdown_fg_color=(accent1, primary),
                                                        dropdown_hover_color=(accent1_light, accent2), 
                                                        dropdown_text_color="#FFFFFF",
                                                        corner_radius=10,
                                                        font=("Arial", 14))
        self.y_axis_selector_dropdown.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')
        
        self.y_axis_selector_dropdown_test = CTkScrollableDropdown(self.y_axis_selector_dropdown,
                                                                    values=['test', 'test2'],
                                                                    fg_color=(primary, primary),
                                                                    hover_color=(secondary_dark, primary_light),
                                                                    #hover_color=('#ff0000'),
                                                                    frame_corner_radius=10,
                                                                    #frame_border_width=2,
                                                                    frame_border_color=(accent1, primary),
                                                                    button_color=(secondary, primary),
                                                                    scrollbar_button_color=(accent1, primary),
                                                                    resize=True)
        
        self.y_axis_selector_label = ctk.CTkLabel(master=self,
                                                fg_color=(primary, secondary),
                                                text='  Y-Axis Field',
                                                text_color=(accent1, '#FFFFFF'),
                                                font=("Roboto", 12),
                                                anchor='center')
                                                #command=lambda: self.root.update_json_callback('y_axis', self))
        self.y_axis_selector_label.grid(row=0, column=1, padx=(0, 5), pady=(0, 0), sticky='ew')