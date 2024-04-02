
import os
import sys
import platform
import csv
import time

import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
from CTkMenuBar import *
from CTkToolTip import *
from CTkTable import *
from PIL import Image
try:
    import pywinstyles
except ImportError:
    pass

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from matplotlib import gridspec as gs

import tensorflow as tf
import numpy as np

from sklearn.ensemble import IsolationForest 
import mplcursors

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

class left_frame_tabview(ctk.CTkTabview):
    def __init__(self, parent, root, width, height):
        self.width = width
        self.height = height
        super().__init__(parent, width=self.width, height=self.height, corner_radius = 10)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.root = root
        
        self.add("Data")
        self.add("Train")
        self.add("Test")
        
        self.initialise_ui()

    def initialise_ui(self):
        
        # DATA #
        
        self.upload_file_button = ctk.CTkButton(self.tab("Data"),
                                                text="Open File",
                                                command=self.root.upload_file_callback)
        self.upload_file_button.pack(pady=10)
        
        self.plot_type_option = ctk.CTkOptionMenu(self.tab("Data"),
                                                    values=['Scatter', 'Line'])
        
        self.input_option = ctk.CTkOptionMenu(self.tab("Data"), 
                                                values=['Select Input'])
        #self.input_option.pack(pady=10)
        
        self.output_option = ctk.CTkOptionMenu(self.tab("Data"), 
                                                values=['Select Output'])
        #self.output_option.pack(pady=10)
        
        self.start_button = ctk.CTkButton(self.tab("Data"), text="start", command=self.root.start)
        #self.start_button.pack(pady=10)
        
        # TRAIN #
        
        self.load_model_button = ctk.CTkButton(self.tab("Train"),
                                                text="Load Model")
        #self.load_model_button.pack(pady=10)
        
        self.epoch_entry = ctk.CTkEntry(self.tab("Train"),
                                        placeholder_text="Epochs")
        #self.epoch_entry.pack(pady=10)
        
        self.extra_layers_entry = ctk.CTkEntry(self.tab("Train"),
                                                placeholder_text="Extra Layers")
        #self.extra_layers_entry.pack(pady=10)
        
        self.train_button = ctk.CTkButton(self.tab("Train"),
                                        text="Train on Current Data - Overwrites Previous Model",
                                        command=self.root.tf_train)
        #self.train_button.pack(pady=10)
        
        self.detect_anomalies_button = ctk.CTkButton(self.tab("Train"),
                                                    text="Detect Anomalies - sklearn (using own data)",
                                                    command = lambda: self.root.sk_train(1))
        #self.detect_anomalies_button.pack(pady=10)
        
        self.detect_anomalies_button_random = ctk.CTkButton(self.tab("Train"),
                                                    text="Detect Anomalies - sklearn (using random points)",
                                                    command = lambda: self.root.sk_train(0))
        #self.detect_anomalies_button.pack(pady=10)
        
        # TEST #
        
        self.results_label = ctk.CTkLabel(self.tab("Test"),
                                            text="Results")
        #self.results_label.pack(pady=10)
        
        self.results_textbox = ctk.CTkTextbox(self.tab("Test"),
                                                state = 'disabled',
                                                font=('consolas', 10))
        #self.results_textbox.pack(pady=10)
        
        self.random_seed_entry = ctk.CTkEntry(self.tab("Train"),
                                                placeholder_text="Set Randomness Seed - Default = 42")
        #self.random_seed_entry.pack(pady=10)
        
        self.random_is_time_var = ctk.StringVar(value="on")
        self.set_randomness_to_time_switch = ctk.CTkSwitch(self.tab("Train"),
                                                            variable=self.random_is_time_var,
                                                            onvalue="on",
                                                            offvalue="off",
                                                            text="Set Randomness Seed to Current Time")
        #self.set_randomness_to_time_switch.pack(pady=10)
        

class left_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width/8*3
        self.height = height
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        #fg_color='#00FF00',
                        corner_radius = 0)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.root = root
        
        self.initialise_ui()

    def initialise_ui(self):
        
        self.left_frame_tabview = left_frame_tabview(parent = self, root = self.root, width = self.width, height = self.height)
        self.left_frame_tabview.pack(padx = 20, pady=20, fill = 'both', expand = True)

class right_panel(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width/8*5
        self.height = height
        super().__init__(parent,
                        width=self.width,
                        height=self.height,
                        #fg_color='#0000FF',
                        corner_radius = 10)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.root = root
        self.initialise_ui()

    def initialise_ui(self):
        pass

class right_frame(ctk.CTkFrame):
    def __init__(self, parent, root, width, height):
        self.width = width/8*5
        self.height = height
        super().__init__(parent,
                        width=self.width,
                        height=self.height, 
                        #fg_color='#FF0000',
                        corner_radius = 0)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.root = root
        self.initialise_ui()

    def initialise_ui(self):
        
        # right_panel = ctk.CTkFrame(self, width=self.width, height=self.height, corner_radius = 10)
        # right_panel.pack(padx=(0, 20), pady=20, fill='both', expand=True)
        
        self.right_panel = right_panel(parent = self, root = self.root, width = self.width, height = self.height)
        self.right_panel.pack(padx=20, pady=20, fill='both', expand=True)

class root(tk.Tk):
    def __init__(self):
        self.width = 1280
        self.height = 720
        super().__init__()
        self.title("Data Analysis Tool - ML")
        self.resizable(False, False) # disable resizing
        # if platform.system() == "Windows":
        #     #pywinstyles.apply_style(self, "mica")
        #     pywinstyles.change_header_color(self, primary)
        
        self.geometry(f'{self.width}x{self.height}+50+50')
        
        #self.iconbitmap('classes/empty.ico') #change icon
        ctk.set_appearance_mode("dark")


        self.initialise_ui()
        #self.check()
    
    def initialise_ui(self):
        
        # self.background = ctk.CTkFrame(self, width=self.width, height=self.height, corner_radius = 0)
        # self.background.place(x=0.5, y=0.5)
        
        self.left_frame = left_frame(parent = self, root = self, width = self.width, height = self.height)
        #self.middle_frame = middle_frame(parent = self,  width = self.width, height = self.height)
        self.right_frame = right_frame(parent = self, root = self, width = self.width, height = self.height)

        self.left_frame.grid(row=0, column=0, padx=(0, 0), pady=0)
        #self.middle_frame.grid(row=0, column=1, padx=0, pady=0)
        self.right_frame.grid(row=0, column=2, padx=0, pady=0)
        
    # def check(self):
    #     self.after(2000, self.check)
    #     print("Checking")
    #     pass
        
    def upload_file_callback(self):
        
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File", filetypes=((("CSV files", "*.csv"), ("All files", "*.*"))))
        print(self.filename)
        
        if not self.filename:
            print("No file selected.")
        elif not os.path.isfile(self.filename):
            print("File not found.")
        elif not self.filename.endswith('.csv'):
            print("File is not a CSV file.")
        else:
            self.set_up_lists(self.filename)
        
        self.left_frame.left_frame_tabview.plot_type_option.pack(pady=10)
        self.left_frame.left_frame_tabview.input_option.pack(pady=10)
        self.left_frame.left_frame_tabview.output_option.pack(pady=10)
        
        self.left_frame.left_frame_tabview.start_button.pack(pady=10)
            
    def set_up_lists(self, filename):
        
        self.raw_data = []
        
        with open(filename, 'r', encoding='utf-8-sig') as csvfile:
            self.csvreader = csv.reader(csvfile)
            # self.headers = next(self.csvreader)
            # self.x_label = self.headers[0]
            # self.y_label = self.headers[1]
            for row in self.csvreader:
                # self.raw_x_data.append(row[0])
                # self.raw_y_data.append(row[1])
                self.raw_data.append(row)
                
        self.column_data = list(map(list, zip(*self.raw_data)))
        
        print(f'\n\nRAW DATA: {self.raw_data}\n\n')
        print(f'\n\nCOLUMN DATA: {self.column_data}\n\n')
        
        self.left_frame.left_frame_tabview.input_option.configure(values = self.raw_data[0])
        self.left_frame.left_frame_tabview.output_option.configure(values = self.raw_data[0])
        
        self.column_data_copy = self.column_data.copy()
        self.raw_data_copy = self.raw_data.copy()
        
        
    def start(self):
        #search copied list for the header selected in dropdown
        #if found, remove the header from the copied list
        
        self.input_index = self.raw_data[0].index(self.left_frame.left_frame_tabview.input_option.get())
        self.output_index = self.raw_data[0].index(self.left_frame.left_frame_tabview.output_option.get())
        print(f'\n\nINDEX 1: {self.raw_data[0].index(self.left_frame.left_frame_tabview.input_option.get())}\n\n')
        print(f'\n\nINDEX 2: {self.raw_data[0].index(self.left_frame.left_frame_tabview.output_option.get())}\n\n')
        
        self.x_data = self.column_data_copy[int(self.input_index)][:]
        self.y_data = self.column_data_copy[int(self.output_index)][:]

        self.x_data_header = self.x_data.pop(0)
        self.y_data_header = self.y_data.pop(0)
        
        self.raw_data_copy.pop(0)
        print(self.raw_data_copy)
        #convert to numpy array
        self.raw_data_copy = np.array(self.raw_data_copy)
        #convert to int
        self.raw_data_copy = self.raw_data_copy.astype(int)
        
        print(f'\n\nX DATA: {self.x_data}\n\n')
        print(f'\n\nY DATA: {self.y_data}\n\n')
        
        self.x_data = list(map(int, self.x_data))
        self.y_data = list(map(int, self.y_data))
        
        if self.left_frame.left_frame_tabview.plot_type_option.get() == 'Scatter':
            pass
        elif self.left_frame.left_frame_tabview.plot_type_option.get() == 'Line':
            self.draw_graph('Line')
        
        self.left_frame.left_frame_tabview.set("Train")
        self.show_options(self.left_frame.left_frame_tabview.plot_type_option.get())
        
    def show_options(self, plot_type):
        match plot_type:
            case 'Scatter':
                self.left_frame.left_frame_tabview.detect_anomalies_button.pack(pady=10)
                self.left_frame.left_frame_tabview.detect_anomalies_button_random.pack(pady=10)
                self.left_frame.left_frame_tabview.random_seed_entry.pack(pady=10)
                self.left_frame.left_frame_tabview.set_randomness_to_time_switch.pack(pady=10)
            case 'Line':
                self.left_frame.left_frame_tabview.load_model_button.pack(pady=10)
                self.left_frame.left_frame_tabview.epoch_entry.pack(pady=10)
                self.left_frame.left_frame_tabview.extra_layers_entry.pack(pady=10)
                self.left_frame.left_frame_tabview.train_button.pack(pady=10)
        
    def draw_graph(self, plot_type):
        
        print(f'\n\nplot_type: {plot_type}\n\n')
        
        match plot_type:
            case 'Line':
                
                try:
                    self.canvas.get_tk_widget().destroy()
                except:
                    pass
                self.fig = plt.Figure(figsize=(5, 5), dpi=100)
                
                self.ax = self.fig.add_subplot(111)
                self.ax.plot(self.x_data,
                            self.y_data)
                
                self.ax.set_xlabel(self.x_data_header)
                self.ax.set_ylabel(self.y_data_header)
                
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame.right_panel)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(padx=20, pady=20, expand = True, fill = "both")
            case 'Scatter':
                
                self.sk_train()
                
            case _:
                print("Invalid plot type")
                
    def tf_train(self):
        self.input_train = np.array(self.x_data, dtype=np.float32)
        self.output_train = np.array(self.y_data, dtype=np.float32)
        
        #prepare model
        # self.model = tf.keras.Sequential()
        # #self.model.add(tf.keras.layers.Dense(units=1, input_shape=[1])) #USE THIS IN TESTING
        # self.model.add(tf.keras.layers.Dense(units=64, input_shape=[1], activation='relu'))
        # self.model.add(tf.keras.layers.Dense(units=64, activation='relu'))
        # try:
        #     for i in range(int(self.left_frame.left_frame_tabview.extra_layers_entry.get())):
        #         self.model.add(tf.keras.layers.Dense(units=64, activation='relu'))
        # except:
        #     pass
        # self.model.add(tf.keras.layers.Dense(units=1)) # HASH OUT ALL THIS IN TESTING
        
        #make multi-layered model with keras and sigmoid
        
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=[1]),
            tf.keras.layers.Dense(1)
        ])
        
        for i in range(int(self.left_frame.left_frame_tabview.extra_layers_entry.get())):
            self.model.add(tf.keras.layers.Dense(64, activation='sigmoid'))
        
        
        self.model.compile(optimizer='sgd', loss='mean_squared_error')
        
        #train!
        self.model.fit(self.input_train, self.output_train, epochs=int(self.left_frame.left_frame_tabview.epoch_entry.get()))
        
        print(f'\n\nModel Trained!\nTrained input: {self.input_train}\nTrained Output: {self.output_train}\n\n')
        
        self.test_input = np.array(self.input_train, dtype=np.float32)
        self.predictions = self.model.predict(self.test_input)
        print('\n\nPredictions:\n\n')
        for i in range(len(self.test_input)):
            print(f'Input: {self.test_input[i]} | Output: {self.predictions[i][0]}')
        
        self.ax.plot(self.test_input,
                                self.predictions,
                                color = 'red')
        self.canvas.draw()
        
    def sk_train(self, mode):
        
        if self.left_frame.left_frame_tabview.random_is_time_var.get() == 'on':
            print(time.time())
            np.random.seed(int(time.time()))
        elif self.left_frame.left_frame_tabview.random_is_time_var.get() == 'off':
            np.random.seed(self.left_frame.left_frame_tabview.random_seed_entry.get())
        n_samples = 100 
        n_features = 2 

        if mode == 0:
            normal_data = 0.3 * np.random.randn(n_samples, n_features)
            print(normal_data)

            #generate some anomalies uniformly distributed between -6 and 6
            anomalies = np.random.uniform(low=-6, high=6, size=(20, n_features))
            print(anomalies)

            #combine the normal data and anomalies to create the final dataset
            data = np.vstack([normal_data, anomalies])
            print(data)
        elif mode == 1:
            data = self.raw_data_copy
            print(data)

        #train the isolation forest model
        model = IsolationForest(contamination=0.1)
        #contamination defines the expected proportion of anomalies
        model.fit(data)

        # predict anomalies using the trained model
        anomaly_scores = model.decision_function(data)

        #normalize data
        min_score = min(anomaly_scores)
        max_score = max(anomaly_scores)
        normalized_scores = (anomaly_scores - min_score) / (max_score - min_score)
        print(normalized_scores)
        #confidence_scores = round((normalized_scores) * 100)

        # convert numpy array to list
        confidence_scores = (normalized_scores.copy()).tolist()
        for i, score in enumerate(confidence_scores):
            confidence_scores[i] = round((score) * 100, 0)
            
        #change to test tab
        self.left_frame.left_frame_tabview.set("Test")
        
        self.left_frame.left_frame_tabview.results_label.pack(pady = 10)
        self.left_frame.left_frame_tabview.results_textbox.pack(pady = 10, expand = True, fill = 'both')
        
        self.left_frame.left_frame_tabview.results_textbox.configure(state = 'normal')
        self.left_frame.left_frame_tabview.results_textbox.delete(0.0, 'end')
        
        rounded_scores = [round(score, 2) for score in anomaly_scores]
        if mode == 1:
            for i, score in enumerate(normalized_scores):
                if score >= 0.50:
                    print(f"{Fore.GREEN}Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% | Coords = ({self.x_data[i]}, {self.y_data[i]})\n")
                    self.left_frame.left_frame_tabview.results_textbox.insert('end', f"Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% | Coords = ({self.x_data[i]}, {self.y_data[i]})\n")
                elif score < 0.50 and score >= 0.25:
                    print(f"{Fore.YELLOW}Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% - POSSIBLE ERROR | Coords = ({self.x_data[i]}, {self.y_data[i]})\n")
                    self.left_frame.left_frame_tabview.results_textbox.insert('end', f"Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% - POSSIBLE ERROR | Coords = ({self.x_data[i]}, {self.y_data[i]})\n")
                elif score < 0.25:
                    print(f"{Fore.RED}Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% - LIKELY ERROR | Coords = ({self.x_data[i]}, {self.y_data[i]})\n")
                    self.left_frame.left_frame_tabview.results_textbox.insert('end', f"Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% - LIKELY ERROR | Coords = ({self.x_data[i]}, {self.y_data[i]})\n")
        else:
            for i, score in enumerate(normalized_scores):
                if score >= 0.50:
                    print(f"{Fore.GREEN}Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}%\n")
                    self.left_frame.left_frame_tabview.results_textbox.insert('end', f"Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}%\n")
                elif score < 0.50 and score >= 0.25:
                    print(f"{Fore.YELLOW}Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% - POSSIBLE ERROR \n")
                    self.left_frame.left_frame_tabview.results_textbox.insert('end', f"Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% - POSSIBLE ERROR \n")
                elif score < 0.25:
                    print(f"{Fore.RED}Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% - LIKELY ERROR \n")
                    self.left_frame.left_frame_tabview.results_textbox.insert('end', f"Data point {i+1}: Anomaly Score = {score:.2f} | Consistency = {round(confidence_scores[i], 3)}% - LIKELY ERROR \n")
        
        self.left_frame.left_frame_tabview.results_textbox.configure(state = 'disabled')

        #create a scatter plot
        self.fig = plt.Figure(figsize=(10, 6))  # Set the figure size

        self.scatter = self.fig.add_subplot(111).scatter(data[:, 0], data[:, 1], c=normalized_scores, cmap='viridis')  # Scatter plot with colors based on predictions

        # Set plot title and axis labels
        self.fig.suptitle('Isolation Forest Anomaly Detection')
        # self.fig.set_xlabel('Feature 1')
        # self.fig.set_ylabel('Feature 2')

        # add hover labels to the scatter plot
        def label_formatter(sel):
            i = sel.target.index
            score = confidence_scores[i]
            label_text = f"Data point {i+1}: Consistency = {score:.0f}%"
            sel.annotation.set(text = label_text, backgroundcolor='white', fontsize = 10, font = 'consolas')

            return label_text

        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(label_formatter(sel)))

        # Add a color legend to the plot
        self.fig.colorbar(self.scatter, label='Anomaly Score - Lower is more anomalous')

        # Create a canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame.right_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=20, pady=20, expand=True, fill="both")
        
if __name__ == "__main__":
    
    root = root()
    root.mainloop()