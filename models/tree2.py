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



class NodeInterface(ABC):
    
    @staticmethod
    @abstractmethod
    def _load_root(root: 'NodeInterface'):
        pass

    @staticmethod
    @abstractmethod
    def _create_root(name: str) -> 'NodeInterface':
        pass

    @abstractmethod
    def reload(self):
        pass



class StructNode(NodeInterface):

    @staticmethod
    def _load_root(root: 'StructNode'):
        root.level = 0
        root.path = root.name
        root.parent = None

    @staticmethod
    def _create_root(name: str) -> 'StructNode':
        root = StructNode(name)
        StructNode._load_root(root)
        return root

    def __init__(self, name: str, parent=Union[None,'StructNode']):
        self.name = name;
        self.parent = None
        self._load(parent)        
    
    def _load(self, parent:Union[None,'StructNode']):
        if self.level == 0:
            return
        if parent:
            self.parent = parent
            self.level = parent.level + 1
            self.path = parent.path + "/" + self.name
        else:
            self.parent = None
            self.level = -1
            self.path = self.name

    def has_parent(self):
        return self.parent is not None
    
    def is_root(self):
        return self.level == 0
    
    def is_exists(self):
        return self.parent is not None and self.level >= 0

    def __str__(self):
        return f"{'Directory' if isinstance(self, ContainerNode) else 'File'}: {self.name} (Level: {self.level}, Parent: {self.parent.name if self.parent else 'None'})"

    def to_string(self, indent=''):
        return f"{indent}{self.name}\n"



class BasicNode(StructNode):

    @staticmethod
    def _load_root(root: 'BasicNode'):
        StructNode._load_root(root)
        root.pos = 0
    
    @staticmethod
    def _create_root(name: str) -> 'BasicNode':
        root = BasicNode(name)
        BasicNode._load_root(root)
        return root
    
    def __init__(self, name:str, parent:Union[None, 'BasicNode']):
        super().__init__(name, parent)
        self.pos = -1

    def __str__(self):
        return f"File: {self.name} (Level: {self.level}, Position: {self.pos})"
    
    def to_detailed_string(self, indent='', is_last=True):
        connector = '└── ' if is_last else '├── '
        details = f"{indent}{connector}{self.pos}. {self.name} {'(Leaf)' if is_last else ''} \n"
        return details
    
    def to_string(self, indent=''):
        return f"{indent}{self.name}\n"
    


class Node(BasicNode):

    @staticmethod
    @property
    def capable(self) -> bool:
        return False
    
    def is_container(self) -> bool:
        return Node.capable

    def __init__(self, name:str, parent:Union[None, 'ContainerNode']=None):
        super().__init__(name, parent)
        self.parent: Union[None, 'ContainerNode'] = parent
        self._load(parent)

    def _load(self, parent:Union[None, 'ContainerNode']):
        if parent:
            self.move(parent)
        else:
            self.parent = None
            self.path = self.name
            self.level = -1
            self.pos = -1

    def move(self, new_parent:Union[None, 'ContainerNode']):
        if self.parent:
            assert isinstance(self.parent, ContainerNode)
            self.parent.remove(self)
        new_parent.append(self)
        self.reload()

    def reload(self):
        if self.parent:
            self.parent: ContainerNode = self.parent
            self.path = self.parent.path + "/" + self.name
            self.level = self.parent.level + 1
            self.pos = self.parent.pos_of(self)
        else:
            self.parent = None
            self.path = self.name
            self.level = -1
            self.pos = -1

    def is_last(self):
        if self.parent:
            return self.parent.last() == self

    def __str__(self):
        return f"File: {self.name} (Level: {self.level}, Position: {self.pos}, Is Last: {self.is_last})"
    
    def to_detailed_string(self, indent='', is_last=True):
        connector = '└── ' if is_last else '├── '
        details = f"{indent}{connector}{self.pos}. {self.name} {'(Leaf)' if is_last else ''} \n"
        return details
    


class ContainerNode(BasicNode):
    
    @staticmethod
    @property
    def capable(self) -> bool:
        return True
    
    def is_container(self) -> bool:
        return ContainerNode.capable
    
    @staticmethod
    def _load_root(root: 'ContainerNode'):
        StructNode._load_root(root)
        root.children = []

    @staticmethod
    def _create_root(name: str) -> 'ContainerNode':
        root = ContainerNode(name)
        ContainerNode._load_root(root)
        return root

    def __init__(self, name: str, parent:Union[None, 'ContainerNode']=None):
        self.children: List[Union['Node', 'ContainerNode']] = []
        super().__init__(name, parent)
        self._load(parent)

    def _load(self, parent:Union[None, 'ContainerNode']):
        if parent:
            self.move(parent)
        else:
            self.parent = None
            self.path = self.name
            self.level = -1
            self.pos = -1

    def move(self, new_parent:Union[None, 'ContainerNode']):
        if self.parent:
            assert isinstance(self.parent, ContainerNode)
            self.parent.remove(self)
        new_parent.append(self)
        for child in self.children:
            child.reload_all()

    def get_max_depth(self, depth:int=0)->int:
        for child in self.children:
            if child.is_container():
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

    def is_last(self, node:Union['Node', 'ContainerNode', str])->bool:
        if not self.contains(node):
            return False
        if isinstance(node, str):
            return self.children[len(self.children) - 1].name == node
        return self.children[len(self.children) - 1].name == node.name

    def append(self, node:Union['Node', 'ContainerNode']):
        self.children.append(node)
        node.parent = self
        self.reload_all()

    def remove(self, node:Union['Node', 'ContainerNode']):
        self.children.remove(node)
        node.parent = None
        node.reload()
        self.reload_all()

    def reload(self):
        if self.parent:
            assert isinstance(self.parent, ContainerNode)
            self.parent: ContainerNode = self.parent
            self.path = self.parent.path + "/" + self.name
            self.level = self.parent.level + 1
            self.pos = self.parent.pos_of(self.name)
        else:
            self.parent = None
            self.path = self.name
            self.level = -1
            self.pos = -1
            
    def reload_children(self, only_direct=False):
        if only_direct:
            for idx, child in enumerate(self.children):
                child.reload()
        else:
            for idx, child in enumerate(self.children):
                child.reload()
                if isinstance(child, ContainerNode):
                    child.reload_children()
    
    def reload_all(self):
        self.reload()
        self.reload_children()

    def __str__(self):
        return f"Directory: {self.name} (Level: {self.level}, Position: {self.pos}, Is Last: {self.parent.is_last(self) if self.parent else 'None'})"
    
    def to_detailed_string(self, indent='', is_last=True):
        connector = '└── ' if is_last else '├── '
        child_indent = indent + ('    ' if is_last else '│   ') 
        head_text = '\n'
        head_text += PrinterHelper.add_style(f"{indent}{connector}" f"{self.pos}. {self.name}", [PrinterHelper.Formats.BOLD, PrinterHelper.Colors.CYAN])
        head_text += PrinterHelper.add_style((" (Leaf)" if is_last else ""), PrinterHelper.Colors.BLUE)
        details = [
            child_indent + head_text,
            child_indent + PrinterHelper.add_style(f"  ~ Path: {self.path}", PrinterHelper.Colors.GRAY),
            child_indent + PrinterHelper.add_style(f"  ~ Path: {self.path}", PrinterHelper.Colors.GRAY),
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
        if node.is_container():
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
