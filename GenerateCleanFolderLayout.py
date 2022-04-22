from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFileDialog, QVBoxLayout, QProgressDialog
import os, shutil
import global_variables

class GenerateCleanFolderLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.generate_clean_folder_layout = QHBoxLayout()
        self.addLayout(self.generate_clean_folder_layout)
        self.generate_clean_folder_label = QLabel(os.path.dirname(os.path.abspath(__file__)))
        self.generate_clean_folder_layout.addWidget(self.generate_clean_folder_label)
        self.generate_clean_folder_btn = QPushButton('Browse')
        self.generate_clean_folder_btn.clicked.connect(self.get_directory)
        self.generate_clean_folder_layout.addWidget(self.generate_clean_folder_btn)

        # submit btn
        self.submit_btn = QPushButton('Generate Clean Folder')
        self.submit_btn.clicked.connect(self.submit_btn_clicked)
        self.addWidget(self.submit_btn)
    
    def get_directory(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dlg.filesSelected.connect(lambda x: self.generate_clean_folder_label.setText(x[0]))
        dlg.exec_()
    
    def submit_btn_clicked(self):
        target_path = self.generate_clean_folder_label.text()
        parent_folder_name = os.path.basename(global_variables.ROOT_PATH)
        total_class = len(os.listdir(os.path.join(global_variables.ROOT_PATH, 'clean'))) + len(os.listdir(os.path.join(global_variables.ROOT_PATH, 'suspected')))
        self.progress = QProgressDialog("Copying images...", None, 0, total_class)
        self.progress.setWindowTitle('Generate Clean Folder Progress')
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setValue(0)
        self.progress.setMinimumDuration(0)
        self.progress.show()
        self.move_all_class_to_target(os.path.join(global_variables.ROOT_PATH, 'clean'), os.path.join(target_path, parent_folder_name))
        self.move_all_class_to_target(os.path.join(global_variables.ROOT_PATH, 'suspected'), os.path.join(target_path, parent_folder_name))
        self.progress.setValue(total_class)
    
    def move_all_class_to_target(self, src, dst):
        class_list = os.listdir(src)
        if not os.path.exists(dst):
            os.mkdir(dst)
        for class_item in class_list:
            target_path = os.path.join(dst, class_item)
            if not os.path.exists(target_path):
                os.mkdir(target_path)
            for item in os.listdir(os.path.join(src, class_item)):
                shutil.copy(os.path.join(src, class_item, item), os.path.join(target_path, item))
            self.progress.setValue(self.progress.value() + 1)