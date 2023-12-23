import customtkinter
#import tkinterDnD
import json
from settings import active_light_theme, active_dark_theme, active_theme_type

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

# Read the JSON file
with open('themes.json', 'r') as file:
    themes_data = json.load(file)
    
match active_theme_type:
    case 'light':
        theme = themes_data["light"][f"{active_light_theme}"]
        customtkinter.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
    case 'dark':
        theme = themes_data["dark"][f"{active_dark_theme}"]
        customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"

primary = theme['primary']
secondary = theme['secondary']
accent1 = theme['accent1']
accent2 = theme['accent2']
spare = theme['spare']

primary_light = lighten_color(primary)
accent1_light = lighten_color(accent1)
accent2_light = lighten_color(accent2)

primary_dark = darken_color(primary)
accent1_dark = darken_color(accent1)
accent2_dark = darken_color(accent2)

#customtkinter.set_ctk_parent_class(tkinterDnD.Tk)

#customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x780")
app.title("CustomTkinter simple_example.py")

#print(type(app), isinstance(app, tkinterDnD.Tk))

def button_callback():
    print("Button click", combobox_1.get())

def slider_callback(value):
    progressbar_1.set(value)

background = customtkinter.CTkFrame(master=app, fg_color=primary)
background.pack(pady=0, padx=0, fill="both", expand=True)

frame_1 = customtkinter.CTkFrame(master=background, fg_color=secondary)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT)
label_1.pack(pady=10, padx=10)

progressbar_1 = customtkinter.CTkProgressBar(master=frame_1, progress_color=(accent1, accent2), fg_color=(spare, primary))
progressbar_1.pack(pady=10, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, fg_color=(accent1, primary), hover_color=(accent1_light, primary_dark))
button_1.pack(pady=10, padx=10)

slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=1, button_color=(accent1, primary), fg_color=spare, progress_color=accent2, button_hover_color=(accent1_light, primary_dark))
slider_1.pack(pady=10, padx=10)
slider_1.set(0.5)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry", border_color=(accent1, primary), fg_color=secondary)
entry_1.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."],
                                            fg_color=(accent1, primary),
                                            button_color=(accent1, primary),
                                            button_hover_color=(accent1_light, accent2),
                                            dropdown_fg_color=(accent1, primary),
                                            dropdown_hover_color=(accent1_light, accent2), 
                                            dropdown_text_color="#FFFFFF")
optionmenu_1.pack(pady=10, padx=10)
optionmenu_1.set("CTkOptionMenu")

combobox_1 = customtkinter.CTkComboBox(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."],
                                            fg_color=(secondary, primary),
                                            border_color=accent1,
                                            button_color=accent2,
                                            button_hover_color=(accent2_light, accent2_dark),
                                            dropdown_fg_color=(accent1, primary),
                                            dropdown_hover_color=(accent1_light, accent2),
                                            dropdown_text_color="#FFFFFF")

combobox_1.pack(pady=10, padx=10)
combobox_1.set("CTkComboBox")

checkbox_1 = customtkinter.CTkCheckBox(master=frame_1, border_color=accent1, fg_color=accent2, hover_color=accent1)
checkbox_1.pack(pady=10, padx=10)

radiobutton_var = customtkinter.IntVar(value=1)

radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1, fg_color=accent2, hover_color=accent2, border_color=(accent1, primary))
radiobutton_1.pack(pady=10, padx=10)

radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2, fg_color=accent2, hover_color=accent2, border_color=(accent1, primary))
radiobutton_2.pack(pady=10, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1, fg_color=spare, button_color=(accent1, primary), button_hover_color=(accent1_light, primary_dark), progress_color=accent2)
switch_1.pack(pady=10, padx=10)

text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=70, state="normal", text_color=(accent1, '#FFFFFF'), scrollbar_button_color=(accent1, spare), fg_color=(spare, primary), border_color=(accent1, accent1), border_width=3, corner_radius=10)
text_1.pack(pady=10, padx=10)
text_1.insert("0.0", "CTkTextbox\n\n\n\n\n\n\n\n")

# segmented_button_1 = customtkinter.CTkSegmentedButton(master=frame_1, values=["CTkSegmentedButton", "Value 2"])
# segmented_button_1.pack(pady=10, padx=10)

tabview_1 = customtkinter.CTkTabview(master=frame_1,
                                            width=300,
                                            text_color=accent1,
                                            fg_color=(secondary, primary),
                                            border_width=3,
                                            border_color=accent1,
                                            segmented_button_fg_color=accent1,
                                            segmented_button_selected_color=accent2,
                                            segmented_button_unselected_color=secondary,
                                            segmented_button_selected_hover_color=accent2,
                                            segmented_button_unselected_hover_color=accent2)
tabview_1.pack(pady=10, padx=10)
tabview_1.add("CTkTabview")
tabview_1.add("Tab 2")
tabview_1.add("Tab 3")
tabview_1.add("Tab 4")

app.mainloop()