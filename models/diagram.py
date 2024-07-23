import os
import shutil
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils
from models.abstractGenerator import AbstarctGenerator
from typing import Union, List, Iterable, Dict
from models.tree import ContainerNode, Node, Tree



class TreeDraw:
    def __init__(self, base_dir: Union['None', 'Tree']):
        pass
    
    def draw(self):
        return self.root.to_detailed_string()
    
    def get_child_is_last(self, name: str):
        return self.root.get_child_is_last(name)
    
    def get_child(self, name: str):
        return self.root.get_child(name)
    
    def get_full_path(self, name: str):
        return self.root.get_full_path(name)
    
    def get_parent(self, name: str):
        return self.root.get_parent(name)
    
    def get_root(self):
        return self.root 