import os
import shutil

from pandas import DataFrame


def move_zip_files() -> None:
    """
    Move all zip files in the current working directory to the 'project/data' directory.

    This function iterates through all files in the current working directory and moves
    any file with a '.zip' extension to the 'project/data' directory.

    Returns:
        None
    """
    for file in os.listdir(os.getcwd()):
        if file.endswith(".zip"):
            shutil.move(file, os.path.join(os.getcwd(), f"data/{file}"))


def unzip_files() -> None:
    """
    Unzips all the .zip files in the 'project/data' directory.

    This function changes the current working directory to 'project/data',
    iterates through all the files in the directory, and if a file has a
    .zip extension, it unpacks the archive and removes the original .zip file.

    Returns:
        None
    """
    os.chdir("data")
    for file in os.listdir(os.getcwd()):
        if file.endswith(".zip"):
            shutil.unpack_archive(file, os.getcwd())
            os.remove(file)


def delete_useless_files() -> None:
    """
    Deletes all files in the current directory that contain the letter 't' in their name and have a '.csv' extension.
    """
    for file in os.listdir(os.getcwd()):
        if "k_d_t" in file and file.endswith(".csv"):
            os.remove(file)

    os.chdir(os.path.dirname(os.path.dirname(os.getcwd())))
