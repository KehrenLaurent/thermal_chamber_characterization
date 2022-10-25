'''
This module define classes for checking quality of data (this is use for check)
'''
from abc import ABC, abstractmethod


class DataCheckerBase(ABC):
    '''Base checker to done structue for verify data compliance with standards'''

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def is_data_compliance(self) -> bool:
        '''Return the compliance of data according to the tests to be done by the class'''


class DataCheckerEtablishedSystem(DataCheckerBase):
    '''Check data accordingly with the annex C of the nom FD X 15 140'''
    @abstractmethod
    def is_data_compliance(self) -> bool:
        return True
