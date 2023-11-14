import tkinter as tk
import customtkinter as ctk

from settings import *

class middle_sub_frame_top(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=960, height=180, fg_color='#FFFF00', corner_radius = 0)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass

class middle_sub_frame_middle(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=960, height=720, fg_color='#00FF00', corner_radius = 0)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass

class middle_sub_frame_bottom(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=960, height=180, fg_color='#00FFFF', corner_radius = 0)
        self.initialise_ui()

    def initialise_ui(self):
        pass

class left_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=480, height=height, fg_color='#FF0000', corner_radius = 0)
        self.initialise_ui()

    def initialise_ui(self):
        pass

class middle_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=960, height=height, fg_color='#00FF00', corner_radius = 0)
        self.initialise_ui()

    def initialise_ui(self):
        self.middle_sub_frame_top = middle_sub_frame_top(parent=self)
        self.middle_sub_frame_middle = middle_sub_frame_middle(parent=self)
        self.middle_sub_frame_bottom = middle_sub_frame_bottom(parent=self)
        
        self.middle_sub_frame_top.grid(row=0, column=0, padx=0, pady=0)
        self.middle_sub_frame_middle.grid(row=1, column=0, padx=0, pady=0)
        self.middle_sub_frame_bottom.grid(row=2, column=0, padx=0, pady=0)

class right_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=480, height=height, fg_color='#0000FF', corner_radius = 0)
        self.initialise_ui()

    def initialise_ui(self):
        pass

class root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analysis Tool")
        self.geometry(f'{width}x{height}')
        #self.iconbitmap('classes/empty.ico') #change icon
        ctk.set_appearance_mode("Light")

        self.initialise_ui()

    def initialise_ui(self):

        self.left_frame = left_frame(parent=self)
        self.middle_frame = middle_frame(parent=self)
        self.right_frame = right_frame(parent=self)

        self.left_frame.grid(row=0, column=0, padx=0, pady=0)
        self.middle_frame.grid(row=0, column=1, padx=0, pady=0)
        self.right_frame.grid(row=0, column=2, padx=0, pady=0)

if __name__ == "__main__":
    root = root()
    root.mainloop()