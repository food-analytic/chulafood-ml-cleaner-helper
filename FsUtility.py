import os, csv
import global_variables
from pathlib import Path

def get_mode_path(mode):
    folder_name = ''
    if mode == 'prepare_train_set':
        folder_name = 'test' # prepare_train_set mode will move images from test_set to train_set
    elif mode == 'validate_suspect_set':
        folder_name = 'suspected'
    elif mode == 'validate_clean_set':
        folder_name = 'clean'
    elif mode == 'validate_trash_set':
        folder_name = 'trash'
    return os.path.join(global_variables.ROOT_PATH, folder_name)

def get_mode_target_path(mode):
    folder_name = ''
    if mode == 'prepare_train_set':
        folder_name = 'train'
    elif mode == 'validate_suspect_set':
        folder_name = 'trash'
    elif mode == 'validate_clean_set':
        folder_name = 'trash'
    elif mode == 'validate_trash_set':
        folder_name = 'clean'
    return os.path.join(global_variables.ROOT_PATH, folder_name)

def read_summary_data():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'summary.csv')
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                global_variables.summary_dict[row['class_name']] = { 'clean->trash': int(row['clean->trash']), 'suspect->trash': int(row['suspect->trash']), 'trash->clean': int(row['trash->clean']) }

def write_summary_data():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'summary.csv')
    with open(file_path, 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, ['class_name', 'clean->trash', 'suspect->trash', 'trash->clean'])
        writer.writeheader()
        for key, value in global_variables.summary_dict.items():
            writer.writerow({ 'class_name': key, 'clean->trash': value['clean->trash'], 'suspect->trash': value['suspect->trash'], 'trash->clean': value['trash->clean'] })