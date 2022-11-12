'''
This module define classes for get data by different source
'''

from abc import ABC, abstractmethod
import pandas as pd


class DataReaderBase(ABC):
    '''Abstract object for reader and prepare data for DataCutter'''

    def __init__(self) -> None:
        self.check_config()
        super().__init__()

    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        '''Return a DataFrame with data for next step of process'''

    @abstractmethod
    def check_config(self) -> None:
        '''Check if config is correct for this class'''


class DataReaderCSV(DataReaderBase):
    '''Create a Dataframe from a csv file'''

    def __init__(self, filepath_or_buffer, delimiter=';', decimal='.') -> None:
        self.filepath_or_buffer = filepath_or_buffer
        self.delimiter = delimiter
        self.decimal = decimal
        super().__init__()

    def get_dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(self.filepath_or_buffer,
                         delimiter=self.delimiter,
                         decimal=self.decimal)
        return df

    def check_config(self) -> None:
        try:
            pd.read_csv(self.filepath_or_buffer,
                        delimiter=self.delimiter, decimal=self.decimal)
        except Exception as e:
            print(e)
