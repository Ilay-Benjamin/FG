import os
import argparse
import logging
from pathlib import Path


# Write the code of the helpers.py file -> make it helpful as global as possible 
class PathUtils:

    @staticmethod
    def create_file(path, overwrite=False):
        """
        Create a file at the specified path if it doesn't already exist.
        """
        if os.path.exists(path):
            if overwrite:
                os.remove(path)
                logging.info(f"Deleted file: {path}")
            else:
                logging.warning(f"File already exists: {path}")
                return
        Path(path).touch()

    @staticmethod

    @staticmethod
    def create_folder(path):
        """
        Create a folder at the specified path if it doesn't already exist.
        """
        try:
            os.makedirs(path)
            logging.info(f"Created folder: {path}")
        except FileExistsError:
            logging.warning(f"Folder already exists: {path}")

    def get_absolute_path(path):
        """
        Get the absolute path of a given path.
        """
        return Path(path).resolve()
    pass

    @staticmethod
    def is_path_exists(path):
        """
        Check if the path exists.
        """
        return os.path.exists(path)

    @staticmethod
    def is_path_format_valid(path):
        """
        Check if the path format is valid.
        """
        try:
            Path(path)
            return True
        except Exception:
            return False
        
    @staticmethod
    def get_current_folder_path():
        """
        Get the current folder.
        """
        return os.getcwd()
    
    @staticmethod
    def get_parent_folder_path(path):
        """
        Get the parent folder of a given path.
        """
        return Path(path).parent
    
    @staticmethod
    def get_parent_folder_name(path):
        """
        Get the parent folder name of a given path.
        """
        return Path(path).parent.name
    
    @staticmethod
    def get_folder_path(path):
        """
        Get the folder path of a given path.
        """
        return os.path.dirname(path)
    
    @staticmethod
    def get_file_path(path):
        """
        Get the file path of a given path.
        """
        return os.path.abspath(path)

    @staticmethod
    def get_folder_name(path):
        """
        Get the folder name of a given path.
        """
        return Path(path).name
    
    @staticmethod
    def get_file_name(path):
        """
        Get the file name of a given path.
        """
        return Path(path).stem
    
    @staticmethod
    def get_file_extension(path):
        """
        Get the file extension of a given path.
        """
        return Path(path).suffix
    
    @staticmethod
    def join_paths(*args):
        """
        Join multiple paths together.
        """
        return os.path.join(*args)
    
    @staticmethod
    def is_folder(path):
        """
        Check if the path is a folder.
        """
        return os.path.isdir(path)
    
    @staticmethod
    def is_file(path):
        """
        Check if the path is a file.
        """
        return os.path.isfile(path)
    
    @staticmethod
    def is_folder_empty(path):
        """
        Check if the folder is empty.
        """
        return len(os.listdir(path)) == 0
    
    @staticmethod
    def is_file_empty(path):
        """
        Check if the file is empty.
        """
        return os.path.getsize(path) == 0
    
    @staticmethod
    def get_folder_size(path):
        """
        Get the folder size of a given path.
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
    
    @staticmethod
    def get_file_size(path):
        """
        Get the file size of a given path.
        """
        return os.path.getsize(path)
    
    @staticmethod
    def get_folder_contents(path):
        """
        Get the contents of a folder.
        """
        return os.listdir(path)
    
    @staticmethod
    def get_file_contents(path, line_by_line=False):
        """
        Get the contents of a file.
        """
        with open(path, 'r') as f:
            if line_by_line:
                return f.readlines()
            else:
                return f.read()
                
    @staticmethod
    def write_to_file(path, content, append=False):
        """
        Write content to a file.
        """
        mode = 'a' if append else 'w'
        with open(path, mode) as f:
            f.write(content)

    @staticmethod
    def delete_entity(path):
        """
        Delete a file or folder.
        """
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)


class CLIUtils:

    @staticmethod
    def parse_arguments():
        """
        Parse command line arguments.
        """
        parser = argparse.ArgumentParser(description="Folder Generator")
        parser.add_argument('file_path', type=str, help="Path to the ASCII folder diagram file.")
        parser.add_argument('-d', '--dist', type=str, help="Path to the destination folder. Default is the current folder.", default=os.getcwd())
        args = parser.parse_args()              
        return args