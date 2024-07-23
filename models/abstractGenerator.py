import os
import argparse
import logging
import pathlib
from abc import ABC, abstractmethod
from utils.helpers import CLIUtils, PathUtils 
import models.abstractGenerator as abstractGenerator



class AbstarctGenerator(ABC):        
    
    @staticmethod
    @abstractmethod
    def source_tests(source):
        """
        Get source folder tests.
        """
        pass

    @staticmethod
    @abstractmethod
    def dist_tests(dist):
        """
        Get destination folder tests.
        """
        pass

    @staticmethod
    @abstractmethod
    def is_dist_valid(dist):
        """
        Get destination folder tests results. 
        """

    @staticmethod
    @abstractmethod
    def is_source_valid(source):
        """
        Get source folder tests results. 
        """

    @staticmethod
    @abstractmethod
    def check_source(source):
        """
        Check source folder.
        """
        pass

    @staticmethod
    @abstractmethod
    def check_dist(dist):
        """
        Check destination folder.
        """
        pass

    @staticmethod
    @abstractmethod
    def handle_request(args):
        """
        Handle request data.
        """
        pass

    @staticmethod
    @abstractmethod
    def handle_response(results):
        """
        Handle response data.
        """
        pass

    @staticmethod
    @abstractmethod
    def handle_generate(request_data):
        """
        Handle generate data.
        """

    @staticmethod
    def generate(request_data):
        """
        Generate output based on the source, destination, and options.
        """
        pass 

    @staticmethod
    @abstractmethod
    def parse_arguments(parser):
        pass