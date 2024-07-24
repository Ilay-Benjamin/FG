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



# <--------------------------- NodeRegistry ---------------------------->  
# <--------------------------- NodeRegistry ---------------------------->  


class NodeRegistry:
    __nodes__: List[Union['Node', 'ContainerNode']]= []

    @staticmethod
    def register(node:Union['Node', 'ContainerNode']):
        NodeRegistry.__nodes__.append(node)
        return len(NodeRegistry.__nodes__) - 1

    @staticmethod
    def get(name:str)->Union[None, 'Node', 'ContainerNode']:
        for node in NodeRegistry.__nodes__:
            assert isinstance(node, Node) or isinstance(node, ContainerNode)
            if node.name == name:
                return node
        return None
    
    @staticmethod
    def find(name:str)->Union[None, 'Node', 'ContainerNode']:
        for node in NodeRegistry.__nodes__:
            assert isinstance(node, Node) or isinstance(node, ContainerNode)
            if node.name == name:
                return node
        return None

    @staticmethod
    def get_all():
        return NodeRegistry.__nodes__
    
    @staticmethod
    def count():
        return len(NodeRegistry.__nodes__)
    
    @staticmethod
    def contains(node:Union['Node', 'ContainerNode', str]):
        if isinstance(node, str):
            return node in [child.name for child in NodeRegistry.__nodes__]
        return node.name in [child.name for child in NodeRegistry.__nodes__]
    
    @staticmethod
    def is_empty():
        return len(NodeRegistry.__nodes__) > 0
    
    @staticmethod
    def get_max_depth():
        depth = 0
        for node in NodeRegistry.__nodes__:
            if node.is_container():
                depth = max(depth, node.get_max_depth())
        return depth
    


# <--------------------------- NodeInterface ---------------------------->
# <--------------------------- NodeInterface ---------------------------->

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



# <--------------------------- StructNode ---------------------------->
# <--------------------------- StructNode ---------------------------->

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



# <--------------------------- BasicNode ---------------------------->
# <--------------------------- BasicNode ---------------------------->

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
    


# <--------------------------- Node ---------------------------->
# <--------------------------- Node ---------------------------->

class Node(BasicNode):

    @staticmethod
    def capable() -> bool:
        return False
    
    def is_container(self) -> bool:
        return Node.capable()

    def __init__(self, name:str, parent:Union[None, 'ContainerNode']=None):
        super().__init__(name, parent)
        self.parent: Union[None, 'ContainerNode'] = parent
        self._load(parent)
        self.id = NodeRegistry.register(self)

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
        return f"File: (ID={self.id}) {self.name} (Level: {self.level}, Position: {self.pos}, Is Last: {self.is_last()})"

    def to_detailed_string(self, indent='', is_last=True):
        connector = '└── ' if is_last else '├── '
        details = f"{indent}{connector}{self.pos}. {self.name} {'(Leaf)' if is_last else ''} \n"
        return details

    def to_structure_string(self, indent='', is_last=True):
        connector = '└── ' if is_last else '├── '
        details = f"{indent}{connector}{self.pos}. {self.name}"
        is_last_text = f"{'(Leaf)' if is_last else ''} \n"
        details += PrinterHelper.add_style(is_last_text, PrinterHelper.Colors.ORANGE)
        return details + (indent + '\n'  if is_last else "") 



# <--------------------------- ContainerNode ---------------------------->                                                                      
# <--------------------------- ContainerNode ---------------------------->                                                                      

class ContainerNode(BasicNode):
    """
    Represents a container node in a tree structure.
    """

    @staticmethod
    def capable() -> bool:
        """
        Returns whether the container is capable or not.
        """
        return True
    
    def is_container(self) -> bool:
        """
        Checks if the node is a container.
        """
        return ContainerNode.capable()
    
    @staticmethod
    def _load_root(root: 'ContainerNode'):
        """
        Loads the root node of the container.
        """
        StructNode._load_root(root)
        root.children = []

    @staticmethod
    def _create_root(name: str) -> 'ContainerNode':
        """
        Creates a new root node for the container.
        """
        root = ContainerNode(name)
        ContainerNode._load_root(root)
        return root

    def __init__(self, name: str, parent:Union[None, 'ContainerNode']=None):
        """
        Initializes a new instance of the ContainerNode class.
        """
        self.children: List[Union['Node', 'ContainerNode']] = []
        super().__init__(name, parent)
        self._load(parent)
        self.id = NodeRegistry.register(self)

    def _load(self, parent:Union[None, 'ContainerNode']):
        """
        Loads the container node with the specified parent.
        """
        if parent:
            self.move(parent)
        else:
            self.parent = None
            self.path = self.name
            self.level = -1
            self.pos = -1

    def move(self, new_parent:Union[None, 'ContainerNode']):
        """
        Moves the container node to a new parent.
        """
        if self.parent:
            assert isinstance(self.parent, ContainerNode)
            self.parent.remove(self)
        new_parent.append(self)
        for child in self.children:
            child.reload_all()

    def get_max_depth(self, depth:int=0)->int:
        """
        Returns the maximum depth of the container node.
        """
        for child in self.children:
            print(child.name + " " + str(child.is_container()))
            if isinstance(child, ContainerNode):
                depth = max(depth, child.get_max_depth(depth + 1))            

    def contains(self, node:Union['Node', 'ContainerNode', str]):
        """
        Checks if the container node contains the specified node.
        """
        if isinstance(node, str):
            return node in [child.name for child in self.children]
        return node.name in [child.name for child in self.children]
    
    def is_empty(self):
        """
        Checks if the container node is empty.
        """
        return len(self.children) < 0
    
    def count(self, deep_search=False):
        """
        Returns the number of children in the container node.
        """
        if deep_search:
            count = 0
            for child in self.children:
                count += 1
                if child.is_container():
                    count += child.count(True)
            return count
        return len(self.children)
    
    def get(self, name:str):
        """
        Returns the child node with the specified name.
        """
        if self.contains(name):
            return [child for child in self.children if child.name == name][0]
        return None

    def find(self, index:int):
        """
        Finds the child node at the specified index.
        """
        if index < 0 or index >= len(self.children):
            return None
        return self.children[index]

    def pos_of(self, node:Union['Node', 'ContainerNode', str])->int:
        """
        Returns the position of the specified node in the container.
        """
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
        """
        Returns the last child node in the container.
        """
        return self.children[len(self.children) - 1]
    
    def check_last(self, node:Union['Node', 'ContainerNode', str]):
        """
        Checks if the specified node is the last child in the container.
        """
        if not self.contains(node):
            return False
        if isinstance(node, str):
            return self.children[len(self.children) - 1].name == node
        return self.children[len(self.children) - 1].name == node.name

    def is_last(self) -> bool:
        """
        Checks if the container node is the last child of its parent.
        """
        if self.parent:
            return self.parent.last() == self
        
    

    def append(self, node:Union['Node', 'ContainerNode']):
        """
        Appends a child node to the container.
        """
        self.children.append(node)
        node.parent = self
        self.reload_all()


    def remove(self, node:Union['Node', 'ContainerNode']):
        """
        Removes a child node from the container.
        """
        self.children.remove(node)
        node.parent = None
        node.reload()
        self.reload_all()

    def reload(self):
        """
        Reloads the container node.
        """
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
        """
        Reloads the children of the container node.
        """
        if only_direct:
            for idx, child in enumerate(self.children):
                child.reload()
        else:
            for idx, child in enumerate(self.children):
                child.reload()
                if isinstance(child, ContainerNode):
                    child.reload_children()
    
    def reload_all(self):
        """
        Reloads the container node and its children.
        """
        self.reload()
        self.reload_children()


    def __str__(self):
        """
        Returns a string representation of the container node.
        """
        return f"Directory: (ID={self.id}) {self.name} (Level: {self.level}, Position: {self.pos}, Is Last: {self.parent.is_last(self) if self.parent else 'None'})"

    def to_structure_string(self, indent='', is_last=True):
        """
        Returns a string representation of the container node.
        """
        connector = '└── ' if is_last else '├── '
        child_indent = indent + ('    ' if is_last else '│   ') 
        result = PrinterHelper.add_style(f"{indent}{connector}" 
                                        f"{self.pos}. {self.name}/", 
                                        [PrinterHelper.Formats.BOLD, 
                                        PrinterHelper.Colors.CYAN])
        result += PrinterHelper.add_style((" (Leaf)" if is_last else ""), 
                                        PrinterHelper.Colors.ORANGE) + '\n' + child_indent + '│   ' + '\n' 
        if not self.is_empty():
            for index, child in enumerate(self.children):
                is_last_child = index == len(self.children) - 1
                result += child.to_structure_string(child_indent, is_last_child)
        else:
            if is_last:
                result += child_indent + '    \n'
            else:
                result += child_indent + '│   \n'
        return result

    def to_detailed_string(self, indent='', is_last=True, ):
        """
        Returns a detailed string representation of the container node.
        """
        connector = '└── ' if is_last else '├── '
        child_indent = indent + ('    ' if is_last else '│   ') 
        head_text = '\n'
        head_text += PrinterHelper.add_style(f"{indent}{connector}" f"{self.pos}. {self.name}", [PrinterHelper.Formats.BOLD, PrinterHelper.Colors.CYAN])
        head_text += PrinterHelper.add_style((" (Leaf)" if is_last else ""), PrinterHelper.Colors.BLUE)
        details = []
        details = [
            child_indent + head_text,
            child_indent + PrinterHelper.add_style(f"  ~ Path: {self.path}", PrinterHelper.Colors.GRAY),
            child_indent + PrinterHelper.add_style(f"  ~ Path: {self.path}", PrinterHelper.Colors.GRAY),
            child_indent + PrinterHelper.add_style(f"  ~ Level: {self.level}", PrinterHelper.Colors.GRAY),
            child_indent + PrinterHelper.add_style(f"  ~ Children: {self.count() if self.is_empty() else 'None'}", PrinterHelper.Colors.GRAY),
        ]
        result = ("\n").join(details) + "\n"
        if not self.is_empty():
            for index, child in enumerate(self.children):
                is_last_child = index == len(self.children) - 1
                if child.is_last():
                    result += child_indent + '│    \n'
                result += child.to_detailed_string(child_indent, is_last_child)
        else:
            if is_last:
                result += child_indent + '    \n'
            else:
                result += child_indent + '│    \n'
        return result




# <--------------------------- Tree ---------------------------->
# <--------------------------- Tree ---------------------------->

class Tree:
    def __init__(self, base_dir:ContainerNode):
        self.base_dir = base_dir

    def append(self, node: Union['Node', 'ContainerNode']):
        self.base_dir.children.append(node)

    def collect(self, level:int) -> List[Union['Node', 'ContainerNode']]:
        
        def collect_nodes(node, current_level):
            if current_level == level:
                level_nodes.append(node)
            if isinstance(node, ContainerNode):
                for child in node.children:
                    collect_nodes(child, current_level + 1)

        level_nodes = []
        collect_nodes(self.base_dir, 0)
        return level_nodes
        

    def print_tree(self, node: Union['Node', 'ContainerNode'], indent=""):
        tree_str = indent + str(node) + "\n"
        if isinstance(node, ContainerNode):
            for child in node.children:
                tree_str += self.print_tree(child, indent + "    ")
        return tree_str
    
    def to_detailed_string(self):
        return self.base_dir.to_detailed_string()

    def __str__(self):
        return self.print_tree(self.base_dir)
    


# <--------------------------- TreeData ---------------------------->
# <--------------------------- TreeData ---------------------------->

class TreeData:
    def __init__(self, tree:Tree):
        self.tree = tree
        self.matrix = []
        self.build_matrix()

    def build_matrix(self):
        self.matrix = []
        root = self.tree.base_dir
        max_depth = root.get_max_depth() + 1
        for level in range(max_depth):
            self.matrix.append([])
        self.add_to_matrix(root, 0)

    def add_to_matrix(self, node:Union['Node', 'ContainerNode'], level: int):
        self.matrix[level].append(node)
        if isinstance(node, ContainerNode):
            for child in node.children:
                self.add_to_matrix(child, level + 1)

    def print_matrix(self):
        for level, row in enumerate(self.matrix):
            print(f"Level {level}: ", end="")
            for node in row:
                if isinstance(node, Node):
                    print(node.name, end=" ")
                elif isinstance(node, ContainerNode):
                    print(node.name, end=" ")
            print()