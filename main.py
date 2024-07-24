import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils 
from models.builder import Builder
from tests.create_tree2.test import run




def create_folders_from_diagram(file_path, dist):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    current_path = [dist]
    for line in lines:
        stripped_line = line.rstrip()
        if stripped_line:
            # Calculate depth based on the leading tree structure characters
            depth = len(stripped_line) - len(stripped_line.lstrip(' │├└'))
            # Extract folder name after the tree structure characters
            folder_name = stripped_line.split('─')[-1].strip()
            if folder_name.endswith('/'):
                folder_name = folder_name[:-1]
            # Adjust the current path based on the depth
            while len(current_path) > depth + 1:  # Adjust +1 because dist is already in the path
                current_path.pop()
            if folder_name:
                current_path.append(folder_name)
                dir_path = os.path.join(*current_path)
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Created directory: {dir_path}")
                print(f"Created directory: {dir_path}")



def main():
    parser = argparse.ArgumentParser(description="Folder Generator Tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    build_parser = subparsers.add_parser('build', help='Execute the build command')
    Builder.parse_arguments(build_parser)

    args = parser.parse_args()

    if args.command == 'build':
        Builder.handle_request(args)


if __name__ == "__main__":
    run()