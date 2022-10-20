from abc import ABC, abstractmethod
from dataclasses import dataclass
from distutils.command.config import config
import pandas as pd


@dataclass
class DataReaderConfig:
    '''Class that contains the configuration of the class DataReader'''
    path_file: str = ""
    file_delimiter: str = ""
    file_decimal_delimiter: str = ""


class DataReader(ABC):
    '''Abstract object for reader and prepare data for DataCutter'''

    def __init__(self, config: DataReaderConfig) -> None:
        self.check_config(config)
        self.config = config
        super().__init__()

    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        '''Return a DataFrame with data for next step of process'''

    @abstractmethod
    def check_config(self, config: DataReaderConfig) -> None:
        '''Check if config is correct for this class'''


class DataReaderCSV(DataReader):
    '''Create a Dataframe from a csv file'''

    def get_dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(self.config.path_file,
                         delimiter=self.config.file_delimiter,
                         decimal=self.config.file_decimal_delimiter)
        return df

    def check_config(self, config: DataReaderConfig) -> None:
        assert config.file_decimal_delimiter != "", ValueError(
            f'file_decimal_delimiter must be != ""')
        assert config.file_delimiter != "", ValueError(
            f'file_delimiter must be != ""')
        assert config.file_decimal_delimiter in (',', '.'), ValueError(
            f'{config.file_decimal_delimiter} is not in [.,]')
        assert config.file_delimiter in (',', ';', '.', '\t'), ValueError(
            f'{config.file_delimiter} is not in [.,;\t]')
