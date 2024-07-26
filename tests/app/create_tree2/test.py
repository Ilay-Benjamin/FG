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
from models.graph import draw_graph, get_edges, get_positions
from typing import Union, List, Iterable, Dict, Literal



def run():

    print('')

    tree = generate_tree()

    enhanced_tree = EnhancedTree.Utils.upgrade(tree)

    enhanced_tree.print()

    base_dir = enhanced_tree.base_dir

    print('')

    PrinterHelper.print('\n' + 'Tree Depth:', PrinterHelper.Colors.GREEN)
    print(base_dir.get_depth())

    print('')

    PrinterHelper.print('\n' + 'Tree Direct Children (Top):', PrinterHelper.Colors.GREEN)
    print(base_dir.count())

    print('')
    
    PrinterHelper.print('\n' + 'Positions: ', PrinterHelper.Colors.ORANGE)
    positions = get_positions(base_dir)
    for p in positions:
        x = positions[p][0]
        y = positions[p][1]
        print(f'{p} -> {x}, {y}\n')
        
    print('')

    PrinterHelper.print('\n' + 'Edges: ', PrinterHelper.Colors.ORANGE)
    edges = get_edges(base_dir)
    for e in edges:
        n1 = e[0]
        n2 = e[1]
        print(f'{n1} -> {n2}\n')
        
    print('')
        
                #PrinterHelper.print(str(base_dir.get_max_depth(0)), PrinterHelper.Colors.CYAN, PrinterHelper.Formats.UNDERLINE)
    
    #rint('')

    #path_to_search = 'src\\users\\users_utils\\user_initilaze.ts'
    #path_to_search = 3
    #search_result = enhanced_tree.search({'level': 1, 'position': 3})

    #print('')

    #PrinterHelper.print('\n' + 'Search result:', PrinterHelper.Colors.GREEN)
    #TreePrinter.print(search_result)

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
    