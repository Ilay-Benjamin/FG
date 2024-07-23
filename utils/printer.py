import os
import argparse
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Literal, Dict
from enum import Enum




class PrinterData:

    class AllowedColors(Enum):
        RED = 'red',
        GREEN = 'green',
        YELLOW = 'yellow',
        BLUE = 'blue',
        PURPLE = 'purple',
        CYAN = 'cyan',
        WHITE = 'white',
        BLACK = 'black',
        GRAY = 'gray',
        END = 'end'

        @staticmethod
        def __values():
            values = {
                PrinterData.Colors.RED: '\033[91m',
                PrinterData.Colors.GREEN: '\033[92m',
                PrinterData.Colors.YELLOW: '\033[93m',
                PrinterData.Colors.BLUE: '\033[94m',
                PrinterData.Colors.PURPLE: '\033[95m',
                PrinterData.Colors.CYAN: '\033[96m',
                PrinterData.Colors.WHITE: '\033[97m',
                PrinterData.Colors.BLACK: '\033[30m',
                PrinterData.Colors.GRAY: '\033[90m',
                PrinterData.Colors.END: '\033[0m',
            }
            return values
        
        @staticmethod
        def get(color:Literal['PrinterData.Colors']):
                return PrinterData.AllowedColors.__values()[color]
        
        @staticmethod
        def is_exists(color: 'PrinterData.Colors'):
            return color in PrinterData.AllowedColors.__values()
        
        @staticmethod
        def get_all():
            return PrinterData.AllowedColors.__values()
        
    class AllowedFormats(Enum):
        BOLD = 'bold',
        UNDERLINE = 'underline',
        ITALIC = 'italic',
        END = 'end'
        
        @staticmethod
        def __values(): 
            values = {
                PrinterData.Formats.BOLD: '\033[1m',
                PrinterData.Formats.UNDERLINE: '\033[4m',
                PrinterData.Formats.ITALIC: '\033[3m',
                PrinterData.Formats.END: '\033[0m',
            }
            return values
        
        @staticmethod
        def get(format:Literal['PrinterData.Formats']):
            return PrinterData.AllowedFormats.__values()[format]
        
        @staticmethod
        def is_exists(format: 'PrinterData.Formats'):
            return format in PrinterData.AllowedFormats.__values()
        
        @staticmethod
        def get_all():
            return PrinterData.AllowedFormats.__values()

    Colors = AllowedColors
    Formats = AllowedFormats



class PrinterHelper:

    Colors = PrinterData.Colors
    Formats = PrinterData.Formats    


    
    @staticmethod
    def add_color(text:str, color:Union[PrinterData.Colors, List[PrinterData.Colors]]):
        return PrinterHelper.__add_to_text(text, [color] if not isinstance(color, list) else color)

    @staticmethod
    def add_format(text:str, format:Union[PrinterData.Formats, List[PrinterData.Formats]]):
        return PrinterHelper.__add_to_text(text, [format] if not isinstance(format, list) else format)
    
    @staticmethod
    def add_style(text:str, style:Union[PrinterData.Formats, List[PrinterData.Formats], PrinterData.Colors, List[PrinterData.Colors], List[Union[PrinterData.Colors, PrinterData.Formats]]]):
        return PrinterHelper.__add_to_text(text, [style] if not isinstance(style, list) else style)

    @staticmethod
    def __add_to_text(text: str, additions: List[Union['PrinterData.Colors', 'PrinterData.Formats']]):
        if len(additions) == 0:
            return text
        end_text = PrinterHelper.Colors.get(PrinterData.Colors.END) * (len(additions))
        new_text = ''
        for addition in additions:
            if PrinterData.Colors.is_exists(addition):
                new_text += PrinterHelper.Colors.get(addition)
            else:
                new_text += PrinterHelper.Formats.get(addition)
        new_text += text + end_text
        return new_text
        
