import os
import argparse
import logging
from pathlib import Path


cli_commands = [
    "init",
    "build",
    "draw",
    "create",
    "remove",
    "help"
]

cli_commands_args = {
    "init": ["--path"],
    "build": ["--source", "--dist"],
    "draw": ["--source", "--dist", "--method"],
    "create": ["--path"],
    "remove": ["--path"],
    "help": []
}