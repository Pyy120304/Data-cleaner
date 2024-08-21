import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction, QMenuBar, QStackedWidget, QFileDialog
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
import pandas as pd  # Đảm bảo bạn đã cài đặt pandas để làm việc với dữ liệu
from data_cleaner import drop_duplicates  # Import the drop_duplicates function

# Giả định rằng bạn đã có các lớp UI từ file UI.py
from UI import drop, adjust, entire, merge, missing, split, type

class HomeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        layout = QVBoxLayout()
        
        # Main label
        self.title_label = QLabel("DATA CLEANER")
        self.title_label.setStyleSheet("font-size: 72px; font-weight: bold;")
        layout.addWidget(self.title_label)
        layout.addStretch()
        
        # Subtitle label
        self.subtitle_label = QLabel("UPLOAD NEW FILE TO CLEAN")
        self.subtitle_label.setStyleSheet("font-size: 20px; font-style: italic;")
        layout.addWidget(self.subtitle_label)
        
        # Icon and Upload button
        self.icon_label = QLabel()
        pixmap = QPixmap(".\\free-folder-icon-1449-thumb.png")
        self.icon_label.setPixmap(pixmap.scaled(100, 100))
        layout.addWidget(self.icon_label)
        
        self.upload_button = QPushButton("Upload File")
        self.upload_button.setStyleSheet("background-color: #47676D; color: white; font-size: 14px; padding: 10px;")
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def upload_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;CSV Files (*.csv)", options=options)
        if file_name:
            self.data = pd.read_csv(file_name)
            print(f"Selected file: {file_name}")
            print(f"Loaded data:\n{self.data.head()}")  # In ra dữ liệu để kiểm tra

class DataCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Cleaner")
        self.setGeometry(100, 100, 1000, 800)
        self.data = None  # Placeholder for the data
        self.create_widgets()
        
    def create_widgets(self):
        # Create menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        home_action = QAction("Home", self)
        exit_action = QAction("Exit", self)
        home_action.triggered.connect(lambda: self.display(0))
        open_action.triggered.connect(self.upload_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(home_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        drop_action = QAction("Drop Duplicates", self)
        adjust_action = QAction("Adjust Data", self)
        handle_missing_action = QAction("Handle Missing Data", self)
        drop_action.triggered.connect(lambda: self.display(1))
        adjust_action.triggered.connect(lambda: self.display(2))
        handle_missing_action.triggered.connect(lambda: self.display(3))
        edit_menu.addAction(drop_action)
        edit_menu.addAction(adjust_action)
        edit_menu.addAction(handle_missing_action)
        
        # Transform menu
        transform_menu = menubar.addMenu("Transform")
        change_type_action = QAction("Change Data Type", self)
        merge_column_action = QAction("Merge Column", self)
        split_column_action = QAction("Split Column", self)
        change_type_action.triggered.connect(lambda: self.display(4))
        merge_column_action.triggered.connect(lambda: self.display(5))
        split_column_action.triggered.connect(lambda: self.display(6))
        transform_menu.addAction(change_type_action)
        transform_menu.addAction(merge_column_action)
        transform_menu.addAction(split_column_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        entire_dataset_action = QAction("Entire Dataset", self)
        specific_column_action = QAction("Specific Column", self)
        entire_dataset_action.triggered.connect(lambda: self.display(7))
        specific_column_action.triggered.connect(lambda: self.display(7))  # Update as needed
        view_menu.addAction(entire_dataset_action)
        view_menu.addAction(specific_column_action)
        
        # Create QStackedWidget to hold different interfaces
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)
        
        # Create instances of the interfaces
        self.homeUI = HomeUI()
        
        self.dropUI = QWidget()
        self.dropForm = drop()
        self.dropForm.setupUi(self.dropUI)
        self.dropForm.pushButton.clicked.connect(self.drop_duplicates)  # Connect the button to the drop_duplicates method
        
        self.adjustUI = QWidget()
        self.adjustForm = adjust()
        self.adjustForm.setupUi(self.adjustUI)
        
        self.entireUI = QWidget()
        self.entireForm = entire()
        self.entireForm.setupUi(self.entireUI)
        
        self.mergeUI = QWidget()
        self.mergeForm = merge()
        self.mergeForm.setupUi(self.mergeUI)
        
        self.missingUI = QWidget()
        self.missingForm = missing()
        self.missingForm.setupUi(self.missingUI)
        
        self.splitUI = QWidget()
        self.splitForm = split()
        self.splitForm.setupUi(self.splitUI)
        
        self.typeUI = QWidget()
        self.typeForm = type()
        self.typeForm.setupUi(self.typeUI)
        
        # Add interfaces to stacked widget
        self.stackedWidget.addWidget(self.homeUI)
        self.stackedWidget.addWidget(self.dropUI)
        self.stackedWidget.addWidget(self.adjustUI)
        self.stackedWidget.addWidget(self.missingUI)
        self.stackedWidget.addWidget(self.mergeUI)
        self.stackedWidget.addWidget(self.splitUI)
        self.stackedWidget.addWidget(self.typeUI)
        self.stackedWidget.addWidget(self.entireUI)
    
    def display(self, index):
        self.stackedWidget.setCurrentIndex(index)
    
    def upload_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;CSV Files (*.csv)", options=options)
        if file_name:
            self.data = pd.read_csv(file_name)
            print(f"Loaded data: {file_name}")
            print(f"Data preview:\n{self.data.head()}")  # Kiểm tra dữ liệu được tải lên
    
    def save_file(self):
        if self.data is not None:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;CSV Files (*.csv)", options=options)
            if file_name:
                self.data.to_csv(file_name, index=False)
                print(f"Saved data: {file_name}")
        else:
            print("No data to save.")
    
    def drop_duplicates(self):
        if self.data is not None:
            self.data = drop_duplicates(self.data)
            print("Duplicates dropped.")
            print(f"Data after dropping duplicates:\n{self.data.head()}")  # Kiểm tra dữ liệu sau khi xóa trùng lặp
        else:
            print("No data loaded.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = DataCleanerApp()
    main_window.show()
    sys.exit(app.exec_())
