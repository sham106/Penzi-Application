"""
This module provides code for reading kenyans counties
from the provided kenyan_counties text file which is
included in this module.
"""


class ReadKenyanCounties:
    """
    This class includes all read operation for
    kenya counties from the kenya_counties.txt
    file
    """

    def __init__(self, file_name):
        self.file_name = file_name

    def read_all_counties(self):
        with open(self.file_name, 'r') as file:
            counties = [line.strip('\n') for line in file.readlines()]
           


        return counties


