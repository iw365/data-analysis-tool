import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
from CTkMenuBar import *

import json
import datetime as dt

from settings import active_light_theme, active_dark_theme, active_theme_type
from launcher_functions import *

#open settings file
with open('current-settings.json', 'r') as file:
    settings_data = json.load(file)
    
#set width and height from settings file
width = int(settings_data["window_width"])
height = int(settings_data["window_height"])

#close settings file
file.close()

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
    def __init__(self, parent, width, height):
        self.width = (width/5)*4
        self.height = (height/4)*3
        super().__init__(master=parent,
                        width=self.width,
                        height=self.height,
                        text_color=accent1,
                        fg_color=[secondary, primary],
                        border_width=3,
                        border_color=accent1,
                        segmented_button_fg_color=accent1,
                        segmented_button_selected_color=accent2,
                        segmented_button_unselected_color=secondary,
                        segmented_button_selected_hover_color=accent2,
                        segmented_button_unselected_hover_color=accent2)

        # create tabs
        self.add("tab 1")
        self.add("tab 2")

        # add widgets on tabs
        self.label = ctk.CTkLabel(master=self.tab("tab 1"))
        self.label.grid(row=0, column=0, padx=20, pady=10)

class left_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width/4
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color=primary, corner_radius = 0)
        self.pack_propagate(False)
        self.root=root
        self.initialise_ui()

    def initialise_ui(self):
        self.main_tabview = main_tabview(parent = self, width = self.width, height = self.height)
        self.main_tabview.pack(pady=(20, 0), padx=20)
        
        self.main_button = ctk.CTkButton(master=self,
                                            width = (self.width/5)*4,
                                            height = self.height / 4,
                                            fg_color=(accent1, primary),
                                            hover_color=(accent1_light, primary_dark),
                                            border_width=3,
                                            border_color=(accent1, spare),
                                            corner_radius=10,
                                            text='upload file',
                                            font=("Roboto", 40),
                                            command = self.root.main_button_callback)
        self.main_button.pack(pady=(20, 20), padx=20)
        
        #self.main_button.bind('<Return>', self.root.main_button_callback)
        
        self.close_file_button = ctk.CTkButton(master=self,
                                            width = (self.width/5)*4,
                                            height = self.height / 15,
                                            fg_color=(accent1, primary),
                                            hover_color=(accent1_light, primary_dark),
                                            border_width=3,
                                            border_color=(accent1, spare),
                                            corner_radius=10,
                                            text='close file',
                                            font=("Roboto", 15),
                                            command = self.root.close_file) #need to add later

# class middle_frame(ctk.CTkFrame):
#     def __init__(self, parent, width, height):
#         self.width = width/2
#         self.height = height
#         super().__init__(parent, width=self.width, height=self.height, fg_color='#00FF00', corner_radius = 0)
#         self.initialise_ui()

#     def initialise_ui(self):
#         self.middle_sub_frame_top = middle_sub_frame_top(parent = self, width = self.width, height = self.height)
#         self.middle_sub_frame_middle = middle_sub_frame_middle(parent = self, width = self.width, height = self.height)
#         self.middle_sub_frame_bottom = middle_sub_frame_bottom(parent = self, width = self.width, height = self.height)
        
#         self.middle_sub_frame_top.grid(row=0, column=0, padx=0, pady=0)
#         self.middle_sub_frame_middle.grid(row=1, column=0, padx=0, pady=0)
#         self.middle_sub_frame_bottom.grid(row=2, column=0, padx=0, pady=0)

class top_right_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = (height/4)*3
        super().__init__(parent, width=self.width, height=self.height, fg_color='#FF0000', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass

class bottom_options_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = ((width)/3)*2
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#00FF00', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass
    
class terminal_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = (width)/3
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#0000FF', corner_radius = 0)
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.terminal_header_frame = ctk.CTkFrame(master=self, width=(self.width), height=(self.height/6)*1, border_width=3, border_color=(accent1, accent1), fg_color=(spare, primary), corner_radius=10)
        self.terminal_header_frame.pack(padx=(10, 10), pady=(10, 0))
        self.terminal_header_frame.pack_propagate(False)
        self.terminal_header_label = ctk.CTkLabel(master=self.terminal_header_frame, text="Terminal", text_color=(accent1, '#FFFFFF'), font=("Arial", 20))
        self.terminal_header_label.pack(padx=10, pady=10)
        
        print(self.height)
        print((self.height/6)*1)
        self.terminal = ctk.CTkTextbox(master=self,
                                    width=(self.width),
                                    height=((self.height/6)*4)-20,
                                    state="normal",
                                    text_color=(accent1, '#FFFFFF'),
                                    scrollbar_button_color=(accent1, spare),
                                    fg_color=(spare, primary),
                                    border_color=(accent1, accent1),
                                    border_width=3,
                                    corner_radius=10)
        # self.terminal.pack(padx=30, pady=(0,0), fill = "both", expand = False)
        self.terminal.pack(padx=(10, 10), pady=(0,0), expand = False)
        self.terminal.configure(state = "normal")
        self.terminal.insert("end", f"> APP START\n\n----------\n\n")
        self.terminal.configure(state = "disabled")
        
        self.terminal_clear_button = ctk.CTkButton(master=self,
                                    width = (self.width),
                                    height = (self.height/6)*1,
                                    fg_color=(accent1, primary),
                                    hover_color=(accent1_light, primary_dark),
                                    border_width=3,
                                    border_color=(accent1, accent1),
                                    corner_radius=10,
                                    text='clear terminal',
                                    font=("Arial", 15),
                                    command = self.clear_terminal)
        self.terminal_clear_button.pack(padx=(10, 10), pady=(0, 10))
        
    def clear_terminal(self):
        self.terminal.configure(state = "normal")
        self.terminal.delete("0.0", "end")
        self.terminal.configure(state = "disabled")
        root.terminal_callback("TERMINAL CLEARED", "hard")
        #self.terminal.insert("0.0", "TERMINAL CLEARED\n\n----------\n\n")


class bottom_right_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = (height/4)
        super().__init__(parent, width=self.width, height=self.height, fg_color='#FF00FF', corner_radius = 0)
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        
        self.bottom_options_frame = bottom_options_frame(parent = self, width = self.width, height = self.height)
        self.bottom_options_frame.grid(row=0, column=0, padx=0, pady=0)
        
        self.terminal_frame = terminal_frame(parent = self, width = self.width, height = self.height)
        self.terminal_frame.grid(row=0, column=1, padx=0, pady=0)

class right_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = (width/4)*3
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color=secondary, corner_radius = 0)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.initialise_ui()

    def initialise_ui(self):
        
        self.top_right_frame = top_right_frame(parent = self, width = self.width, height = self.height)
        self.top_right_frame.pack(padx=0, pady=(0, 0))
        self.bottom_right_frame = bottom_right_frame(parent = self, width = self.width, height = self.height)
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
        self.geometry(f'{self.width}x{self.height}')
        #self.iconbitmap('classes/empty.ico') #change icon
        #ctk.set_appearance_mode("Light")

        self.initialise_ui()

    def initialise_ui(self):
        
        self.left_frame = left_frame(parent = self, root = self, width = self.width, height = self.height)
        #self.middle_frame = middle_frame(parent = self,  width = self.width, height = self.height)
        self.right_frame = right_frame(parent = self, width = self.width, height = self.height)

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
        
        if self.file_active == True:
            
            self.left_frame.main_button.configure(text="run tool", height = self.height/5/5*3) #this is so scuffed
            self.left_frame.close_file_button.configure(text="clear", height = self.height/5/5*2)
            print("tool active")
            self.left_frame.main_button.pack_configure(pady=(20, 0))
            self.left_frame.close_file_button.pack(pady=(0, 20), padx=20)
        elif self.file_active == False:
            self.left_frame.close_file_button.pack_forget()
            self.left_frame.main_button.configure(text="upload file", height = self.height/4) #this is so scuffed
            print("no tool active")
            self.left_frame.main_button.pack_configure(pady=(20, 20))
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
    accent1_light = lighten_color(accent1)
    accent2_light = lighten_color(accent2)
    print(primary, secondary, accent1, accent2, spare)

    primary_dark = darken_color(primary)
    accent1_dark = darken_color(accent1)
    accent2_dark = darken_color(accent2)
    
    root = root()
    root.protocol("WM_DELETE_WINDOW", root.exit_app_callback)
    root.mainloop()