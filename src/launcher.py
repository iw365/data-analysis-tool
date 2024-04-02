import tkinter as tk
import customtkinter as ctk
from CTkToolTip import *

from PIL import Image
import subprocess
import platform
import os
import json

from settings import *
from launcher_functions import *

class option_holder(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, width = self.width, height = self.height, fg_color = '#3F3F3F', border_width = 5, border_color = '#FFFFFF', corner_radius = 20)
        self.grid_propagate(True)
        self.initialise_ui()
        
    def initialise_ui(self):
        app_launch_button = ctk.CTkButton(master=self, width = self.width - 80, height = self.height / 5, text='launch app', command = self.launch_app_call)
        app_launch_button.grid(row=0, column=0, padx=20, pady=20)
        
        ml_app_launch_button = ctk.CTkButton(master=self, width = self.width - 80, height = self.height / 5, text='launch machine-learning-app', command = self.launch_ml_app_call)
        ml_app_launch_button.grid(row=1, column=0, padx=20, pady=(0,20))
        
        open_root_button = ctk.CTkButton(master=self, width = self.width - 80, height = self.height / 5, text='open root folder', command = self.open_root_folder)
        open_root_button.grid(row=2, column=0, padx=20, pady=(0,20))
        
    def launch_app_call(self):
        self.get_settings()
        
        #read data
        with open('current-settings.json', 'r') as file:
            settings_data = json.load(file)
        
        if settings_data["keep_launcher_open_on_app_launch"] == "False": #!BUH
            root.destroy()
            
        launch_app_reg('main.py')
        
    def launch_ml_app_call(self):
        self.get_settings()
        
        #read data
        with open('current-settings.json', 'r') as file:
            settings_data = json.load(file)
        
        if settings_data["keep_launcher_open_on_app_launch"] == "False":
            root.destroy()
            
        launch_app_reg('ML-app.py')
        
    def get_settings(self):
        print('getting settings', launcher_permittivity_enabled.get())
        
        #read data
        with open('current-settings.json', 'r') as file:
            settings_data = json.load(file)
        
        settings_data["keep_launcher_open_on_app_launch"] = str(launcher_permittivity_enabled.get())
        #save settings
        with open("current-settings.json", "w") as file:
            json.dump(settings_data, file)
        
    def open_root_folder(self):
        current_dir = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        
        match system:
            case 'Windows':
                subprocess.Popen(f'explorer "{parent_dir}"')
            case 'Linux':
                subprocess.Popen(['xdg-open', parent_dir])
            case 'Darwin': #NOT FULLY SUPPORTED
                subprocess.Popen(['open', parent_dir])
            case _:
                print("Unsupported operating system") #!ERROR LOG NEEDED

class left_sub_frame_top(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height/4
        super().__init__(parent, width=self.width, height=self.height, fg_color='#3F3F3F', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), dark_image=Image.open("assets/logo.png"), size=(self.width, self.height))
        image_label = ctk.CTkLabel(master = self, image=logo, text="", corner_radius=0)
        
        image_label.pack()

class left_sub_frame_bottom(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = (height/4)*3
        super().__init__(parent, width=self.width, height=self.height, fg_color='#3F3F3F', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        self.option_holder = option_holder(parent = self, width = self.width, height = self.height)
        self.option_holder.pack(padx = 0, pady = 20, ipadx = 0, ipady = 0)

class left_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = (width/5)*3
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#3F3F3F', corner_radius = 0)
        self.grid_propagate(False)
        #self.pack_propagate(False)
        
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.initialise_ui()

    def initialise_ui(self):
        self.left_sub_frame_top = left_sub_frame_top(parent = self, width = self.width, height = self.height)
        self.left_sub_frame_bottom = left_sub_frame_bottom(parent = self, width = self.width, height = self.height)
        
        self.left_sub_frame_top.grid(row = 0, column = 0, padx = 0, pady = 0)
        self.left_sub_frame_bottom.grid(row = 1, column = 0, padx = 0, pady = 0)

class settings_menu_holder(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, width = self.width, height = self.height, fg_color = '#3F3F3F', border_width = 5, border_color = '#FFFFFF', corner_radius = 20)
        self.grid_propagate(True)
        self.initialise_ui()
        
    def initialise_ui(self):
        with open('current-settings.json', 'r') as file:
            settings_data = json.load(file)
            
        #self.grid_rowconfigure(2, weight=1)
        
        global launcher_permittivity_enabled
        launcher_permittivity_enabled=ctk.BooleanVar(value=(settings_data["keep_launcher_open_on_app_launch"]))
        self.launcher_permittivity_switch=ctk.CTkSwitch(master=self, text='Keep Launcher Open', variable=launcher_permittivity_enabled, onvalue=True, offvalue=False, command=self.get_settings)
        self.launcher_permittivity_switch.grid(row=0, column=0, padx=50, pady=(20, 0))
        
        global resolution
        self._width = settings_data["window_width"]
        self._height = settings_data["window_height"]
        resolution = ctk.StringVar(value=f"{self._width}x{self._height}")
        
        print(self.winfo_screenwidth(), self.winfo_screenheight())
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.detected_resolution = f"Detected Display: {self.screen_width}x{self.screen_height}"
        
        self.resolution_options = ctk.CTkOptionMenu(master=self, values=[self.detected_resolution, "1280x720", "1600x900", "1920x1080", "2560x1440", "3840x2160"], variable=resolution, command=self.get_settings)
        self.resolution_options.grid(row=1, column=0, padx=50, pady=(20, 0))
        
        self.resolution_warning_label = ctk.CTkLabel(master=self, text="*All resolutions other than \n1600x900 are experimental", text_color="#AD0000")
        if str(resolution.get()) != "1600x900":
            self.resolution_warning_label.grid(row=2, column=0, padx=50, pady=(20, 0))
        
        global show_date
        show_date = ctk.StringVar(value=(settings_data["show_date_in_terminal"]))
        show_date_checkbox = ctk.CTkCheckBox(master=self, text="Show Date in Terminal", variable=show_date, onvalue="True", offvalue="False", command=self.get_settings)
        show_date_checkbox.grid(row=3, column=0, padx=50, pady=(20, 20))
        
    def get_settings(self, *args):
        #read data
        with open('current-settings.json', 'r') as file:
            settings_data = json.load(file)
        
        #show a warning if the resolution is not 1600x900
        if str(resolution.get()) != "1600x900":
            self.resolution_warning_label.grid(row=2, column=0, padx=50, pady=(20, 0))
        else:
            self.resolution_warning_label.grid_forget()
        
        if str(resolution.get()) == self.detected_resolution:
            resolution.set(f"{self.screen_width}x{self.screen_height}")
        
        settings_data["keep_launcher_open_on_app_launch"] = str(launcher_permittivity_enabled.get())
        settings_data["window_width"] = str(resolution.get().split("x")[0])
        settings_data["window_height"] = str(resolution.get().split("x")[1])
        settings_data["show_date_in_terminal"] = str(show_date.get())
        
        #save settings
        with open("current-settings.json", "w") as file:
            json.dump(settings_data, file)

class right_sub_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#656464', corner_radius = 0)
        self.grid_propagate(False)
        self.pack_propagate(True)
        self.initialise_ui()
        
    def initialise_ui(self):
        self.settings_menu_holder = settings_menu_holder(parent = self, width = self.width, height = self.height)
        self.settings_menu_holder.pack(padx = 0, pady = 20)

class right_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = (width/5)*2
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#656464', corner_radius = 0)
        self.pack_propagate(False)
        self.initialise_ui()

    def initialise_ui(self):
        self.right_sub_frame = right_sub_frame(parent = self, width = self.width, height = self.height)
        self.right_sub_frame.pack(padx = 0, pady = 20)

class root(tk.Tk):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        super().__init__()
        self.title("Data Analysis Tool Launcher")
        self.geometry(f'{launcher_width}x{launcher_height}')
        #self.iconbitmap('classes/empty.ico') #change icon
        ctk.set_appearance_mode("Dark")

        self.initialise_ui()

    def initialise_ui(self):
        
        self.left_frame = left_frame(parent=self, width = self.width, height = self.height)
        self.right_frame = right_frame(parent=self, width = self.width, height = self.height)
        
        self.left_frame.grid(row=0, column=0, padx=0, pady=0)
        self.right_frame.grid(row=0, column=1, padx=0, pady=0)

system = platform.system()

if __name__ == "__main__":
    root = root(launcher_width, launcher_height)
    root.mainloop()