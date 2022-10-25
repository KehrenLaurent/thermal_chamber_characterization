'''
This module define classes for analyse data according to different standards
'''
from abc import ABC, abstractmethod


class DataAnalyserBase(ABC):
    '''Gives thes basic structure of data analyser. Allows data processing according to a standard'''


class DataAnalyserFDX15140(DataAnalyserBase):
    '''Analyse data compliance of the norm FD X 15 140 2013'''
