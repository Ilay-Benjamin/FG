import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from utils.printer import PrinterHelper, PrinterData
from models.abstractGenerator import AbstarctGenerator
from models.tree2 import ContainerNode, Node, Tree
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
    def validate_node(method:Literal['Validation.NodeMethods'], target:Node, *args) -> bool:
        return Validation.AllowedNodeMethods.__methods()[method](target, *args)

    @staticmethod
    def validate_container_node(method:Literal['Validation.ContainerNodeMethods'], target:ContainerNode, *args) -> bool:
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