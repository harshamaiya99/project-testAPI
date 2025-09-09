import os
import shutil

def delete_folders(root_folder, target_folders=None):
    if target_folders is None:
        target_folders = [".idea", "__pycache__", ".pytest_cache", ".venv"]

    for dirpath, dirnames, filenames in os.walk(root_folder, topdown=True):
        for dirname in dirnames:
            if dirname in target_folders:
                folder_path = os.path.join(dirpath, dirname)
                print(f"Deleting: {folder_path}")
                shutil.rmtree(folder_path, ignore_errors=True)

if __name__ == "__main__":
    root_path = r"C:\Users\maiya\PycharmProjects"  # 🔹 Change this to your root folder
    delete_folders(root_path)
