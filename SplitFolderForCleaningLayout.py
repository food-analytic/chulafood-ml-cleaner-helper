from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFileDialog, QVBoxLayout, QProgressDialog, QMessageBox
import os, shutil
import global_variables

class SplitFolderForCleaning(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.split_folder_for_cleaning_layout = QHBoxLayout()
        self.addLayout(self.split_folder_for_cleaning_layout)

        self.split_folder_target_layout = QHBoxLayout()
        self.split_folder_target_desc = QLabel('Target directory: ')
        self.split_folder_target_layout.addWidget(self.split_folder_target_desc)
        self.split_folder_target_label = QLabel('')
        self.split_folder_target_layout.addWidget(self.split_folder_target_label)
        self.addLayout(self.split_folder_target_layout)
        # submit btn
        self.submit_btn = QPushButton('Split Folder')
        self.submit_btn.clicked.connect(self.submit_btn_clicked)
        self.addWidget(self.submit_btn)

    def submit_btn_clicked(self):
        self.split_all_class()
    
    def split_all_class(self):
        create_folder_names = ['train', 'test', 'clean', 'suspected', 'trash']
        create_folder_names_no_test = ['train', 'clean', 'suspected', 'trash']
        # create all folder at ROOT_PATH
        for item in create_folder_names:
            os.makedirs(os.path.join(global_variables.ROOT_PATH, item), exist_ok=True)
        # move all directory that name not match create_folder_names into "test"
        move_folders = [path for path in os.listdir(global_variables.ROOT_PATH) if os.path.isdir(os.path.join(global_variables.ROOT_PATH, path)) and path not in create_folder_names]
        for name in move_folders:
            os.rename(os.path.join(global_variables.ROOT_PATH, name), os.path.join(global_variables.ROOT_PATH, 'test', name))
            # create the same class folder in all created folder except "test"
            for name2 in create_folder_names_no_test:
                os.makedirs(os.path.join(global_variables.ROOT_PATH, name2, name), exist_ok=True)       
        # info user that operation is finished
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle('Spliting is finished.')
        msg_box.setText('Good job at waiting.')
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()