import tkinter as tk
import customtkinter as ctk
from PIL import Image
import subprocess
import platform
import os

from settings import *

class option_holder(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, width = self.width, height = self.height, fg_color = '#3F3F3F', border_width = 5, border_color = '#FFFFFF', corner_radius = 20)
        self.grid_propagate(True)
        self.initialise_ui()
        
    def initialise_ui(self):
        app_launch_button = ctk.CTkButton(master=self, width = self.width - 80, height = self.height / 5, text='launch app', command = self.launch_app)
        app_launch_button.grid(row=0, column=0, padx=20, pady=20)
        
        open_root_button = ctk.CTkButton(master=self, width = self.width - 80, height = self.height / 5, text='open root folder', command = self.open_root_folder)
        open_root_button.grid(row=1, column=0, padx=20, pady=20)
        
    def launch_app(self):
        root.destroy()
        os.system('python3 main.py')
        
    def open_root_folder(self):
        current_dir = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        system = platform.system()
        
        match system:
            case 'Windows':
                subprocess.Popen(f'explorer "{parent_dir}"')
            case 'Linux':
                subprocess.Popen(['xdg-open', parent_dir])
            case 'Darwin':
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
        self.option_holder.pack(padx = 0, pady = 20, ipadx = 0, ipady = 50)

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
        super().__init__(parent, width = self.width, height = self.height, fg_color = '#FF0000', border_width = 5, border_color = '#FFFFFF', corner_radius = 20)
        self.grid_propagate(True)
        self.initialise_ui()
        
    def initialise_ui(self):
        app_launch_button = ctk.CTkButton(master=self, width = self.width - 80, height = self.height / 5, text='launch app', command = self.launch_app)
        app_launch_button.grid(row=0, column=0, padx=20, pady=20)
        
    def launch_app(self):
        root.destroy()
        os.system('python3 main.py')

class right_sub_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#FFFF00', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        self.settings_menu_holder = settings_menu_holder(parent = self, width = self.width, height = self.height)
        self.settings_menu_holder.pack(padx = 0, pady = 20)

class right_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = (width/5)*2
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#656464', corner_radius = 0)
        self.pack_propagate(False)#pack false
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

if __name__ == "__main__":
    root = root(launcher_width, launcher_height)
    root.mainloop()