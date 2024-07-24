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
    

    tree = TreeExample.get_tree()
    base_dir = tree.base_dir
    
    env_file = base_dir.get('env')

    level_index = 4;
    level_group = tree.collect(level_index) 

    print('')
    
    print(str(TreePrinter.ContainerPrinter.get_structure_text(base_dir)))

    print('')

    print(str(TreePrinter.print(base_dir, TreePrinter.Formats.SUMMARY)))

    print('')

    print(str(TreePrinter.print_summary(env_file)))
    
    print('')
    
    print(len(level_group))
    
    print('')
    
    print('')

    #print('')
#
    #print('')
#
    #print('')

