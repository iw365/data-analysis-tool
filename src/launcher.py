import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os

from settings import *

class left_sub_frame_top(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height/4
        super().__init__(parent, width=self.width, height=self.height, fg_color='#0000FF', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass
        # logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), dark_image=Image.open("assets/logo.png"), size=(self.width, self.height))
        # image_label = ctk.CTkLabel(master = self, image=logo, text="")
        
class left_sub_frame_bottom(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = (height/4)*3
        super().__init__(parent, width=self.width, height=self.height, fg_color='#FFFF00', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        app_launch_button = ctk.CTkButton(master=self, text='launch app', command = self.launch_app)
        app_launch_button.grid(row=0, column=0, padx=0, pady=0)
        
    def launch_app(self):
        root.destroy()
        
        os.system('python3 main.py')

class left_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = (width/5)*3
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#FF0000', corner_radius = 0)
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

class right_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = (width/5)*2
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#00FF00', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()

    def initialise_ui(self):
        pass

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