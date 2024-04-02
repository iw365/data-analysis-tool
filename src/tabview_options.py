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
        
class show_best_fit_line_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width / 2
        self.height = height / 30
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        corner_radius = 10)
        self.root = root
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.show_best_fit_line_var = ctk.StringVar(value="on")
        
        self.initialise_ui()
    
    def initialise_ui(self):
            
            self.show_best_fit_line_checkbox = ctk.CTkCheckBox(master=self,
                                                            text='Show Best Fit Line',
                                                            variable=self.show_best_fit_line_var,
                                                            onvalue="on",
                                                            offvalue="off",
                                                            fg_color=(accent1, primary),
                                                            hover_color=(accent1_light, accent2),
                                                            corner_radius=10,
                                                            font=("Roboto", 12))
            self.show_best_fit_line_checkbox.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')

# DATA OPTIONS #

class main_calculation_button_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width / 2
        self.height = height / 30
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        corner_radius = 10)
        self.root = root
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.initialise_ui()
        
    def initialise_ui(self):
            
            self.main_calculation_button = ctk.CTkButton(master=self,
                                                            text='Calculate',
                                                            fg_color=(accent1, primary),
                                                            hover_color=(accent1_light, accent2),
                                                            corner_radius=10,
                                                            font=("Roboto", 12),
                                                            command=lambda: self.root.calculate())
            self.main_calculation_button.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')

class calculation_results_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width / 2
        self.height = height / 4
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        corner_radius = 10)
        self.root = root
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.initialise_ui()
        
    def initialise_ui(self):
            
            self.calculation_results_textbox = ctk.CTkTextbox(master=self,
                                                            width=self.width/3,
                                                            height=self.height,
                                                            fg_color=(accent1, primary),
                                                            corner_radius=10,
                                                            font=("Roboto", 12),
                                                            state = 'normal',)
            self.calculation_results_textbox.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')
            
            self.calculation_results_textbox.delete(0.0, "end")
            self.calculation_results_textbox.insert(0.0, "Results will be displayed here")
            self.calculation_results_textbox.configure(state='disabled')
            
class z_score_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width / 2
        self.height = height / 30
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        corner_radius = 10)
        self.root = root
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.initialise_ui()
        
    def initialise_ui(self):
            
            self.z_score_entry = ctk.CTkEntry(master=self,
                                                placeholder_text='Area to test Z-score',
                                                fg_color=(accent1, primary),
                                                corner_radius=10,
                                                            font=("Roboto", 12))
            self.z_score_entry.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')
            
            self.z_score_button = ctk.CTkButton(master=self,
                                                text='Calculate Z-Score',
                                                fg_color=(accent1, primary),
                                                hover_color=(accent1_light, accent2),
                                                corner_radius=10,
                                                font=("Roboto", 12),
                                                command=lambda: self.root.calculate_z_score())
            self.z_score_button.grid(row=0, column=1, padx=(0, 5), pady=(0, 0), sticky='ew')
            
class z_score_results_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width / 2
        self.height = height / 4
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        corner_radius = 10)
        self.root = root
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.initialise_ui()
        
    def initialise_ui(self):
            
            self.z_score_results_textbox = ctk.CTkTextbox(master=self,
                                                            width=self.width/3,
                                                            height=self.height,
                                                            fg_color=(accent1, primary),
                                                            corner_radius=10,
                                                            font=("Roboto", 12),
                                                            state = 'normal',)
            self.z_score_results_textbox.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')
            
            self.z_score_results_textbox.delete(0.0, "end")
            self.z_score_results_textbox.insert(0.0, "Z-Score will be displayed here")
            self.z_score_results_textbox.configure(state='disabled')

# APPEARANCE OPTIONS #

class show_grid_frame(ctk.CTkFrame):
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
        
        self.show_grid_var = ctk.StringVar(value="on")
        
        self.initialise_ui()
    
    def initialise_ui(self):
        
        self.show_grid_checkbox = ctk.CTkCheckBox(master=self,
                                                        text='Show Grid',
                                                        text_color=(accent1, '#FFFFFF'),
                                                        variable=self.show_grid_var,
                                                        onvalue="on",
                                                        offvalue="off",
                                                        fg_color=(accent1, primary),
                                                        hover_color=(accent1_light, accent2),
                                                        corner_radius=10,
                                                        font=("Roboto", 12))
        self.show_grid_checkbox.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')

class show_legend_frame(ctk.CTkFrame):
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
        
        self.show_legend_var = ctk.StringVar(value="on")
        
        self.initialise_ui()
    
    def initialise_ui(self):
        
        self.show_legend_checkbox = ctk.CTkCheckBox(master=self,
                                                        text='Show Legend',
                                                        text_color=(accent1, '#FFFFFF'),
                                                        variable=self.show_legend_var,
                                                        onvalue="on",
                                                        offvalue="off",
                                                        fg_color=(accent1, primary),
                                                        hover_color=(accent1_light, accent2),
                                                        corner_radius=10,
                                                        font=("Roboto", 12))
        self.show_legend_checkbox.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky='ew')
class spine_selector_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height): #take in arguements when it is packed in other file
        self.width = width / 2
        self.height = height / 5
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        fg_color=secondary,
                        #fg_color="#FF0000",
                        corner_radius = 10)
        self.root = root
        
        self.north_spine = 0
        self.east_spine = 0
        self.south_spine = 1
        self.west_spine = 1
        
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.initialise_ui()
    
    def initialise_ui(self):
        
        self.spine_selector_label = ctk.CTkLabel(master=self,
                                                fg_color=(primary, secondary),
                                                text='Select which Spines to Display: ',
                                                text_color=(accent1, '#FFFFFF'),
                                                font=("Roboto", 12),
                                                anchor='center')
                                                #command=lambda: self.root.update_json_callback('x_axis', self))
        self.spine_selector_label.grid(row=1, column=0, padx=(0, 20), pady=(0, 0), sticky='ew')
        
        self.spine_selector_button_1 = ctk.CTkButton(master=self,
                                                        width=14,
                                                        height=50,
                                                        text=None,
                                                        #text='y',
                                                        font=("Arial", 12),
                                                        text_color=(accent1, '#FFFFFF'),
                                                        #variable=self.show_grid_var,
                                                        #onvalue="on",
                                                        #offvalue="off",
                                                        bg_color=('#ffff00'),
                                                        fg_color=(accent1, primary),
                                                        border_color=(accent1, primary),
                                                        border_width=0,
                                                        hover_color=(accent1_light, secondary_light),
                                                        corner_radius=0,
                                                        anchor='s',
                                                        command=lambda: self.reconfigure_spine_selector(1))
        self.spine_selector_button_1.grid(row = 1, column = 1, padx=(0, 0), pady=(0, 0), sticky='nesw')
        
        self.spine_selector_button_2 = ctk.CTkButton(master=self,
                                                        width=100,
                                                        height=14,
                                                        text=None,
                                                        #variable=self.show_grid_var,
                                                        #onvalue="on",
                                                        #offvalue="off",
                                                        bg_color=('#ffff00'),
                                                        fg_color=(accent1_light, secondary_light),
                                                        border_color=(accent1, primary),
                                                        border_width=0,
                                                        hover_color=(accent1, primary),
                                                        corner_radius=0,
                                                        command=lambda: self.reconfigure_spine_selector(2))
        self.spine_selector_button_2.grid(row = 0, column = 2, padx=(0, 0), pady=(0, 0), sticky='nesw')
        
        self.spine_selector_button_3 = ctk.CTkButton(master=self,
                                                        width=14,
                                                        height=50,
                                                        text=None,
                                                        #variable=self.show_grid_var,
                                                        #onvalue="on",
                                                        #offvalue="off",
                                                        bg_color=('#ffff00'),
                                                        fg_color=(accent1_light, secondary_light),
                                                        border_color=(accent1, primary),
                                                        border_width=0,
                                                        hover_color=(accent1, primary),
                                                        corner_radius=0,
                                                        command=lambda: self.reconfigure_spine_selector(3))
        self.spine_selector_button_3.grid(row = 1, column = 3, padx=(0, 0), pady=(0, 0), sticky='nesw')
        
        self.spine_selector_button_4 = ctk.CTkButton(master=self,
                                                        width=100,
                                                        height=14,
                                                        text=None,
                                                        #text='x',
                                                        font=("Arial", 12),
                                                        text_color=(accent1, '#FFFFFF'),
                                                        #variable=self.show_grid_var,
                                                        #onvalue="on",
                                                        #offvalue="off",
                                                        bg_color=('#ffff00'),
                                                        fg_color=(accent1, primary),
                                                        border_color=(accent1, primary),
                                                        border_width=0,
                                                        hover_color=(accent1_light, secondary_light),
                                                        corner_radius=0,
                                                        anchor='w',
                                                        command=lambda: self.reconfigure_spine_selector(4))
        self.spine_selector_button_4.grid(row = 2, column = 2, padx=(0, 0), pady=(0, 0), sticky='nesw')

        
    def reconfigure_spine_selector(self, button_num):
        self.spine_to_configure = 'spine_selector_button_'+str(button_num)
        print(self.spine_to_configure)
        if button_num == 1:
            if self.west_spine == 1:
                self.spine_selector_button_1.configure(fg_color=secondary_light, hover_color=primary)
                self.west_spine = 0
            else:
                self.spine_selector_button_1.configure(fg_color=primary, hover_color=secondary_light)
                self.west_spine = 1
        elif button_num == 2:
            if self.north_spine == 1:
                self.spine_selector_button_2.configure(fg_color=secondary_light, hover_color=primary)
                self.north_spine = 0
            else:
                self.spine_selector_button_2.configure(fg_color=primary, hover_color=secondary_light)
                self.north_spine = 1
        elif button_num == 3:
            if self.east_spine == 1:
                self.spine_selector_button_3.configure(fg_color=secondary_light, hover_color=primary)
                self.east_spine = 0
            else:
                self.spine_selector_button_3.configure(fg_color=primary, hover_color=secondary_light)
                self.east_spine = 1
        elif button_num == 4:
            if self.south_spine == 1:
                self.spine_selector_button_4.configure(fg_color=secondary_light, hover_color=primary)
                self.south_spine = 0
            else:
                self.spine_selector_button_4.configure(fg_color=primary, hover_color=secondary_light)
                self.south_spine = 1
        
        print(self.north_spine, self.east_spine, self.south_spine, self.west_spine)
        #self.spine_selector_checkbox_2.grid(row = 0, column = 1, padx=(0, 5), pady=(0, 0), sticky='ew')