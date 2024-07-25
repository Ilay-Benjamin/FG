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
from typing import Union, List, Iterable, Dict, Literal



def run():

    print('')

    tree = generate_tree()

    base_dir = tree.base_dir

    node_group = get_nodes_group(tree, ['src', 'user_model.ts', 'user_controller.ts', 'env'])
    PrinterHelper.print('\nGroup Nodes #1: ', [PrinterHelper.Formats.UNDERLINE, PrinterHelper.Colors.PURPLE])
    for node in node_group:
        print(f"({node.level} , {node.pos}) {node.name} {node.id}@ -> {node.path}")
    #get_list(tree, ['src', 'user_model.ts', 'user_controller.ts', 'env'])
    
    print('')

    tree2 = Tree(ContainerNode('second_base_dir'))

    level_index = 3;
    level_group = collect_level_group(tree, level_index)

    PrinterHelper.print('\nTree #1 Structure: ', [PrinterHelper.Formats.UNDERLINE, PrinterHelper.Colors.PURPLE])
    print(str(TreePrinter.ContainerPrinter.get_structure_text(base_dir)))
    
    print('')

    PrinterHelper.print('\nTree #1 Summary: ', [PrinterHelper.Formats.UNDERLINE, PrinterHelper.Colors.PURPLE])
    print(str(TreePrinter.print(base_dir, TreePrinter.Formats.SUMMARY)))

    print('')


    PrinterHelper.print('\nLevel Index: ', [PrinterHelper.Formats.UNDERLINE, PrinterHelper.Colors.PURPLE])
    print(level_index)

    print('')

    PrinterHelper.print('\nLevel Group: ', [PrinterHelper.Formats.UNDERLINE, PrinterHelper.Colors.PURPLE])
    for node in level_group:
        print(node.name + ' -> ' + node.path)


    
    print('')

    #print('')
#
    #print('')
#
    #print('')


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
    