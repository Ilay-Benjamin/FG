import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from utils.printer import PrinterHelper, PrinterData
from utils.tree.printer import TreePrinter
from models.abstractGenerator import AbstarctGenerator
from models.tree2 import ContainerNode, Node, Tree, TreeData, NodeRegistry
from typing import Union, List, Iterable, Dict, Callable, Literal
from enum import Enum   



class EnhancedTree(Tree):

    def __init__(self, base_dir: ContainerNode):
        super().__init__(base_dir)


    class __TreeUtils__:
        @staticmethod
        def upgrade(tree: 'Tree') -> 'EnhancedTree':
            return EnhancedTree(tree.base_dir)    
        
        @staticmethod
        def downgrade(tree: 'EnhancedTree') -> 'Tree':
            return Tree(tree.base_dir)
    
    class __TreeFactory__:
        @staticmethod
        def __create_new_tree__(base_dir: ContainerNode) -> 'EnhancedTree':
            return EnhancedTree(base_dir)
        
        @staticmethod
        def __create_tree_by_data__(data: TreeData) -> 'EnhancedTree':
            pass

        @staticmethod
        def create_tree(arg: Union[str, 'TreeData']) -> 'EnhancedTree':
            if isinstance(arg, str):
                return EnhancedTree.Factory.__create_new_tree__(ContainerNode(arg))
            elif isinstance(arg, TreeData):
                print('Creating tree by data')
            else:
                raise Exception('Invalid argument type')
            
    class __TreeSearch__():
        class __SearchTypes__(Enum):
            ID = 'ID',
            PATH = 'PATH',
            CORDINATES = 'CORDINATES',

            @staticmethod
            def is_exists(search_type: 'EnhancedTree.__TreeSearch__.__SearchTypes__'):
                return search_type in EnhancedTree.__TreeSearch__.__SearchTypes__.__members__
        
        
        @staticmethod
        def __search__(tree: 'EnhancedTree',
                    search_value: Union[str, dict['level':int, 'position':int], int]) -> Union['Node', 'ContainerNode']:
            if isinstance(search_value, str):
                return EnhancedTree.__TreeSearch__.__search_by_path__(tree, search_value)
            elif isinstance(search_value, dict):
                return EnhancedTree.__TreeSearch__.__search_by_cordinates__(tree, search_value)
            elif isinstance(search_value, int):
                return EnhancedTree.__TreeSearch__.__search_by_id__(tree, search_value)
            else:
                raise Exception('Invalid search value type')

        @staticmethod
        def __search_by_path__(tree: 'EnhancedTree', path: str) -> Union['Node', 'ContainerNode']:
            return EnhancedTree.__TreeSearch__.__search_by_path_handler__(tree, path)

        @staticmethod
        def __search_by_cordinates__(tree: 'EnhancedTree', cordinates: dict['level':int, 'position':int]) -> Union['Node', 'ContainerNode']:
            return EnhancedTree.__TreeSearch__.__search_by_cordinates_handler__(tree, cordinates)
        
        @staticmethod
        def __search_by_id__(tree: 'EnhancedTree', id:int) -> Union['Node', 'ContainerNode']:        
            return EnhancedTree.__TreeSearch__.__search_by_id_handler__(tree, id)

        @staticmethod
        def __search_by_path_handler__(tree: 'EnhancedTree', path: str) -> Union['Node', 'ContainerNode']:
            return tree.get_by_path(path)

        @staticmethod
        def __search_by_cordinates_handler__(tree: 'EnhancedTree', cordinates: dict['level':int, 'position':int]) -> Union['Node', 'ContainerNode']:
            return tree.get_by_cords(cordinates)

        @staticmethod
        def __search_by_id_handler__(tree: 'EnhancedTree', id:int) -> Union['Node', 'ContainerNode']:        
            return tree.get_by_id(id)
                
        @staticmethod
        def __search_by_type__(tree: 'EnhancedTree', search_type: Literal['EnhancedTree.SearchTypes'], 
                search_value: Union[str, dict['level':int, 'position':int], int]) -> Union['Node', 'ContainerNode']:
            if search_type == EnhancedTree.SearchTypes.ID:
                return EnhancedTree.__TreeSearch__.__search_by_id__(tree, search_value)
            elif search_type == EnhancedTree.SearchTypes.PATH:
                return EnhancedTree.__TreeSearch__.__search_by_path__(tree, search_value)
            elif search_type == EnhancedTree.SearchTypes.CORDINATES:
                return EnhancedTree.__TreeSearch__.__search_by_cordinates__(tree, search_value)
            else:  
                raise Exception('Invalid search type')

        Types = __SearchTypes__


    Factory: __TreeFactory__ = __TreeFactory__()
    Utils: __TreeUtils__ = __TreeUtils__()
    __Search__: __TreeSearch__ = __TreeSearch__()
    SearchTypes = __Search__.Types

    @staticmethod
    def create(root_dir_name: str) -> 'EnhancedTree':
        return EnhancedTree.Factory.create_tree(root_dir_name)
    
    def print(self, format: Literal['TreePrinter.Formats']=TreePrinter.Formats.STRUCTURE) -> 'EnhancedTree': 
        str_format = ''
        if format == TreePrinter.Formats.STRUCTURE:
            str_format = 'STRUCTURE'
        elif format == TreePrinter.Formats.DETAILS:
            str_format = 'DETAILS'
        elif format == TreePrinter.Formats.SUMMARY:
            str_format = 'SUMMARY'
        PrinterHelper.print('Tree Print (' + str_format + ')' + ': ', [PrinterHelper.Formats.UNDERLINE, PrinterHelper.Colors.PURPLE])
        TreePrinter.print(self.base_dir, format)

    def append(self, node: Union['Node', 'ContainerNode'], parent: Union['Node', 'ContainerNode']) -> 'EnhancedTree':
        self.base_dir.append(node, parent)
        return self
    
    def simplify(self):
        pass

    def search(self, search_value: Union[str, dict['level':int, 'position':int], int]) -> Union['Node', 'ContainerNode']:
        return EnhancedTree.__Search__.__search__(self, search_value)
    
    def depth(self)->int:
        return self.base_dir.get_max_depth()