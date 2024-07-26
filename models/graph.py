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
import matplotlib.pyplot as plt
import networkx as nx



def get_positions(node: ContainerNode) -> dict[str, tuple[int, int]]:

    def build_positions(node: Union[ContainerNode, Node], x: int, y: int, positions: dict[str, tuple[int, int]]):
        if isinstance(node, ContainerNode):
            positions[node.name] = (x, y)
            for child in node.children:
                build_positions(child, child.level, child.id, positions)
        else:
            positions[node.name] = (x, y)

    positions = {}
    build_positions(node, 0, 0, positions)
    return positions



def get_edges(node: ContainerNode) -> list[tuple[str, str]]:

    def build_edges(node: Union[ContainerNode, Node], edges: list[tuple[str, str]]):
        if isinstance(node, ContainerNode):
            for child in node.children:
                edges.append((node.name, child.name))
                build_edges(child, edges)

    edges = []
    build_edges(node, edges)
    return edges





def draw_graph(tree: Tree):
    
        base_dir = tree.base_dir
    
        positions = get_positions(base_dir)
        edges = get_edges(base_dir)

        G = nx.DiGraph()

        for node, position in positions.items():
            G.add_node(node, pos=position)
        
        for edge in edges:
            G.add_edge(edge[0], edge[1])

        pos = nx.get_node_attributes(G, 'pos')

        nx.draw(G, pos, with_labels=True, arrows=True)
        plt.title("File System Tree as a 2D Graph")
        plt.xlabel("X-axis (Horizontal Position)")
        plt.ylabel("Y-axis (Vertical Position)")
        plt.show()





# Create a directed graph
G = nx.DiGraph()

# Define positions for each node with unique X coordinates
positions = {
    "/": (0, 0),
    "home": (1, 1),
    "user": (2, 2),
    "documents": (3, 3),
    "file.txt": (4, 4),
    "pictures": (5, 3),
    "etc": (6, 1),
    "config": (7, 2),
    "network": (8, 2)
}

# Define edges for the graph
edges = [
    ("/", "home"),
    ("/", "etc"),
    ("home", "user"),
    ("user", "documents"),
    ("documents", "file.txt"),
    ("user", "pictures"),
    ("etc", "config"),
    ("etc", "network")
]

