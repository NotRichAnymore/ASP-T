import os
import json
import sys

import configupdater as configupdater
import pandas as pd
import base64
from pathlib import Path


# File Handling

# - Directory
def create_directory(directory):
    try:
        print(f"Creating directory: {directory}")
        os.mkdir(directory)

    except FileExistsError:
        print("Directory already exists")


def check_directory_exists(file_path):
    directoryExists = os.path.isdir(file_path)
    if directoryExists:
        return True
    elif not directoryExists:
        return False


def get_root_directory():
    return os.path.dirname(sys.path[0])


# - Files
def check_file_exists(file_path):
    fileExists = os.path.exists(file_path)
    if fileExists:
        return True
    elif not fileExists:
        return False


def check_file_empty(file_path):
    fileIsEmpty = os.stat(file_path).st_size == 0
    if fileIsEmpty:
        return True
    elif not fileIsEmpty:
        return False


def create_internal_files(file_path):
    match (os.path.basename(file_path)):
        case 'command_help.txt':
            with open(file_path, 'w') as file:
                file.write('')


def initialise_internal_files(directory):
    filenames = ['command_help.txt']

    presentFiles = []
    try:
        while len(presentFiles) != len(filenames):
            for file in filenames:
                internalFilePath = directory + "/" + file
                fileExists = os.path.exists(internalFilePath)
                print(internalFilePath, fileExists)
                if fileExists:
                    if internalFilePath not in presentFiles:
                        presentFiles.append(internalFilePath)
                        print(presentFiles)
                elif not fileExists:
                    print(f'Creating {file}')
                    create_internal_files(internalFilePath)

        if len(presentFiles) == len(filenames):
            return True
        else:
            return False
    except FileNotFoundError:
        os.mkdir(directory)


# - CSV Format
def write_to_csv(data, file_path):
    df = pd.DataFrame([data])
    df.to_csv(file_path, mode='w', index=False)
    print(f'Written to: {file_path}')


def append_to_csv(data, file_path):
    df = pd.DataFrame([data])
    with open(file_path, 'a') as file:
        df.to_csv(file, mode='a', index=False, header=not os.path.exists(file_path))


def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        fileContents = pd.read_csv(csvfile)
    print(f'Read {file_path}')
    return fileContents


def remove_null_rows(file_path):
    fileContents = read_csv(file_path)
    for index, row in fileContents.iterrows():
        if row[index] == 'null':
            row[index] = row[index].str.rstrip('null')
    return fileContents


# Json Format
def get_json_object_from_file(file_path):
    jsonObject = {}
    with open(file_path, "r") as file:
        for obj in file:
            jsonDict = json.loads(obj)
            jsonObject = jsonDict
    return jsonObject


# From Paths
def get_filename_from_path(file_path):
    filename = os.path.basename(file_path)
    return filename


def get_new_unit_test_paths():
    scripts = []
    rootdir = Path(__file__).resolve().parent.parent.parent
    directories_to_exclude = ['Files', 'Images', 'Tests']
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for directory in directories_to_exclude:
            if '\\src\\' in dirpath and directory not in dirpath:
                for file in filenames:
                    if os.path.exists(os.path.join(dirpath, os.path.join('test_' + file))):
                        continue
                    if '.py' == Path(file).suffix:
                        if os.path.join(dirpath, file) not in scripts:
                            scripts.append(os.path.join(dirpath, file))
    return scripts


# Base 64 Operations
# - Encoding
def image_to_base64(directory, icon_names):
    base64Icons = []
    for name in icon_names:
        icon = set_icon(directory, name)
        with open(icon, 'rb') as file:
            base64Icons.append(base64.encodebytes(file.read()))

    return base64Icons


# - Decoding
def base64_to_image(main_directory, image_file):
    updater = configupdater.ConfigUpdater()
    iconsFile = "src/Images/Icons"
    filePath = Path.joinpath(main_directory, iconsFile)
    with open(filePath, 'r+') as file:
        updater.read_file(file)

    options = updater.options('Icons')
    for key in options:
        if key.lower() in os.path.basename(image_file).lower():
            with open(image_file, 'wb') as file:
                img = base64.b64decode(updater['Icons'][key].value)
                file.write(img)


# Image Handling        
def set_icon(main_directory, file_name):
    file_name = "src/Images/Icon" + file_name
    icon = Path.joinpath(main_directory, file_name)
    return icon


def initialise_images(directory):
    presentFiles = []

    iconNames = ['back_icon.png']

    try:
        while len(presentFiles) != len(iconNames):
            for file in iconNames:
                imagePath = directory + "/" + file
                iconExists = os.path.exists(imagePath)
                if iconExists:
                    presentFiles.append(file)
                elif not iconExists:
                    print(f'Creating {file}')
                    base64_to_image(directory, imagePath)

        if len(presentFiles) == len(iconNames):
            return True
        else:
            return False
    except FileNotFoundError:
        os.mkdir(directory)


def create_error_message(error_type, message, error_message):
    return f'Error Type: {error_type}, {message} \nError Message: {error_message}'
