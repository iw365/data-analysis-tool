import tkinter as tk
import customtkinter as ctk
import json

from settings import active_light_theme, active_dark_theme, active_theme_type, width, height


class middle_sub_frame_top(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height/6
        super().__init__(parent, width=self.width, height=self.height, fg_color='#FFFF00', corner_radius = 0)
        self.grid_propagate(False)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass

class middle_sub_frame_middle(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = (height/6)*4
        super().__init__(parent, width=self.width, height=self.height, fg_color=primary, corner_radius = 0)
        self.initialise_ui()
        
    def initialise_ui(self):
        pass

class middle_sub_frame_bottom(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height/6
        super().__init__(parent, width=self.width, height=self.height, fg_color='#00FFFF', corner_radius = 0)
        self.initialise_ui()

    def initialise_ui(self):
        pass

class main_tabview(ctk.CTkTabview):
    def __init__(self, parent, width, height):
        self.width = (width/5)*4
        self.height = (height/4)*3
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        text_color=accent1,
                        fg_color=(secondary, primary),
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
    def __init__(self, parent, width, height):
        self.width = width/4
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color=secondary, corner_radius = 0)
        self.pack_propagate(False)
        self.initialise_ui()

    def initialise_ui(self):
        self.main_tabview = main_tabview(parent = self, width = self.width, height = self.height)
        self.main_tabview.pack(pady=20, padx=20)
        
        upload_file_button = ctk.CTkButton(master=self, width = (self.width/5)*4, height = self.height / 5, text='upload file', command = self.upload_file)
        upload_file_button.pack(pady=20, padx=20)
        
    def upload_file(self):
        pass

class middle_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width/2
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color='#00FF00', corner_radius = 0)
        self.initialise_ui()

    def initialise_ui(self):
        self.middle_sub_frame_top = middle_sub_frame_top(parent = self, width = self.width, height = self.height)
        self.middle_sub_frame_middle = middle_sub_frame_middle(parent = self, width = self.width, height = self.height)
        self.middle_sub_frame_bottom = middle_sub_frame_bottom(parent = self, width = self.width, height = self.height)
        
        self.middle_sub_frame_top.grid(row=0, column=0, padx=0, pady=0)
        self.middle_sub_frame_middle.grid(row=1, column=0, padx=0, pady=0)
        self.middle_sub_frame_bottom.grid(row=2, column=0, padx=0, pady=0)

class right_frame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        self.width = width/4
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, fg_color=secondary, corner_radius = 0)
        self.initialise_ui()

    def initialise_ui(self):
        pass

class exit_dialogue_window(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('640x360')
        self.initialise_ui()

class root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analysis Tool")
        self.geometry(f'{width}x{height}')
        #self.iconbitmap('classes/empty.ico') #change icon
        ctk.set_appearance_mode("Light")

        self.initialise_ui()

    def initialise_ui(self):

        self.left_frame = left_frame(parent = self, width = width, height = height)
        self.middle_frame = middle_frame(parent = self,  width = width, height = height)
        self.right_frame = right_frame(parent = self, width = width, height = height)

        self.left_frame.grid(row=0, column=0, padx=0, pady=0)
        self.middle_frame.grid(row=0, column=1, padx=0, pady=0)
        self.right_frame.grid(row=0, column=2, padx=0, pady=0)
        
        self.toplevel_window = None
        
    def exit_app_callback(self):
        root.destroy()
        # if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
        #     self.toplevel_window = exit_dialogue_window(self)  # create window if its None or destroyed
        # else:
        #     self.toplevel_window.focus()

if __name__ == "__main__":
    
    with open('themes.json', 'r') as file:
        themes_data = json.load(file)
    
    match active_theme_type:
        case 'light':
            theme = themes_data["light"][f"{active_light_theme}"]
            ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
        case 'dark':
            theme = themes_data["dark"][f"{active_dark_theme}"]
            ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"

    primary = theme['primary']
    secondary = theme['secondary']
    accent1 = theme['accent1']
    accent2 = theme['accent2']
    spare = theme['spare']
    
    root = root()
    root.protocol("WM_DELETE_WINDOW", root.exit_app_callback)
    root.mainloop()