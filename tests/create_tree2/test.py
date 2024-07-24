import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from utils.tree.printer import TreePrinter
from utils.tree.helper import TreeExample
from models.abstractGenerator import AbstarctGenerator
from models.tree2 import ContainerNode, Node, Tree, TreeData, NodeRegistry
from typing import Union, List, Iterable, Dict



def run():
    

    base_dir = TreeExample.get_base_dir()
    
    env_file = base_dir.get('env')

    print(str(base_dir.to_structure_string()))

    print('')
    
    print(str(TreePrinter.ContainerPrinter.get_structure_text(base_dir)))

    print('')
    

    print('base_dir - TYPE :    ', type(base_dir))
    
    print('')

    print('base_dir - TYPE :    ', type(env_file))
    
    print('')
    
    print('')
    

    #print('')
#
    #print('')
#
    #print('')

