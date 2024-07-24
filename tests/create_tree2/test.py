import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from models.abstractGenerator import AbstarctGenerator
from models.tree2 import ContainerNode, Node, Tree, TreeData, NodeRegistry
from typing import Union, List, Iterable, Dict



def run():
    
    base_dir = ContainerNode._create_root("base_dir")

    tree1 = Tree(base_dir)
    
    env_file = Node("env", base_dir)
    src_top_dir =  ContainerNode("src", base_dir)

    users_dir = ContainerNode("users", src_top_dir)

    user_model_file = Node("user_model.ts", users_dir)
    user_controller_file = Node("user_controller.ts", users_dir)
    user_utils_dir = ContainerNode("users_utils", users_dir)

    user_initilaze_file = Node("user_initilaze.ts", user_utils_dir)

    config_dir = ContainerNode("config", base_dir)

    global_config_dir = ContainerNode("global_config", config_dir)
    app_config_file = Node("app_config.json", global_config_dir)
    db_config_file = Node("db_config.json", global_config_dir)

    tsconfig_json_file = Node("tsconfig.json", base_dir)

    tree1_data = TreeData(tree1)


    print('')

    print(base_dir.to_structure_string())

    print('')

    print('')
