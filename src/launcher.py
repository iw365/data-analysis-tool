import tkinter as tk
import customtkinter as ctk
import os

from settings import *

class left_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=600, height=600, fg_color='#FF0000', corner_radius = 0)
        self.grid_propagate(False)
        #self.pack_propagate(False)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.initialise_ui()

    def initialise_ui(self):
        app_launch_button = ctk.CTkButton(master=self, text='launch app', command = self.launch_app)
        app_launch_button.grid(row=0, column=0, padx=0, pady=0)
        
    def launch_app(self):
        root.destroy()
        os.system('python3 main.py')

class right_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=400, height=600, fg_color='#00FF00', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()

    def initialise_ui(self):
        pass

class root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analysis Tool Launcher")
        self.geometry('1000x600')
        #self.iconbitmap('classes/empty.ico') #change icon
        ctk.set_appearance_mode("Dark")

        self.initialise_ui()

    def initialise_ui(self):
        
        self.left_frame = left_frame(parent=self)
        self.right_frame = right_frame(parent=self)
        
        self.left_frame.grid(row=0, column=0, padx=0, pady=0)
        self.right_frame.grid(row=0, column=1, padx=0, pady=0)

if __name__ == "__main__":
    root = root()
    root.mainloop()