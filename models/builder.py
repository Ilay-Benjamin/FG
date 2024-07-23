import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from models.abstractGenerator import AbstarctGenerator



class Builder(AbstarctGenerator):

    @staticmethod
    def parse_arguments(parser: argparse.ArgumentParser):
        parser.add_argument('-o', '--override', action="store_true", default=False, help="Is Override to use. Default is 'build'.")
        parser.add_argument('source', type=str, help="Path to the ASCII folder diagram file.")
        parser.add_argument('dist', nargs='?', type=str, default=None, help="Path to the destination folder. Default is the current folder.")

    @staticmethod
    def handle_request(args):
        request_data = {
            "args": args.__dict__,
        }   
        request_data['args']["dist"] = request_data['args']["dist"] if request_data['args']["dist"] else PathUtils.join_paths(os.getcwd(), PathUtils.get_folder_name(request_data['args']["source"]))
        if PathUtils.is_path_exists(request_data['args']["dist"]):
            if not PathUtils.is_folder_empty(request_data['args']["dist"]):
                if request_data['args']["override"]:
                    shutil.rmtree(request_data['args']["dist"])
                    PathUtils.create_folder(request_data['args']["dist"])
                else: 
                    raise ValueError("Destination folder is not empty. Use the '-o' flag to override, or the '-a' flag to append.")
            else:   
                pass
        else:
            PathUtils.create_folder(request_data['args']["dist"])
        Builder.generate(request_data)

    @staticmethod
    def dist_tests(dist):
        return [
            { "function": lambda: PathUtils.is_path_format_valid(dist), "errorMessage": "Destination folder path is invalid." },
            { "function": lambda: PathUtils.is_path_exists(dist), "errorMessage": "Destination folder does not exist." },        
            { "function": lambda: PathUtils.is_folder(dist), "errorMessage": "Destination is not a folder." },
        ]

    @staticmethod
    def source_tests(source):
        return [
            { "function": lambda: PathUtils.is_path_format_valid(source), "errorMessage": "Source file path is invalid." },
            { "function": lambda: PathUtils.is_path_exists(source), "errorMessage": "Source file does not exist."},
            { "function": lambda: PathUtils.is_file(source), "errorMessage": "Source isn't a file."},
            { "function": lambda: PathUtils.get_file_extension(source) == '.txt', "errorMessage": "Source file is not a text file."},
            { "function": lambda: not PathUtils.is_file_empty(source), "errorMessage": "Source file is empty."},
        ]
    
    @staticmethod
    def is_dist_valid(dist):
        for test in Builder.dist_tests(dist):
            if not test["function"]:
                return {"status": False, "message": test["errorMessage"]}
        return {"status": True, "message": "Destination folder is valid."}  
    
    @staticmethod
    def is_source_valid(source):
        for test in Builder.dist_tests(source):
            if not test["function"]:
                return {"status": False, "message": test["errorMessage"]}
        return {"status": True, "message": "Source folder is valid."}
    

    @staticmethod
    def check_dist(dist):
        dist_results = Builder.is_dist_valid(dist)
        if not dist_results["status"]:
            raise ValueError(dist_results["message"])
        return dist_results
    
    @staticmethod
    def check_source(source):
        source_results = Builder.is_source_valid(source)
        if not source_results["status"]:
            raise ValueError(source_results["message"])
        return source_results
    
    @staticmethod
    def handle_generate(request_data):
        logging.info("Generating folders and files...")
        source = request_data['args']['source']
        dist = request_data['args']['dist']
        
        with open(source, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        current_path = [dist]
        for line in lines:
            stripped_line = line.rstrip()
            if stripped_line:
                # Calculate depth based on the leading tree structure characters
                depth = len(stripped_line) - len(stripped_line.lstrip(' │├└'))
                # Extract folder or file name after the tree structure characters
                item_name = stripped_line.split('─')[-1].strip()
                print(item_name)
                if item_name.endswith('/'):
                    item_name = item_name[:-1]
                    is_folder = True
                else:
                    is_folder = False
                
                # Adjust the current path based on the depth
                while len(current_path) > depth + 1:  # Adjust +1 because dist is already in the path
                    current_path.pop()
                current_path.append(item_name)
                
                item_path = os.path.join(*current_path)
                if is_folder:
                    if not os.path.exists(item_path):
                        os.makedirs(item_path)
                        logging.info(f"Created directory: {item_path}")
                else:
                    parent_dir = os.path.dirname(item_path)
                    if not os.path.exists(parent_dir):
                        os.makedirs(parent_dir)
                        PathUtils.create_file(item_path)
                    logging.info(f"Created file: {item_path}")
        
        return {"status": True, "message": "Folders and files created successfully."}

    @staticmethod
    def handle_response(results):
        print(results["message"])
        return results

    @staticmethod
    def generate(request_data):
        Builder.check_source(request_data['args']["source"])
        Builder.check_dist(request_data['args']["dist"])
        results = Builder.handle_generate(request_data)
        reponse_data = Builder.handle_response(results)
        return reponse_data


class FolderGenerator():
    pass
    

