import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from data_cleaner import *

# tạo thêm 1 nút để lọc dữ liệu


class AdjustApp:
    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.data = data  # Nhận dữ liệu từ lớp chính
        self.update_callback = update_callback
        self.setupUi()
        self.display_data()  # Hiển thị dữ liệu sau khi thiết lập giao diện

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        self.title_label = tk.Label(self.frame, text="Normalization Tool", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0,30))
        self.instruction_label = tk.Label(self.frame, text="Press the button below to normalize data.", fg="#ba0000", font=("Helvetica", 12))
        self.instruction_label.place(x=220, y = 200)
        self.push_button = tk.Button(self.frame, text="Normalize", bg="#47676D", fg="white", font=("Arial", 12), compound=tk.LEFT, command=self.adjust_data1)
        self.push_button.pack(padx=(0,10), pady=(170, 20))
        self.combo_box = ttk.Combobox(self.frame, width=20, height=30)
        self.combo_box.place(x=360, y=140)
        self.combo_box['values'] = ("Min-Max", "Robust", "Z-score")
        self.combo_box.current(0)
        self.text_edit = tk.Text(self.frame, height=1, width=20)
        self.text_edit.place(x=360, y=90)
        self.clear_button = tk.Button(self.frame, text="Delete", width=7, height=1, bg="#47676D", fg="white", font=("Arial", 9), command=self.clear_text_box)
        self.clear_button.place(x=535, y=90) 
        self.label = ttk.Label(self.frame, text="Choose columns:")
        self.label.place(x=180, y=90, width=131, height=31)
        self.label_2 = ttk.Label(self.frame, text="Choose method:")
        self.label_2.place(x=180, y=140, width=131, height=31)
        font_style = ("Arial", 12, "italic underline")
        label = tk.Label(self.main_frame, text="Do you want to go back to the homepage? Click here", font=font_style, fg="#0085ba", cursor="hand2")
        label.place(x=10, y=730)
        label.bind("<Button-1>", lambda event: self.open_home(self.data))
        
    def clear_text_box(self):
        self.text_edit.delete("1.0", tk.END)

    def open_home(self,data):
        home = Home(self.main_frame, data)

    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80)  # Thiết lập độ rộng cho cột

            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

    def adjust_data1(self):
        try:
            if self.data.empty: # Kiểm tra nếu data rỗng
                messagebox.showinfo("Notification", "Please upload data to perform the operation!")
                return
    # Lấy giá trị từ text box và combo box
            columns_text = self.text_edit.get("1.0", tk.END).strip()
            columns = columns_text.split(",") if columns_text else []
            method = self.combo_box.get()
            # Điều chỉnh dữ liệu
            self.data = adjust_data(self.data, columns, method)
            self.update_callback(self.data)
            self.setupUi()
            self.display_data()
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while retrieving data: {}".format(str(e)))
        
    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        column_index = self.tree.identify_column(event.x)
        column_name = self.tree.heading(column_index)["text"]
        current_text = self.text_edit.get("1.0", tk.END).strip()
        if current_text:
            current_columns = current_text.split(",")
            if column_name not in current_columns:
                current_columns.append(column_name)
                self.text_edit.delete("1.0", tk.END)
                self.text_edit.insert(tk.END, ",".join(current_columns))
        else:
            self.text_edit.insert(tk.END, column_name)




class DropApp:
    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.setupUi()
        self.data = data 
        self.update_callback = update_callback
        self.display_data()

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        self.title_label = tk.Label(self.frame, text="Drop Duplicates Tool", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0,30))
        self.instruction_label = tk.Label(self.frame, text="Press the button below to drop duplicate entries", 
                                          fg="#ba0000", font=("Helvetica", 12))
        self.instruction_label.place(x=220, y = 100)
        self.push_button = tk.Button(self.frame, text="Drop duplicate", bg="#47676D", fg="white", 
                                     font=("Arial", 12), compound=tk.LEFT, command=self.drop_duplicates)
        self.push_button.pack(padx=(0,10),pady=(100,20))
        font_style = ("Arial", 12, "italic underline")
        label = tk.Label(self.main_frame, text="Do you want to go back to the homepage? Click here", 
                         font=font_style, fg="#0085ba", cursor="hand2")
        label.place(x=10, y=730)
        label.bind("<Button-1>", lambda event: self.open_home(self.data))

        
    def open_home(self,data):
        home = Home(self.main_frame, data)

    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80) 
            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)



    def drop_duplicates(self):
        try: 
            if  self.data.empty:  # Kiểm tra nếu data rỗng
                messagebox.showinfo("Notification", "Please upload data to perform the operation!")
                return
            self.data = drop_duplicates(self.data)
            self.clear_widgets()
            self.setupUi()
            self.display_data()
            self.update_callback(self.data)
            # messagebox.showinfo("Success", "Operation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while retrieving data: {}".format(str(e)))
        


class EntireApp:
    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.data = data
        self.update_callback = update_callback
        self.setupUi()
        self.display_data()

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.place(x=40, y=0, width=540, height=400)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        self.title_label = tk.Label(self.frame, text="Data Viewer", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0,30))
        self.instruction_label = tk.Label(self.frame, text="Press the button below to view info", fg="#ba0000", font=("Helvetica", 12))
        self.instruction_label.place(x=250, y =100)
        self.info_button = tk.Button(self.frame, text="Show Info",bg="#47676D", fg="white", font=("Arial", 12), compound=tk.LEFT, command=self.show_info)
        self.info_button.pack(padx=(0,10),pady=(100,20))
        # Create a new Treeview for displaying info
        self.info_tree = ttk.Treeview(self.data_frame, show="headings", height=5)
        self.info_tree.place(x=600, y=0, width=220, height=400)
        self.scrollbar_y = ttk.Scrollbar(self.info_tree, orient=tk.VERTICAL, command=self.info_tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.info_tree, orient=tk.HORIZONTAL, command=self.info_tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Configure info_treeview scroll command
        self.info_tree.configure(yscrollcommand=self.scrollbar_y.set,xscrollcommand=self.scrollbar_x.set)
        font_style = ("Arial", 12, "italic underline")
        label = tk.Label(self.main_frame, text="Do you want to go back to the homepage? Click here", font=font_style, fg="#0085ba", cursor="hand2")
        label.place(x=10, y=730)
        label.bind("<Button-1>", lambda event: self.open_home(self.data))

    def open_home(self,data):
        home = Home(self.main_frame, data)

    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80)

            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)
                
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
    def show_info(self):
        try:
            if  self.data.empty:  # Kiểm tra nếu data rỗng
                messagebox.showinfo("Notification", "Please upload data to perform the operation!")
                return
            # Clear current info_tree content
            
            self.info_tree.delete(*self.info_tree.get_children())  

            # Set columns for info_tree
            self.info_tree["columns"] = ("", "")
            self.info_tree.column("", width=60)
            self.info_tree.column("", width=100)

            # Insert information
            num_rows = self.data.shape[0]
            num_columns = self.data.shape[1]
            self.info_tree.insert("", "end", values=("Number of Rows", num_rows))
            self.info_tree.insert("", "end", values=("Number of Columns", num_columns))
            self.info_tree.insert("", "end", values=("", ""))  # Blank row for spacing
            self.info_tree.insert("", "end", values=("Columns and Data Types", ""))
            for col in self.data.columns:
                dtype = self.data[col].dtype
                self.info_tree.insert("", "end", values=(col, dtype))
            # messagebox.showinfo("Success", "Operation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while retrieving data: {}".format(str(e)))
        

class ShowColumnApp:
    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.data = data
        self.update_callback = update_callback
        self.setupUi()
        self.display_data()

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.place(x=40, y=0, width=540, height=400)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        self.title_label = tk.Label(self.frame, text="Data Viewer", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0,30))
        self.choose_label = tk.Label(self.frame, text="Choose column: ",  font=("Helvetica", 12))
        self.choose_label.place(x=230, y =100)
        self.text_edit = tk.Text(self.frame, height=1, width=20)
        self.text_edit.place(x=370, y=100)
        self.clear_button = tk.Button(self.frame, text="Delete", width=7, height=1, bg="#47676D", fg="white", font=("Arial", 9), command=self.clear_text_box)
        self.clear_button.place(x=560, y=100)
        self.instruction_label = tk.Label(self.frame, text="Press the button below to view info", fg="#ba0000", font=("Helvetica", 12))
        self.instruction_label.place(x=250, y =170)
        self.info_button = tk.Button(self.frame, text="Show Info",bg="#47676D", fg="white", font=("Arial", 12), compound=tk.LEFT, command=self.show_column)
        self.info_button.pack(padx=(0,10),pady=(160,20))
        # Create a new Treeview for displaying info
        self.info_tree = ttk.Treeview(self.data_frame, show="headings", height=5)
        self.info_tree.place(x=600, y=0, width=220, height=400)
        self.scrollbar_y = ttk.Scrollbar(self.info_tree, orient=tk.VERTICAL, command=self.info_tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.info_tree, orient=tk.HORIZONTAL, command=self.info_tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Configure info_treeview scroll command
        self.info_tree.configure(yscrollcommand=self.scrollbar_y.set,xscrollcommand=self.scrollbar_x.set)
        font_style = ("Arial", 12, "italic underline")
        label = tk.Label(self.main_frame, text="Do you want to go back to the homepage? Click here", font=font_style, fg="#0085ba", cursor="hand2")
        label.place(x=10, y=730)
        label.bind("<Button-1>", lambda event: self.open_home(self.data))

    
    def clear_text_box(self):
        self.text_edit.delete("1.0", tk.END)

    def open_home(self,data):
        home = Home(self.main_frame, data)

    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()


    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80)

            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)

    def show_column(self):
        try:
            if self.data.empty:
                messagebox.showinfo("Notification", "Please upload data to perform the operation!")
                return
            selected_column = self.text_edit.get("1.0", tk.END).strip()
            if not selected_column:
                messagebox.showinfo("Notification", "Please enter a column name to view its frequency distribution!")
                return
            # Clear current info_tree content
            self.info_tree.delete(*self.info_tree.get_children())
            # Calculate frequency distribution
            frequency_data = frequency_distribution(self.data, selected_column)
            # Set columns for info_tree
            self.info_tree["columns"] = list(frequency_data.columns)
            for column in frequency_data.columns:
                self.info_tree.heading(column, text=column)
                self.info_tree.column(column, width=100)  # Set column width
            # Insert frequency distribution data
            for _, row in frequency_data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.info_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while retrieving data: {str(e)}")

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        column_index = self.tree.identify_column(event.x)
        column_name = self.tree.heading(column_index)["text"]
        current_text = self.text_edit.get("1.0", tk.END).strip()
        if current_text:
            current_columns = current_text.split(",")
            if column_name not in current_columns:
                current_columns.append(column_name)
                self.text_edit.delete("1.0", tk.END)
                self.text_edit.insert(tk.END, ",".join(current_columns))
        else:
            self.text_edit.insert(tk.END, column_name)



class MergeApp:
    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.setupUi()
        self.data = data
        self.update_callback = update_callback
        self.display_data()

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        self.title_label = tk.Label(self.frame, text="Merge Columns Tool", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0,30))
        self.instruction_label = tk.Label(self.frame, text="Press the button below to merge columns", 
                                          fg="#ba0000", font=("Helvetica", 12))
        self.instruction_label.place(x=220, y = 200)
        self.push_button = tk.Button(self.frame, text="Merge column", bg="#47676D", fg="white",
                                      font=("Arial", 12), compound=tk.LEFT, command=self.merge_column)
        # self.push_button.pack(pady=(140,30))
        self.push_button.pack(padx=(0,10), pady=(170, 20))
        self.text_edit = tk.Text(self.frame, height=1, width=20)
        self.text_edit.place(x=360, y=90)
        self.clear_button = tk.Button(self.frame, text="Delete", width=7, height=1, bg="#47676D", 
                                      fg="white", font=("Arial", 9), command=self.clear_text_box)
        self.clear_button.place(x=535, y=90)
        self.text_edit_2 = tk.Text(self.frame, height=1, width=20)
        self.text_edit_2.place(x=360, y=140)
        self.label = ttk.Label(self.frame, text="Choose columns:")
        self.label.place(x=180, y=90)
        self.label_2 = ttk.Label(self.frame, text="Character:")
        self.label_2.place(x=180, y=140)
        font_style = ("Arial", 12, "italic underline")
        label = tk.Label(self.main_frame, text="Do you want to go back to the homepage? Click here",
                          font=font_style, fg="#0085ba", cursor="hand2")
        label.place(x=10, y=730)
        label.bind("<Button-1>", lambda event: self.open_home(self.data))

    def clear_text_box(self):
        self.text_edit.delete("1.0", tk.END)

    def open_home(self,data):
        home = Home(self.main_frame, data)



    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
    
    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80)  # Thiết lập độ rộng cho cột
            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
   
    def merge_column(self):
        try: 
            if self.data.empty:  # Kiểm tra nếu data rỗng
                messagebox.showinfo("Notification", "Please upload data to perform the operation!")
                return
            # Lấy giá trị từ text box 
            columns_text = self.text_edit.get("1.0", tk.END).strip()
            char_text = self.text_edit_2.get("1.0", tk.END).strip()
            columns = columns_text.split(",") if columns_text else []

            # Điều chỉnh dữ liệu
            self.data = merge_column(self.data, columns, char_text)
            self.update_callback(self.data)

            # Cập nhật giao diện hiển thị dữ liệu
            self.clear_widgets()
            self.setupUi()
            self.display_data()
            # messagebox.showinfo("Success", "Operation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while retrieving data: {}".format(str(e)))
        
    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        column_index = self.tree.identify_column(event.x)
        column_name = self.tree.heading(column_index)["text"]
        current_text = self.text_edit.get("1.0", tk.END).strip()
        if current_text:
            current_columns = current_text.split(",")
            if column_name not in current_columns:
                current_columns.append(column_name)
                self.text_edit.delete("1.0", tk.END)
                self.text_edit.insert(tk.END, ",".join(current_columns))
        else:
            self.text_edit.insert(tk.END, column_name)









class MissingApp:
    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.setupUi()
        self.data = data
        self.update_callback = update_callback
        self.display_data()

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        self.title_label = tk.Label(self.frame, text="Missing Data Handler", 
                                    font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0,30))
        self.instruction_label = tk.Label(self.frame, text="Press the button below to handle missing data", 
                                          fg="#ba0000", font=("Helvetica", 12))
        self.instruction_label.place(x=220, y = 100)
        self.push_button = tk.Button(self.frame, text="Handle missing data", bg="#47676D", fg="white", 
                                     font=("Arial", 12), compound=tk.LEFT, command=self.handle_missing_data)
        self.push_button.pack(padx=(0,10),pady=(100,20))
        font_style = ("Arial", 12, "italic underline")
        label = tk.Label(self.main_frame, text="Do you want to go back to the homepage? Click here", 
                         font=font_style, fg="#0085ba", cursor="hand2")
        label.place(x=10, y=730)
        label.bind("<Button-1>", lambda event: self.open_home(self.data))

    def open_home(self,data):
        home = Home(self.main_frame, data)



    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80)  # Thiết lập độ rộng cho cột
            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)


    def handle_missing_data(self):
        try: 
            if self.data.empty:  # Kiểm tra nếu data rỗng
                messagebox.showinfo("Notification", "Please upload data to perform the operation!")
                return
            self.data = handle_missing_data(self.data)
            self.update_callback(self.data)
            self.clear_widgets()
            self.setupUi()
            self.display_data()
            # messagebox.showinfo("Success", "Operation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while retrieving data: {}".format(str(e)))
        



class SplitApp:
    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.setupUi()
        self.data = data
        self.update_callback = update_callback
        self.display_data()

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        self.title_label = tk.Label(self.frame, text="Split Data Tool", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0,30))
        self.instruction_label = tk.Label(self.frame, text="Press the button below to split column", 
                                          fg="#ba0000", font=("Helvetica", 12))
        self.instruction_label.place(x=220, y = 200)
        self.push_button = tk.Button(self.frame, text="Split column", bg="#47676D", fg="white", 
                                     font=("Arial", 12), compound=tk.LEFT, command=self.split_column)
        # self.push_button.pack(pady=(140,30))
        self.push_button.pack(padx=(0,10), pady=(170, 20))
        self.text_edit = tk.Text(self.frame, height=1, width=20)
        self.text_edit.place(x=360, y=90)
        self.clear_button = tk.Button(self.frame, text="Delete", width=7, height=1, bg="#47676D", 
                                      fg="white", font=("Arial", 9), command=self.clear_text_box)
        self.clear_button.place(x=535, y=90)
        self.text_edit_2 = tk.Text(self.frame, height=1, width=20)
        self.text_edit_2.place(x=360, y=140)
        self.label = ttk.Label(self.frame, text="Choose columns:")
        self.label.place(x=180, y=90)
        self.label_2 = ttk.Label(self.frame, text="Character:")
        self.label_2.place(x=180, y=140)
        font_style = ("Arial", 12, "italic underline")
        label = tk.Label(self.main_frame, text="Do you want to go back to the homepage? Click here", 
                         font=font_style, fg="#0085ba", cursor="hand2")
        label.place(x=10, y=730)
        label.bind("<Button-1>", lambda event: self.open_home(self.data))

    def clear_text_box(self):
        self.text_edit.delete("1.0", tk.END)

    def open_home(self,data):
        home = Home(self.main_frame, data)

    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80)  # Thiết lập độ rộng cho cột
            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
    
    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        column_index = self.tree.identify_column(event.x)
        column_name = self.tree.heading(column_index)["text"]
        current_text = self.text_edit.get("1.0", tk.END).strip()
        if current_text:
            current_columns = current_text.split(",")
            if column_name not in current_columns:
                current_columns.append(column_name)
                self.text_edit.delete("1.0", tk.END)
                self.text_edit.insert(tk.END, ",".join(current_columns))
        else:
            self.text_edit.insert(tk.END, column_name)


    
    def split_column(self):
        try: 
            if self.data.empty:  # Kiểm tra nếu data rỗng
                messagebox.showinfo("Notification", "Please upload data to perform the operation!")
                return
            # Lấy giá trị từ text box và combo box
            columns_text = self.text_edit.get("1.0", tk.END).strip()
            char_text = self.text_edit_2.get("1.0", tk.END).strip()
            columns = columns_text.split(",") if columns_text else []

            # Điều chỉnh dữ liệu
            self.data = split_column(self.data, columns, char_text)
            self.update_callback(self.data)

            # Cập nhật giao diện hiển thị dữ liệu
            self.clear_widgets()
            self.setupUi()
            self.display_data()
            # messagebox.showinfo("Success", "Operation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while retrieving data: {}".format(str(e)))
        



class TypeApp:

    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.setupUi()
        self.data = data
        self.update_callback = update_callback
        self.display_data()

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        self.title_label = tk.Label(self.frame, text="Column Data Type Viewer", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0,30))
        self.instruction_label = tk.Label(self.frame, text="Press the button below to view the data type of the column",
                                           fg="#ba0000", font=("Helvetica", 12))
        self.instruction_label.place(x=220, y = 200)
        self.push_button = tk.Button(self.frame, text="Change data type", bg="#47676D", fg="white", 
                                     font=("Arial", 12), compound=tk.LEFT, command=self.change_data_type)
        # self.push_button.pack(pady=(140,30))
        self.push_button.pack(padx=(0,10), pady=(170, 20))
        self.combo_box = ttk.Combobox(self.frame)
        self.combo_box.place(x=370, y=140)
        self.combo_box['values'] = ("Float", "String", "DateTime", "Int")
        self.combo_box.current(0)
        self.text_edit = tk.Text(self.frame, height=1, width=20)
        self.text_edit.place(x=360, y=90)
        self.clear_button = tk.Button(self.frame, text="Delete", width=7, height=1, bg="#47676D", fg="white", 
                                      font=("Arial", 9), command=self.clear_text_box)
        self.clear_button.place(x=535, y=90)
        self.label = ttk.Label(self.frame, text="Choose column:")
        self.label.place(x=180, y=90)
        self.label_2 = ttk.Label(self.frame, text="Choose type:")
        self.label_2.place(x=180, y=140)
        font_style = ("Arial", 12, "italic underline")
        label = tk.Label(self.main_frame, text="Do you want to go back to the homepage? Click here", 
                         font=font_style, fg="#0085ba", cursor="hand2")
        label.place(x=10, y=730)
        label.bind("<Button-1>", lambda event: self.open_home(self.data))

    def clear_text_box(self):
        self.text_edit.delete("1.0", tk.END)

    def open_home(self,data):
        home = Home(self.main_frame, data)

    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()


    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80)  # Thiết lập độ rộng cho cột

            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        column_index = self.tree.identify_column(event.x)
        column_name = self.tree.heading(column_index)["text"]
        current_text = self.text_edit.get("1.0", tk.END).strip()
        if current_text:
            current_columns = current_text.split(",")
            if column_name not in current_columns:
                current_columns.append(column_name)
                self.text_edit.delete("1.0", tk.END)
                self.text_edit.insert(tk.END, ",".join(current_columns))
        else:
            self.text_edit.insert(tk.END, column_name)



    def change_data_type(self):
        try: 
            if self.data.empty:  # Kiểm tra nếu data rỗng
                messagebox.showinfo("Notification", "Please upload data to perform the operation!")
                return
            # Lấy giá trị từ text box và combo box
            columns_text = self.text_edit.get("1.0", tk.END).strip()
            columns = columns_text.split(",") if columns_text else []
            method = self.combo_box.get().lower()

            # Điều chỉnh dữ liệu
            self.data = change_data_type(self.data, columns, method)
            self.update_callback(self.data)

            # Cập nhật giao diện hiển thị dữ liệu
            self.clear_widgets()
            self.setupUi()
            self.display_data()
            print(columns, method)
            # messagebox.showinfo("Success", "Operation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while retrieving data: {}".format(str(e)))

        


class Home:
    def __init__(self, parent, data, update_callback):
        self.parent = parent
        self.data = data 
        self.update_callback = update_callback
        self.setupUi()
        self.display_data()  

    def setupUi(self):
        self.clear_widgets()
        font = ("Arial", 11)
        self.parent.option_add("*Font", font)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=60, y=300, width=850, height=340)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.frame = ttk.Frame(self.main_frame)
        self.frame.place(x=100, y=0, width=750, height=300)
        title_label = tk.Label(self.frame, text="Data Handling Tools", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0,20))
        instruction_label = tk.Label(self.frame, text="Select an operation below:",fg="#ba0000", font=("Helvetica", 14))
        instruction_label.pack(pady=(0,30))
        button_config = {
            "width": 16,
            "height": 2,
            "bg": "#47676D",
            "fg": "white",
            "font": ("Helvetica", 12),
            "anchor": "center",
            "justify": "center"
        }
        normalize_button = tk.Button(self.frame, text="Normalize Data", command=lambda:self.open_adjust_ui(self.data), **button_config)
        normalize_button.place(x=5, y=115)
        handle_missing_button = tk.Button(self.frame, text="Handle Missing Data", command=lambda:self.open_missing_ui(self.data), **button_config)
        handle_missing_button.place(x=205, y=115)
        drop_duplicate_button = tk.Button(self.frame, text="Drop Duplicate", command=lambda:self.open_drop_ui(self.data), **button_config)
        drop_duplicate_button.place(x=405, y=115)
        data_type_button = tk.Button(self.frame, text="Data Type", command=lambda:self.open_type_ui(self.data), **button_config)
        data_type_button.place(x=605, y=115)
        view_entire_button = tk.Button(self.frame, text="View Entire Data", command=lambda:self.open_entire_ui(self.data), **button_config)
        view_entire_button.place(x=5, y=200)
        merge_column_button = tk.Button(self.frame, text="Merge Column", command=lambda:self.open_merge_ui(self.data), **button_config)
        merge_column_button.place(x=205, y=200)
        split_column_button = tk.Button(self.frame, text="Split Column", command=lambda:self.open_split_ui(self.data), **button_config)
        split_column_button.place(x=405, y=200)
        show_column_button = tk.Button(self.frame, text="Show Column Info", command=lambda:self.open_showcolumn_ui(self.data), **button_config)
        show_column_button.place(x=605, y=200)

    def clear_widgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def display_data(self):
        if self.data is not None:
            self.tree["columns"] = list(self.data.columns)
            for column in self.data.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=80)  # Thiết lập độ rộng cho cột

            for index, row in self.data.iterrows():
                values = [str(value) if pd.notnull(value) else "NaN" for value in row]
                self.tree.insert("", "end", values=values)
        self.scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure treeview scroll command
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

    def update_data(self, new_data):
        self.data = new_data

    def open_type_ui(self, data):
        type_app = TypeApp(self.main_frame, data, self.update_data)

    def open_drop_ui(self, data):
        drop_app = DropApp(self.main_frame, data, self.update_data)

    def open_adjust_ui(self, data):
        adjust_app = AdjustApp(self.main_frame, data, self.update_data)
        # adjust_app.display_data()

    def open_entire_ui(self, data):
        entire_app = EntireApp(self.main_frame, data, self.update_data)

    def open_merge_ui(self, data):
        merge_app = MergeApp(self.main_frame, data, self.update_data)

    def open_split_ui(self, data):
        split_app = SplitApp(self.main_frame, data, self.update_data)

    def open_missing_ui(self, data):
        missing_app = MissingApp(self.main_frame, data, self.update_data)

    def open_showcolumn_ui(self, data):
        show = ShowColumnApp(self.main_frame, data, self.update_data)