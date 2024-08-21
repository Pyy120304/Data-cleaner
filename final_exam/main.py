
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
import pandas as pd 
import numpy as np
from data_cleaner import * 
from UI_tkinter import * 

class DataCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Cleaner")
        self.root.geometry("1000x800")  
        self.create_widgets()
        self.data = None

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"Selected file: {file_path}")
            try:
                self.data = pd.read_csv(file_path)  
                print("Data loaded successfully!")
                self.clear_widgets()
                self.display_data()  
            except Exception as e:
                print(f"Error loading file: {e}")
    def save_file(self):
        if self.data is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if file_path:
                try:
                    self.data.to_csv(file_path, index=False) 
                    print(f"File saved to: {file_path}")
                except Exception as e:
                    print(f"Error saving file: {e}")
        else:
            print("No data to save.")

    def display_data(self):
        if self.data is not None:
            self.open_home(self.data)

    def clear_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_widgets(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        # File menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.upload_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Home", command=lambda:self.open_home(self.data))
        file_menu.add_command(label="Exit", command=self.root.destroy)
        # Edit menu
        edit_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Drop Duplicates", command=lambda: self.open_drop_ui(self.data))  
        edit_menu.add_command(label="Handle Missing Data", command=lambda: self.open_missing_ui(self.data))  
        edit_menu.add_command(label="Normalize Data", command=lambda: self.open_adjust_ui(self.data))  
        # Transform menu
        transform_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Transform", menu=transform_menu)
        transform_menu.add_command(label="Change Data Type", command=lambda: self.open_type_ui(self.data))  
        transform_menu.add_command(label="Merge Column", command=lambda: self.open_merge_ui(self.data))  
        transform_menu.add_command(label="Split Column", command=lambda: self.open_split_ui(self.data))  
        # View menu
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Entire Dataset", command=lambda: self.open_entire_ui(self.data))
        view_menu.add_command(label="Show column", command=lambda: self.open_showcolumn_ui(self.data))  
        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Guidebook", command=lambda: self.open_guidebook())

        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        # Main label
        self.title_label = tk.Label(self.main_frame, text="DATA CLEANER", font=("Arial", 78, "bold"))
        self.title_label.pack(pady=(150,10))

        # Load icon
        icon_path = ".\\final_exam\\free-folder-icon-1449-thumb.png"  
        self.icon_image = Image.open(icon_path)
        self.icon_image = self.icon_image.resize((100, 100), Image.LANCZOS)
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)

        # Subtitle label with icon
        self.subtitle_label = tk.Label(self.main_frame, text="UPLOAD NEW FILE TO CLEAN", font=("Arial", 20, "italic"))
        self.subtitle_label.pack(pady=(110, 0))

        # Create a frame to hold the icon and label
        self.icon_frame = tk.Frame(self.main_frame)
        self.icon_frame.pack(pady=20)

        # Icon label
        self.icon_label = tk.Label(self.icon_frame, image=self.icon_photo)
        self.icon_label.pack(pady=10)
        # Upload button with label
        self.upload_button = tk.Button(self.icon_frame, text="Upload File", bg="#47676D", fg="white", 
                                       font=("Arial", 14), compound=tk.LEFT, command=self.upload_file)
        self.upload_button.pack(side=tk.LEFT, padx=10)




    def open_guidebook(self):
        mess = """
1. Getting Started
    Open Data Cleaner: Double-click the Data Cleaner application icon to launch the program.
2. Main Menu
    Open File: Click "Open File" to select and load a data file (CSV, Excel, etc.) into the Data Cleaner interface.
    Save File: Click "Save File" to save the cleaned data to a new file.
    Home: Click "Home" to return to the main menu.
    Exit: Click "Exit" to close Data Cleaner.
3. Data Cleaning Features
    Handle Missing Data: Select this feature to manage missing data values. You can choose to:
        - Delete rows with missing data: Removes entire rows containing missing values.
        - Replace missing data: Replace missing values with a specified value or calculate based on other data.
        - Fill missing data: Fill missing values with mean, median, or other statistical measures.
    Normalize Data: Click "Normalize Data" to scale data values within a specific range. This helps to ensure consistent data scales for analysis.
    Drop Duplicate: Select "Drop Duplicate" to remove duplicate rows from your data.
    View Entire: Click "View Entire" to display the entire dataset in the application window.
    View Column: Click "View Column" to display data from a specific column.
    Change Datatype: Select "Change Datatype" to modify the data type of a column (e.g., from text to numeric).
    Merge Column: Click "Merge Column" to combine data from multiple columns into a single column.
    Split Column: Select "Split Column" to divide a column's data into multiple columns.
4. Using the Features
    Data Display: The Data Cleaner interface displays your data in a tabular format.
    Selection: Use your mouse to select the rows and/or columns you want to modify.
    Feature Options: Once you select a feature, a menu will appear with options specific to the feature.
    Apply Changes: Click the button to execute the selected action on your data.
5. Saving Your Work
    Save as: Click "Save File" to save your cleaned data to a new file. You can choose a file format (CSV, Excel, etc.) from the options provided.
"""
        messagebox.showinfo("Guidebook", mess)
    
    def update_data(self, new_data):
        self.data = new_data


    def open_type_ui(self, data):
        self.clear_widgets()
        type_app = TypeApp(self.main_frame, data, self.update_data)
    def open_drop_ui(self, data):
        self.clear_widgets()
        drop_app = DropApp(self.main_frame, data, self.update_data)
    def open_adjust_ui(self, data):
        self.clear_widgets()
        adjust_app = AdjustApp(self.main_frame, data, self.update_data)
        # adjust_app.display_data()
    def open_entire_ui(self, data):
        self.clear_widgets()
        entire_app = EntireApp(self.main_frame, data, self.update_data)
    def open_merge_ui(self, data):
        self.clear_widgets()
        merge_app = MergeApp(self.main_frame, data, self.update_data)
    def open_split_ui(self, data):
        self.clear_widgets()
        split_app = SplitApp(self.main_frame, data, self.update_data)
    def open_missing_ui(self, data):
        self.clear_widgets()
        missing_app = MissingApp(self.main_frame, data, self.update_data)
    def open_home(self, data):
        self.clear_widgets()
        home = Home(self.main_frame, data, self.update_data)
    def open_showcolumn_ui(self, data):
        self.clear_widgets()
        show = ShowColumnApp(self.main_frame, data, self.update_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = DataCleanerApp(root)
    root.mainloop()
    print(app.data.columns)