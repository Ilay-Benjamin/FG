import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from utils.printer import PrinterHelper, PrinterData
from models.abstractGenerator import AbstarctGenerator
from typing import Union, List, Iterable, Dict, Callable, Literal
from enum import Enum



class Validation():

    class AllowedNodeMethods(Enum):
        MOVE = 'move',

        @staticmethod
        def __methods():
            methods = {
                Validation.AllowedNodeMethods.MOVE: 
                    lambda target, new_parent: isinstance(new_parent, ContainerNode) and target.parent != new_parent 
            }
            return methods
        
        @staticmethod
        def is_exists(method:Literal['Validation.NodeMethods']):
            return method in Validation.AllowedNodeMethods.__methods()[method]
        
    class AllowedContainerNodeMethods(Enum):
        MOVE = 'move',
        APPEND = 'append',
        REMOVE = 'remove',

        @staticmethod
        def __methods():
            methods = {
                Validation.AllowedNodeMethods.MOVE: 
                    lambda target, new_parent: isinstance(new_parent, ContainerNode) and target.parent != new_parent,
                Validation.AllowedNodeMethods.APPEND:
                    lambda target, new_child: (isinstance(new_child, ContainerNode) or isinstance(new_child, Node)) and new_child.parent != target,
                Validation.AllowedNodeMethods.REMOVE:
                    lambda target, child: (isinstance(child, Node) or isinstance(child, str)) and child.parent == target
            }
            return methods
        
        @staticmethod
        def is_exists(method:Literal['Validation.ContainerNodeMethods']):
            return method in Validation.AllowedContainerNodeMethods.__methods()[method]
    
    NodeMethods = AllowedNodeMethods
    ContainerNodeMethods = AllowedContainerNodeMethods 

    @staticmethod
    def validate_node(method:Literal['Validation.NodeMethods'], target:'Node', *args) -> bool:
        return Validation.AllowedNodeMethods.__methods()[method](target, *args)

    @staticmethod
    def validate_container_node(method:Literal['Validation.ContainerNodeMethods'], target:'ContainerNode', *args) -> bool:
        return Validation.AllowedContainerNodeMethods.__methods()[method](target, *args)

    @staticmethod  
    def validate(method:Literal['Validation.NodeMethods', 'Validation.ContainerNodeMethods'], target:Union['Node', 'ContainerNode'], *args) -> bool:
        if (Validation.NodeMethods.is_exists(method) and Validation.ContainerNodeMethods.is_exists(method)):
            if isinstance(target, Node):
                return Validation.validate_node(method, target, *args)
            return Validation.validate_container_node(method, target, *args)
        elif Validation.NodeMethods.is_exists(method):
            return Validation.validate_node(method, target, *args)
        elif Validation.ContainerNodeMethods.is_exists(method):
            return Validation.validate_container_node(method, target, *args)
        return False    



class StructNode:
    valid_tests = {}
    
    def __init__(self, name: str, parent=Union[None,'StructNode']):
        self.name = name;
        self.level = 
        self.pos = pos;
        self.parent = parent;
        self.path = name

    def is_valid(self, method, *args):
        if method not in self.valid_tests:
            return False
        return self.valid_tests[method](self, *args)

    def has_parent(self):
        return self.parent is not None
    
        return self.level == 0

    def is_exists(self):
        if self.parent is None and (self.pos < 0 or self.level < 0):
            return False 
        return True
    
    def assemble_path(self):
        if self.is_exists():
            return self.name
        if self.is_root():
            return self.name
        if self.parent:
            return self.parent.assemble_path() + "/" + self.name
        return self.name

    def __str__(self):
        return f"{'Directory' if isinstance(self, ContainerNode) else 'File'}: {self.name} (Level: {self.level}, Parent: {self.parent.name if self.parent else 'None'})"

    def to_string(self, indent=''):
        return f"{indent}{self.name}\n"

    def to_detailed_string(self, indent='', is_last=True):
        connector = '└── ' if is_last else '├── '
        details = f"{indent}{connector}{self.pos}. {self.name} {'(Leaf)' if is_last else ''} \n"
        return details



class Node(StructNode):

    def __init__(self, name:str, parent:Union[None, 'ContainerNode']=None):
        super().__init__(name, level, pos, parent)
        assert isinstance(self.parent, ContainerNode)
        self.children: List[Union['Node', 'ContainerNode']]= []
        self.is_container = False
        if parent:
            parent.append(self)
            self.parent: ContainerNode = parent
        self.reload()

    def is_last(self):
        if self.parent:
            return self.parent.is_last(self)

    def move(self, new_parent:Union[None, 'ContainerNode']):
        if self.parent:
            assert isinstance(self.parent, ContainerNode)
            self.parent.remove(self)
        new_parent.append(self)        
        self.reload()

    def reload(self):
        if self.parent:
            self.pos = self.parent.pos_of(self)
            self.level = self.parent.level + 1
            self.path = self.parent.assemble_path()
        else:
            self.pos = 0
            self.level = 0
            self.path = self.name

    def __str__(self):
        return f"File: {self.name} (Level: {self.level}, Position: {self.pos}, Is Last: {self.is_last})"
    


class ContainerNode(Node):

    def __init__(self, name: str, parent:Union[None, 'ContainerNode']=None):
        super().__init__(name, parent)
        self.children: List[Union['Node', 'ContainerNode']]= []
        self.is_container = True
        if (parent):
            parent.append(self)
            self.parent: ContainerNode = parent
        self.reload()

    def get_max_depth(self, depth:int=0)->int:
        for child in self.children:
            if child.is_container:
                depth = max(depth, child.get_max_depth(depth + 1))            

    def contains(self, node:Union['Node', 'ContainerNode', str]):
        if isinstance(node, str):
            return node in [child.name for child in self.children]
        return node.name in [child.name for child in self.children]
    
    def is_empty(self):
        return len(self.children) > 0
    
    def count(self):
        return len(self.children)
    
    def get(self, name:str):
        if self.contains(name):
            return [child for child in self.children if child.name == name][0]
        return None

    def find(self, index:int):
        if index < 0 or index >= len(self.children):
            return None
        return self.children[index]

    def pos_of(self, node:Union['Node', 'ContainerNode', str])->int:
        if not self.contains(node):
            return -10
        if isinstance(node, str):
            for idx, child in enumerate(self.children):
                if child.name == node:
                    return idx + 1
        else:
            for idx, child in enumerate(self.children):
                if child.name == node.name:
                    return idx + 1
        return -5
    
    def last(self):
        return self.children[len(self.children) - 1]

    def islast(self, node:Union['Node', 'ContainerNode', str])->bool:
        if not self.contains(node):
            return False
        if isinstance(node, str):
            return self.children[len(self.children) - 1].name == node
        return self.children[len(self.children) - 1].name == node.name

    def append(self, node:Union['Node', 'ContainerNode']):
        if not self.is_valid("append", node):
            return
        self.children.append(node)
        node.parent = self
        node.reload()

    def remove(self, node:Union['Node', 'ContainerNode']):
        if not self.is_valid("remove", node):
            return
        self.children.remove(node)
        node.parent = None
        node.reload()
        self.reload_direct_children()

    def move(self, new_parent:Union[None, 'ContainerNode']):
        if self.parent:
            self.parent.remove(self)
        new_parent.append(self)

    def reload_all(self):
        self.reload()
        self.reload_children()

    def reload(self):
        if self.parent:
            assert isinstance(self.parent, ContainerNode)
            self.pos = self.parent.pos_of(self.name)
            self.level = self.parent.level + 1
            self.path = self.parent.assemble_path()
        else:
            self.pos = 0
            self.level = 0
            self.path = self.name
            
    def reload_children(self):
        for idx, child in enumerate(self.children):
            child.reload()

    def reload_direct_children(self):
        for idx, child in enumerate(self.children):
            if not child.is_container:
                child.reload()

    def __str__(self):
        return f"Directory: {self.name} (Level: {self.level}, Position: {self.pos}, Is Last: {self.is_last()})"
    
    def to_detailed_string(self, indent='', is_last=True):
        connector = '└── ' if is_last else '├── '
        child_indent = indent + ('    ' if is_last else '│   ') 
        head_text = '\n'
        head_text += PrinterHelper.add_style(f"{indent}{connector}" f"{self.pos}. {self.name}", [PrinterHelper.Formats.BOLD, PrinterHelper.Colors.CYAN])
        head_text += PrinterHelper.add_style((" (Leaf)" if is_last else ""), PrinterHelper.Colors.BLUE)
        details = [
            child_indent + head_text,
            child_indent + PrinterHelper.add_style(f"  ~ Path: {self.assemble_path()}", PrinterHelper.Colors.GRAY),
            child_indent + PrinterHelper.add_style(f"  ~ Path: {self.assemble_path()}", PrinterHelper.Colors.GRAY),
            child_indent + PrinterHelper.add_style(f"  ~ Level: {self.level}", PrinterHelper.Colors.GRAY),
            child_indent + PrinterHelper.add_style(f"  ~ Children: {self.count() if self.is_empty() else 'None'}", PrinterHelper.Colors.GRAY),
        ]
        result = ("\n").join(details) + "\n"
        if self.is_empty():
            for index, child in enumerate(self.children):
                is_last_child = index == len(self.children) - 1
                if child.is_last:
                    result += child_indent + '│    \n'
                result += child.to_detailed_string(child_indent, is_last_child)
        else:
            if is_last:
                result += child_indent + '    \n'
            else:
                result += child_indent + '│    \n'
        return result 


class Tree:
    def __init__(self, base_dir:ContainerNode):
        self.base_dir = base_dir

    def append(self, node: Union['Node', 'ContainerNode']):
        node.parent = self.base_dir
        node.level = self.base_dir.level + 1
        self.base_dir.children.append(node)

    def print_tree(self, node: Union['Node', 'ContainerNode'], indent=""):
        tree_str = indent + str(node) + "\n"
        if node.is_container:
            for child in node.children:
                tree_str += self.print_tree(child, indent + "    ")
        return tree_str
    
    def to_detailed_string(self):
        return self.base_dir.to_detailed_string()

    def __str__(self):
        return self.print_tree(self.base_dir)
    


class TreeData:
    def __init__(self, tree:Tree):
        self.tree = tree
        self.matrix = []
        self.build_matrix()

    def build_matrix(self):
        self.matrix = []
        self.add_to_matrix(self.tree.base_dir, 0, 0)

    def add_to_matrix(self, node:Union['Node', 'ContainerNode'], row:int, col:int):
        while len(self.matrix) <= row:
            self.matrix.append([])
        while len(self.matrix[row]) <= col:
            self.matrix[row].append(None)
        self.matrix[row][col] = node
        if isinstance(node, ContainerNode) and node.is_empty():
            for idx, child in enumerate(node.children):
                self.add_to_matrix(child, row + idx + 1, col + 1)

    def print_matrix(self):
        for row in self.matrix:
            for node in row:
                assert isinstance(node, Node) or isinstance(node, ContainerNode)
                print (node.name if node else None)                 
