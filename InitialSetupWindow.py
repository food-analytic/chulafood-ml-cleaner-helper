from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QIntValidator
import os
import global_variables

class InitialSetupWindow(QMainWindow):
    def __init__(self, dashboard_layout):
        super().__init__()
        self.dashboard_layout = dashboard_layout

        self.setWindowTitle("Initial Setup")
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # root path
        self.root_path_layout = QHBoxLayout()
        self.layout.addLayout(self.root_path_layout)

        self.root_path_label_desc = QLabel('Data Location')
        self.root_path_layout.addWidget(self.root_path_label_desc)

        self.root_path_label_directory = QLabel(os.path.dirname(os.path.abspath(__file__)))
        self.root_path_label_directory.setStyleSheet('''
        border: 1px solid black;
        background-color: #fff;
        ''')
        self.root_path_layout.addWidget(self.root_path_label_directory)

        self.root_path_btn = QPushButton("Browse")
        self.root_path_btn.setMaximumWidth(100)
        self.root_path_btn.clicked.connect(self.get_directory)
        self.root_path_layout.addWidget(self.root_path_btn)

        # target train set size
        self.target_train_set_size_layout = QHBoxLayout()
        self.layout.addLayout(self.target_train_set_size_layout)

        self.target_train_set_size_label = QLabel("Target Train Set Size: ")
        self.target_train_set_size_layout.addWidget(self.target_train_set_size_label)

        self.target_train_set_size_line_edit = QLineEdit()
        self.target_train_set_size_line_edit.setMaxLength(3)
        self.target_train_set_size_line_edit.setValidator(QIntValidator(0, 999))
        self.target_train_set_size_line_edit.setText(str(global_variables.TARGET_TRAIN_SET_SIZE))
        self.target_train_set_size_line_edit.textChanged.connect(self.update_target_train_set_size)
        self.target_train_set_size_layout.addWidget(self.target_train_set_size_line_edit)

        # image button size
        self.image_btn_size_layout = QHBoxLayout()
        self.layout.addLayout(self.image_btn_size_layout)

        self.image_btn_size_label = QLabel("Image Size (square): ")
        self.image_btn_size_layout.addWidget(self.image_btn_size_label)

        self.image_btn_size_line_edit = QLineEdit()
        self.image_btn_size_line_edit.setMaxLength(3)
        self.image_btn_size_line_edit.setValidator(QIntValidator(1, 999))
        self.image_btn_size_line_edit.setText(str(global_variables.DEFAULT_IMAGE_BUTTON_SIZE[0]))
        self.image_btn_size_line_edit.textChanged.connect(self.update_image_btn_size)
        self.image_btn_size_layout.addWidget(self.image_btn_size_line_edit)

        # confirm button
        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.clicked.connect(self.open_main_window)
        self.layout.addWidget(self.confirm_btn)

        self.setCentralWidget(self.widget)
        self.show()
    
    def get_directory(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dlg.filesSelected.connect(lambda x: self.root_path_label_directory.setText(x[0]))
        if dlg.exec_():
            global_variables.ROOT_PATH = dlg.selectedFiles()[0]
            print(f'Set ROOT_PATH as {global_variables.ROOT_PATH}')
    
    def update_target_train_set_size(self, x):
        global_variables.TARGET_TRAIN_SET_SIZE = int(x)
        print(f'Set TARGET_TRAIN_SET_SIZE as {str(global_variables.TARGET_TRAIN_SET_SIZE)}')

    def update_image_btn_size(self, x):
        global_variables.DEFAULT_IMAGE_BUTTON_SIZE = (int(x), int(x))
        print(f'Set DEFAULT_IMAGE_BUTTON_SIZE as {str(global_variables.DEFAULT_IMAGE_BUTTON_SIZE)}')

    def open_main_window(self):
        self.dashboard_layout.load_table_data()
        self.close()
        self.main_window.show()