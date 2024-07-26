import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from utils.tree.printer import TreePrinter
from utils.tree.helper import TreeExample
from utils.printer import PrinterHelper
from models.abstractGenerator import AbstarctGenerator
from models.tree2 import ContainerNode, Node, Tree, TreeData, NodeRegistry
from models.enhanced_tree import EnhancedTree
from typing import Union, List, Iterable, Dict, Literal



def run():

    print('')

    tree = generate_tree()

    enhanced_tree = EnhancedTree.Utils.upgrade(tree)

    enhanced_tree.print()

    path_to_search = 'src\\users\\users_utils\\user_initilaze.ts'

    search_result = enhanced_tree.search(path_to_search)

    print('')

    PrinterHelper.print('Search result:', PrinterHelper.Colors.GREEN)


    TreePrinter.print(search_result)

    print('')    


def collect_level_group(tree: Tree, level_index: int) -> List[Union['Node', 'ContainerNode']]:
    level_index = 2;
    level_group = tree.collect(level_index) 
    return level_group

def generate_tree() -> Tree:
    tree = TreeExample.get_tree()
    return tree

def get_nodes_group(tree: Tree, paths: Union[str, List[str]]) -> Union[List[Union['Node', 'ContainerNode']] , None]:
    results = tree.get(paths) 
    if results is None:
        return None
    if isinstance(results, List):
        return results
    return [results]

def get_list(tree: Tree, paths: Union[str, List[str]]) -> List[Union['Node', 'ContainerNode']]:
    results = tree.get(paths) 
    if results is None:
        return None
    if isinstance(results, List):
        return results
    return [results]
    