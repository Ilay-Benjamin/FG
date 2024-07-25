import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from models.abstractGenerator import AbstarctGenerator
from models.tree2 import ContainerNode, Node, Tree, TreeData, NodeRegistry
from typing import Union, List, Iterable, Dict, Callable, Literal
from enum import Enum
from utils.printer import PrinterHelper, PrinterData



class TreePrinter:


# <--------------------------- PrinterTypes ---------------------------->                                                                      
# <--------------------------- PrinterTypes ---------------------------->                                                                      

    class PrinterTypes(Enum):
        NODE = 'node',
        Container = 'container',
    
        @staticmethod
        def is_exists(type: 'TreePrinter.Types'):
            return type in TreePrinter.Types.__members__


# <--------------------------- PrintFormats ---------------------------->                                                                      
# <--------------------------- PrintFormats ---------------------------->                                                                      

    class PrintFormats(Enum):
        STRUCTURE = 'structure',
        DETAILS = 'details',
        SUMMARY = 'summary',

        @staticmethod
        def is_exists(format: 'TreePrinter.Formats'):
            return format in TreePrinter.Formats.__members__


    Types = PrinterTypes
    Formats = PrintFormats


# <--------------------------- PrinterInterface ---------------------------->                                                                      
# <--------------------------- PrinterInterface ---------------------------->                                                                      

    class PrinterInterface(ABC):

        @staticmethod
        @abstractmethod
        def get_summary_text(node: Union['ContainerNode', 'Node']) -> str:
            pass

        @staticmethod
        @abstractmethod
        def print_summary(node: Union['ContainerNode', 'Node']):
            pass
        
        @staticmethod
        @abstractmethod
        def get_structure_text(node: Union['ContainerNode', 'Node']) -> str:
            pass

        @staticmethod
        @abstractmethod
        def print_structure(node: Union['ContainerNode', 'Node']):
            pass

        @staticmethod
        @abstractmethod
        def print_detailed(node: Union['ContainerNode', 'Node']):
            pass

        @staticmethod
        @abstractmethod
        def get_detailed_text(node: Union['ContainerNode', 'Node']) -> str:
            pass

        @staticmethod
        @abstractmethod
        def get_type() -> 'TreePrinter.Types':
            pass


# <--------------------------- ContainerPrinter ---------------------------->                                                                      
# <--------------------------- ContainerPrinter ---------------------------->                                                                      

    class ContainerPrinter(PrinterInterface):
        @staticmethod
        def get_type() -> 'TreePrinter.Types':
            return TreePrinter.Types.Container
        
        @staticmethod
        def get_summary_text(node: ContainerNode) -> str:
            assert isinstance(node, ContainerNode)
            return TreePrinter.ContainerPrinter.generate_summary_text(node)
        
        @staticmethod
        def print_summary(node: ContainerNode):
            assert isinstance(node, ContainerNode)
            print(TreePrinter.ContainerPrinter.get_summary_text(node))

        @staticmethod
        def generate_summary_text(target: ContainerNode) -> str:
            assert isinstance(target, ContainerNode)
            return f"Container: (ID={target.id}) {target.name} (Level: {target.level}, Position: {target.pos}, Is Last: {target.is_last()}"

        @staticmethod
        def get_structure_text(node: ContainerNode) -> str:
            assert isinstance(node, ContainerNode)
            return TreePrinter.ContainerPrinter.generate_structure_text(node)

        @staticmethod    
        def print_structure(node: ContainerNode):
            assert isinstance(node, ContainerNode)
            print(TreePrinter.ContainerPrinter.get_structure_text(node))

        @staticmethod
        def generate_structure_text(target: ContainerNode, indent='', is_last=True):
            connector = '└── ' if is_last else '├── '
            child_indent = indent + ('    ' if is_last else '│   ') 
            result = PrinterHelper.add_style(f"{indent}{connector}" 
                                            f"{target.pos}. {target.name}/", 
                                            [PrinterHelper.Formats.BOLD, 
                                            PrinterHelper.Colors.CYAN])
            result += PrinterHelper.add_style((" (Leaf)" if is_last else ""), 
                                            PrinterHelper.Colors.ORANGE) + '\n' + child_indent + '│   ' + '\n' 
            if not target.is_empty():
                for index, child in enumerate(target.children):
                    is_last_child = index == len(target.children) - 1
                    generator = TreePrinter.NodePrinter.generate_structure_text if isinstance(child, Node) else TreePrinter.ContainerPrinter.generate_structure_text
                    result += generator(child, child_indent, is_last_child)
            else:
                if is_last:
                    result += child_indent + '    \n'
                else:
                    result += child_indent + '│   \n'
            return result

        @staticmethod
        def get_detailed_text(node: ContainerNode) -> str:
            assert isinstance(node, ContainerNode)
            return TreePrinter.ContainerPrinter.generate_detailed_text(node)

        @staticmethod    
        def print_detailed(node: ContainerNode):
            assert isinstance(node, ContainerNode)
            print(TreePrinter.ContainerPrinter.get_detailed_text(node))

        @staticmethod
        def generate_detailed_text(target: ContainerNode, indent='', is_last=True):
            connector = '└── ' if is_last else '├── '
            child_indent = indent + ('    ' if is_last else '│   ') 
            head_text = '\n'
            head_text += PrinterHelper.add_style(f"{indent}{connector}" f"{target.pos}. {target.name}", [PrinterHelper.Formats.BOLD, PrinterHelper.Colors.CYAN])
            head_text += PrinterHelper.add_style((" (Leaf)" if is_last else ""), PrinterHelper.Colors.BLUE)
            details = []
            details = [
                child_indent + head_text,
                child_indent + PrinterHelper.add_style(f"  ~ Path: {target.path}", PrinterHelper.Colors.GRAY),
                child_indent + PrinterHelper.add_style(f"  ~ Path: {target.path}", PrinterHelper.Colors.GRAY),
                child_indent + PrinterHelper.add_style(f"  ~ Level: {target.level}", PrinterHelper.Colors.GRAY),
                child_indent + PrinterHelper.add_style(f"  ~ Children: {target.count() if target.is_empty() else 'None'}", PrinterHelper.Colors.GRAY),
            ]
            result = ("\n").join(details) + "\n"
            if not target.is_empty():
                for index, child in enumerate(target.children):
                    is_last_child = index == len(target.children) - 1
                    if child.is_last():
                        result += child_indent + '│    \n'
                    generator = TreePrinter.NodePrinter.generate_detailed_text if isinstance(child, Node) else TreePrinter.ContainerPrinter.generate_detailed_text
                    result += generator(child, child_indent, is_last_child)
                    result += TreePrinter.ContainerPrinter.generate_detailed_text(child, child_indent, is_last_child)
            else:
                if is_last:
                    result += child_indent + '    \n'
                else:
                    result += child_indent + '│    \n'
            return result


# <--------------------------- NodePrinter ---------------------------->                                                                      
# <--------------------------- NodePrinter ---------------------------->                                                                      

    class NodePrinter(PrinterInterface):
        @staticmethod
        def get_type() -> 'TreePrinter.Types':
            return TreePrinter.Types.NODE
        
        @staticmethod
        def get_summary_text(node: Node) -> str:
            assert isinstance(node, Node)
            return TreePrinter.NodePrinter.generate_summary_text(node)
        
        @staticmethod
        def print_summary(node: Node):
            assert isinstance(node, Node)
            print(TreePrinter.NodePrinter.get_summary_text(node))

        @staticmethod
        def generate_summary_text(target: Node) -> str:
            assert isinstance(target, Node)
            return f"Node: (ID={target.name})AEDFG {target.name} (Level: {target.level}, Position: {target.pos}, Is Last: {target.is_last()}"
        
        @staticmethod
        def get_structure_text(node: Node) -> str:
            assert isinstance(node, Node)
            return TreePrinter.NodePrinter.generate_structure_text(node)
        
        @staticmethod
        def print_structure(node: Node):
            assert isinstance(node, Node)
            print(TreePrinter.NodePrinter.get_structure_text(node))

        @staticmethod
        def generate_structure_text(target: Node, indent='', is_last=True):
            connector = '└── ' if is_last else '├── '
            details = f"{indent}{connector}{target.pos}. {target.name}"
            is_last_text = f"{' (Leaf)' if is_last else ''} \n"
            details += PrinterHelper.add_style(is_last_text, PrinterHelper.Colors.ORANGE)
            return details + (indent + '\n'  if is_last else "") 
        
        @staticmethod
        def get_detailed_text(node: Node) -> str:
            return TreePrinter.NodePrinter.generate_detailed_text(node)
        
        @staticmethod
        def print_detailed(node: Node):
            print(TreePrinter.NodePrinter.get_detailed_text(node))

        @staticmethod
        def generate_detailed_text(target: Node, indent='', is_last=True):
            connector = '└── ' if is_last else '├── '
            details = f"{indent}{connector}{target.pos}. {target.name} {'(Leaf)' if is_last else ''} \n"
            return details
    
    @staticmethod
    def print_structure(node: Union['ContainerNode', 'Node']):
        assert isinstance(node, (ContainerNode, Node))
        if isinstance(node, ContainerNode):
            TreePrinter.ContainerPrinter.print_structure(node)
        else:
            TreePrinter.NodePrinter.print_structure(node)

    @staticmethod
    def print_detailed(node: Union['ContainerNode', 'Node']):
        assert isinstance(node, (ContainerNode, Node))
        if isinstance(node, ContainerNode):
            TreePrinter.ContainerPrinter.print_detailed(node)
        else:
            TreePrinter.NodePrinter.print_detailed(node)

    @staticmethod
    def print_summary(node: Union['ContainerNode', 'Node']):
        assert isinstance(node, (ContainerNode, Node))
        if isinstance(node, ContainerNode):
            TreePrinter.ContainerPrinter.print_summary(node)
        else:
            TreePrinter.NodePrinter.print_summary(node)

    @staticmethod
    def get_structure_text(node: Union['ContainerNode', 'Node']) -> str:
        assert isinstance(node, (ContainerNode, Node))
        if isinstance(node, ContainerNode):
            return TreePrinter.ContainerPrinter.get_structure_text(node)
        else:
            return TreePrinter.NodePrinter.get_structure_text(node)
        
    @staticmethod
    def get_detailed_text(node: Union['ContainerNode', 'Node']) -> str:
        assert isinstance(node, (ContainerNode, Node))
        if isinstance(node, ContainerNode):
            return TreePrinter.ContainerPrinter.get_detailed_text(node)
        else:
            return TreePrinter.NodePrinter.get_detailed_text(node)
        
    @staticmethod
    def get_summary_text(node: Union['ContainerNode', 'Node']) -> str:
        assert isinstance(node, (ContainerNode, Node))
        if isinstance(node, ContainerNode):
            return TreePrinter.ContainerPrinter.get_summary_text(node)
        else:
            return TreePrinter.NodePrinter.get_summary_text(node)

    @staticmethod
    def print(node: Union['ContainerNode', 'Node'], format: Literal['TreePrinter.Formats']):
        if format == TreePrinter.Formats.STRUCTURE:
            TreePrinter.print_structure(node)
        elif format == TreePrinter.Formats.DETAILS:
            TreePrinter.print_detailed(node)
        else:
            TreePrinter.print_summary(node)
