import sys, os
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QFileDialog, QLineEdit, QComboBox, QMessageBox
from FlowLayout import FlowLayout
from InitialSetupWindow import InitialSetupWindow
from MergeFolderAfterCleaningLayout import MergeFolderAfterCleaningLayout
from SplitFolderForCleaningLayout import SplitFolderForCleaning
from DashboardLayout import DashboardLayout
import global_variables
import FsUtility

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.btn_list = []

        self.setWindowTitle("Chulafood Cleaner Helper")
        self.resize(*global_variables.DEFAULT_MAIN_WINDOW_SIZE)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        # mode desc label
        self.mode_desc_label = QLabel('')
        self.main_layout.addWidget(self.mode_desc_label)
        # init mode desc label
        self.update_desc_label(mode='dashboard')

        # action option
        self.action_layout = QHBoxLayout()
        self.main_layout.addLayout(self.action_layout)

        # mode dropdown
        self.mode_combo_box = QComboBox()
        self.mode_combo_box.addItems(global_variables.MODES)
        self.mode_combo_box.currentTextChanged.connect(self.load_mode)
        self.mode_combo_box.currentTextChanged.connect(self.update_desc_label)
        self.action_layout.addWidget(self.mode_combo_box)

        # class dropdown
        self.class_combo_box = QComboBox()
        self.class_combo_box.currentTextChanged.connect(self.load_image_btn)
        self.action_layout.addWidget(self.class_combo_box)

        # next class btn
        self.next_class_btn = QPushButton("Next Class")
        self.next_class_btn.clicked.connect(self.next_class_btn_clicked)
        self.action_layout.addWidget(self.next_class_btn)

        # submit btn
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_btn_clicked)
        self.action_layout.addWidget(self.submit_btn)

        # selected images summary
        self.selected_summary_layout = QHBoxLayout()
        self.selected_summary_desc = QLabel("Select: ")
        self.selected_summary_value = QLabel("0")
        self.selected_summary_total_value = QLabel("/0")
        self.selected_summary_layout.addWidget(self.selected_summary_desc)
        self.selected_summary_layout.addWidget(self.selected_summary_value)
        self.selected_summary_layout.addWidget(self.selected_summary_total_value)
        self.action_layout.addLayout(self.selected_summary_layout)

        # image_button_content
        self.image_button_content_layout = FlowLayout()
        self.image_button_content_widget = QWidget()
        self.image_button_content_widget.setLayout(self.image_button_content_layout)        
        self.image_button_scroll = QScrollArea()
        self.image_button_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.image_button_scroll.setWidgetResizable(True)
        self.image_button_scroll.setWidget(self.image_button_content_widget)
        self.main_layout.addWidget(self.image_button_scroll)
        # init image_button_scroll state
        self.image_button_scroll.hide()

        # merge_folder_after_cleaning
        self.merge_folder_after_cleaning_layout = MergeFolderAfterCleaningLayout()
        self.merge_folder_after_cleaning_widget = QWidget()
        self.merge_folder_after_cleaning_widget.setLayout(self.merge_folder_after_cleaning_layout)
        self.main_layout.addWidget(self.merge_folder_after_cleaning_widget)
        # init merge_folder_after_cleaning_layout
        self.merge_folder_after_cleaning_widget.hide()

        # split_folder_for_cleaning
        self.split_folder_for_cleaning_layout = SplitFolderForCleaning()
        self.split_folder_for_cleaning_widget = QWidget()
        self.split_folder_for_cleaning_widget.setLayout(self.split_folder_for_cleaning_layout)
        self.main_layout.addWidget(self.split_folder_for_cleaning_widget)
        # init split_folder_for_cleaning_layout
        self.split_folder_for_cleaning_widget.hide()

        # dashboard
        self.dashboard_layout = DashboardLayout(change_mode=self.change_mode, change_class=self.change_class)
        self.dashboard_widget = QWidget()
        self.dashboard_widget.setLayout(self.dashboard_layout)
        self.main_layout.addWidget(self.dashboard_widget)
        # init dashboard_layout
        self.dashboard_widget.show()

        self.setCentralWidget(self.main_widget)

    def change_mode(self, mode):
        self.mode_combo_box.setCurrentText(mode)

    def change_class(self, class_name):
        self.class_combo_box.setCurrentText(class_name)

    def load_mode(self, mode):
        print(f'Load mode "{mode}"')
        if mode == 'dashboard':
            self.image_button_scroll.hide()
            self.merge_folder_after_cleaning_widget.hide()
            self.dashboard_widget.show()
            self.clear_image_btn()
            self.dashboard_layout.load_table_data()
        elif mode == 'merge_folder_after_cleaning':
            self.image_button_scroll.hide()
            self.merge_folder_after_cleaning_widget.show()
            self.dashboard_widget.hide()
            self.clear_image_btn()
        elif mode == 'split_folder_for_cleaning':
            self.image_button_scroll.hide()
            self.merge_folder_after_cleaning_widget.hide()
            self.dashboard_widget.hide()
            self.split_folder_for_cleaning_widget.show()
        else:
            self.merge_folder_after_cleaning_widget.hide()
            self.image_button_scroll.show()
            self.dashboard_widget.hide()
            self.reset_class_combo_box()
            self.class_combo_box.addItems(os.listdir(FsUtility.get_mode_path(mode)))

    def clear_image_btn(self):
        # clear old btn
        for item in self.btn_list:
            self.image_button_content_layout.removeWidget(item)
            item.deleteLater()
        self.btn_list.clear()
        self.selected_summary_value.setText("0")

    def reset_class_combo_box(self):
        # require disconnect before edit dropdown option to prevent unintention load_image_btn be called
        self.class_combo_box.currentTextChanged.disconnect(self.load_image_btn)
        for _ in range(self.class_combo_box.count()):
            self.class_combo_box.removeItem(0)
        self.class_combo_box.currentTextChanged.connect(self.load_image_btn)

    def load_image_btn(self, sub_path):
        self.clear_image_btn()
        # add new btn
        mode_path = FsUtility.get_mode_path(self.mode_combo_box.currentText())
        print('Load images from path', os.path.join(mode_path, sub_path))
        img_list = list(filter(lambda item: os.path.splitext(item)[1] in ['.jpg','.jpeg','.png'], os.listdir(os.path.join(mode_path, sub_path))))
        self.selected_summary_total_value.setText(f'/{len(img_list)}')
        for img_idx, img_name in enumerate(img_list):
            image_path = os.path.join(mode_path, sub_path, img_name)
            self.btn_list.append(QPushButton())
            self.btn_list[img_idx].img_source = image_path
            self.btn_list[img_idx].setCheckable(True)
            pxmap = QPixmap(image_path)
            if pxmap.width() > pxmap.height():
                pxmap = pxmap.scaledToWidth(global_variables.DEFAULT_IMAGE_BUTTON_SIZE[0])
            else:
                pxmap = pxmap.scaledToHeight(global_variables.DEFAULT_IMAGE_BUTTON_SIZE[0])
            self.btn_list[img_idx].setIcon(QIcon(pxmap))
            self.btn_list[img_idx].setIconSize(QSize(*global_variables.DEFAULT_IMAGE_BUTTON_SIZE))
            self.btn_list[img_idx].resize(QSize(*global_variables.DEFAULT_IMAGE_BUTTON_SIZE))
            self.btn_list[img_idx].clicked.connect(lambda checked, idx=img_idx: self.image_btn_clicked(idx))
            self.btn_list[img_idx].setStyleSheet('''
            QPushButton {
                border: 5px solid transparent;
            }
            QPushButton:checked {
                border: 5px solid red;
            }
            ''')
            self.image_button_content_layout.addWidget(self.btn_list[img_idx])
    
    def image_btn_clicked(self, button_idx):
        mode = self.mode_combo_box.currentText()
        value = int(self.selected_summary_value.text())
        if self.btn_list[button_idx].isChecked():
            new_value = value + 1
            self.selected_summary_value.setText(str(new_value))
        else:
            new_value = value - 1
            self.selected_summary_value.setText(str(new_value))
        if mode == 'prepare_train_set' and new_value == global_variables.TARGET_TRAIN_SET_SIZE:
            # ask user to submit now or not
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle('Submit to train set?')
            msg_box.setText(f'Move {new_value} images to train set?')
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            ret = msg_box.exec_()
            if ret == QMessageBox.Ok:
                self.submit_btn_clicked()

    def next_class_btn_clicked(self):
        next_idx = self.class_combo_box.currentIndex() + 1
        if next_idx < self.class_combo_box.count():
            self.class_combo_box.setCurrentIndex(next_idx)
        else:
            self.class_combo_box.setCurrentIndex(0)
            self.class_combo_box.setCurrentIndex(self.class_combo_box.count() - 1)
        self.image_button_scroll.verticalScrollBar().setValue(self.image_button_scroll.verticalScrollBar().minimum())

    def submit_btn_clicked(self):
        mode = self.mode_combo_box.currentText()
        # get all img_source of selected btn
        select_image_source_list = [btn.img_source for btn in filter(lambda item: item.isChecked(), self.btn_list)]
        # move all img to folder according to the mode
        target_path = FsUtility.get_mode_target_path(mode)
        for image_source in select_image_source_list:
            os.rename(image_source, os.path.join(target_path, self.class_combo_box.currentText(), os.path.basename(image_source)))
        # keep result in summary_dict
        if not self.class_combo_box.currentText() in global_variables.summary_dict:
            global_variables.summary_dict[self.class_combo_box.currentText()] = { 'clean->trash': 0, 'suspect->trash': 0, 'trash->clean': 0 }
        if mode == 'prepare_train_set':
            print(f'Move {len(select_image_source_list)} images from test to train')
        elif mode == 'validate_suspect_set':
            global_variables.summary_dict[self.class_combo_box.currentText()]['suspect->trash'] += len(select_image_source_list)
            print(f'Move {len(select_image_source_list)} images from suspect to trash')
            FsUtility.write_summary_data()
        elif mode == 'validate_clean_set':
            global_variables.summary_dict[self.class_combo_box.currentText()]['clean->trash'] += len(select_image_source_list)
            print(f'Move {len(select_image_source_list)} images from clean to trash')
            FsUtility.write_summary_data()
        elif mode == 'validate_trash_set':
            global_variables.summary_dict[self.class_combo_box.currentText()]['trash->clean'] += len(select_image_source_list)
            print(f'Move {len(select_image_source_list)} images from trash to clean')
            FsUtility.write_summary_data()
        # auto go to next class
        self.next_class_btn_clicked()

    def update_desc_label(self, mode):
        self.mode_desc_label.setText(global_variables.mode_description[mode])

def main():
    global_variables.init_variables()
    FsUtility.read_summary_data()

    app = QApplication(sys.argv)

    main_window = MainWindow()
    initial_setup_window = InitialSetupWindow(main_window.dashboard_layout)
    initial_setup_window.main_window = main_window
    # update label in SplitFolderForCleaningLayout when click at submit btn in InitialSetupWindow
    initial_setup_window.confirm_btn.clicked.connect(lambda: main_window.split_folder_for_cleaning_layout.split_folder_target_label.setText(global_variables.ROOT_PATH))
    app.exec()

if __name__ == '__main__':
    main()