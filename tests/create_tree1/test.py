import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from models.abstractGenerator import AbstarctGenerator
from models.tree2 import ContainerNode, Node, Tree, TreeData
from typing import Union, List, Iterable, Dict



def run():
    
    base_dir = ContainerNode._create_root("base_dir")

    tree1 = Tree(base_dir)
    
    src_top_dir =  ContainerNode("src", base_dir)
    utils_dir = ContainerNode("utils", base_dir)
    
    models_dir = ContainerNode("models", src_top_dir)
    controllers_dir = ContainerNode("controllers", src_top_dir)

    initilaizes_dir = ContainerNode("initilaziesUtils", utils_dir)

    user_controllers_dir = ContainerNode("user_controllers", controllers_dir)
    game_controllers_dir = ContainerNode("game_controllers", controllers_dir)
    
    user_models_dir = ContainerNode("user_models", models_dir)
    game_models_dir = ContainerNode("game_models", models_dir)
    
    main_script = Node("main.py", src_top_dir)
    secondary_script = Node("secondary.py", src_top_dir)

    helper_script = Node("helpers.py", utils_dir)

    initilazeApp_script = Node("init.py", initilaizes_dir)
    initilazeDB_script = Node("init_db.py", initilaizes_dir)
    initilazeLogger_script = Node("init_logger.py", initilaizes_dir)

    user_controller1 = Node("user_controller1.py", user_controllers_dir)
    user_controller2 = Node("user_controller2.py", user_controllers_dir)

    game_controller1 = Node("game_controller1.py", game_controllers_dir)
    game_controller2 = Node("game_controller2.py", game_controllers_dir)

    user_model1 = Node("user_model1.py", user_models_dir)
    user_model2 = Node("user_model2.py", user_models_dir)

    game_model1 = Node("game_model1.py", game_models_dir)
    game_model2 = Node("game_model2.py", game_models_dir)


    config_dir = ContainerNode("config", base_dir)

    tree1_data = TreeData(tree1)

    print('')
 
    print(str(src_top_dir.to_detailed_string()))

    print('')
    
    print(str(base_dir.children))

    print('')

    print('')

    print('')

    #print(tree1_data.__str__())

   # print(base_dir.to_detailed_string())
   
    #tree1_data.print_matrix()