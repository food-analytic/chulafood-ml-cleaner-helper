from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFileDialog, QVBoxLayout, QProgressDialog, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
import os, shutil
import global_variables

class DashboardLayout(QVBoxLayout):    
    def __init__(self, change_mode, change_class):
        super().__init__()
        self.table_data = {}
        self.change_mode = change_mode
        self.change_class = change_class

        self.table = QTableWidget()
        self.addWidget(self.table)
        self.table.cellClicked.connect(self.cell_clicked)
        row_size = 3
        self.column_name = ['train', 'test', 'clean', 'suspected', 'trash']
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['class name', *self.column_name])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    
    def cell_clicked(self, row, col):
        class_name = self.table.item(row, 0).text()
        column_name = self.table.horizontalHeaderItem(col).text()
        if column_name in ['train', 'clean', 'suspected', 'trash']:
            if column_name == 'train':
                mode = 'prepare_train_set'
            elif column_name == 'clean':
                mode = 'validate_clean_set'
            elif column_name == 'suspected':
                mode = 'validate_suspect_set'
            elif column_name == 'trash':
                mode = 'validate_trash_set'
            # ask user to go or not
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle('Sure?')
            msg_box.setText(f'Go to "{class_name}" -> mode "{mode}"?')
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            ret = msg_box.exec_()
            if ret == QMessageBox.Ok:
                print(mode, class_name)
                self.change_mode(mode)
                self.change_class(class_name)
    
    def load_table_data(self):
        self.table_data.clear()
        for column_idx, column_item in enumerate(self.column_name):
            class_list = os.listdir(os.path.join(global_variables.ROOT_PATH, column_item))
            for item in class_list:
                if not item in self.table_data.keys():
                    self.table_data[item] = ['n/a'] * len(self.column_name)
                if self.table_data[item][column_idx] == 'n/a':
                    self.table_data[item][column_idx] = len(os.listdir(os.path.join(global_variables.ROOT_PATH, column_item, item)))
                else:
                    self.table_data[item][column_idx] += len(os.listdir(os.path.join(global_variables.ROOT_PATH, column_item, item)))
        self.table.setRowCount(len(self.table_data.keys()))
        for key_idx, [key, value] in enumerate(self.table_data.items()):
            self.table.setItem(key_idx, 0, QTableWidgetItem(str(key)))
            for value_item_idx, value_item in enumerate(value):
                self.table.setItem(key_idx, value_item_idx+1, QTableWidgetItem(str(value_item)))