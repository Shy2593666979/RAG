import os

def get_folder_file(folder_path): # 加载文件夹下全部的文件
    all_file = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        all_file.append(file_path)

    return all_file

def get_folder_PDF(folder_path): # 加载文件夹下所有PDF文件
    all_file = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            all_file.append(file_path)

    return all_file

def get_folder_Excel(folder_path): # 加载文件夹下所有Excel文件
    all_file = []

    for file in os.listdir(folder_path):
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            all_file.append(file_path)

    return all_file

def get_folder_Word(folder_path): # 加载文件夹下所有Word文件
    all_file = []

    for file in os.listdir(folder_path):
        if file.endswith(".docx"):
            file_path = os.path.join(folder_path, file)
            all_file.append(file_path)

    return all_file
