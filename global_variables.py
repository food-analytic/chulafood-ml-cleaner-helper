import os

def init_variables():
    global ROOT_PATH, TARGET_TRAIN_SET_SIZE, DEFAULT_MAIN_WINDOW_SIZE, DEFAULT_IMAGE_BUTTON_SIZE, MODES, current_mode, summary_dict, mode_description
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    TARGET_TRAIN_SET_SIZE = 20
    DEFAULT_MAIN_WINDOW_SIZE = (1200, 600)
    DEFAULT_IMAGE_BUTTON_SIZE = (300, 300)
    MODES = ['dashboard', 'prepare_train_set', 'validate_suspect_set', 'validate_clean_set', 'validate_trash_set', 'generate_clean_folder']
    current_mode = MODES[0]
    summary_dict = {}
    mode_description = {
        'dashboard': 'Current stat of target path. Click at the table cell to go to specific mode and class.',
        'prepare_train_set': 'Submit to move images from "train_set" to "test_set".',
        'validate_suspect_set': 'Submit to move images from "suspect_set" to "trash_set".',
        'validate_clean_set': 'Submit to move images from "clean_set" to "trash_set".',
        'validate_trash_set': 'Submit to move images from "trash_set" to "clean_set".',
        'generate_clean_folder': 'Copy all images from "clean_set" and "suspect_set" to specific path. Should be used after finish cleaning.'
    }