'''
This module define classes for analyse data according to different standards
'''
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import sqrt
import pandas as pd


@dataclass
class ProcessedSensorData:
    '''object that contains statistics after data processing'''
    min: float
    max: float
    stability: float
    mean: float
    std: float
    umj: float
    mean_increased_by_umj: float
    mean_decreased_by_umj: float


@dataclass
class DataSensorAnalyserBase(ABC):
    '''Gives thes basic structure of data analyser. Allows data processing according to a standard'''

    measurements: pd.Series = None
    sensor_measurement_uncertainty: float = None

    @abstractmethod
    def get_processed_data(self,  sensor_measurement_uncertainty: float, measurements: pd.Series) -> ProcessedSensorData:
        """Return object ProcessedSensorData"""


class DataSensorAnalyserFDX15140(DataSensorAnalyserBase):
    '''Analyse data compliance of the norm FD X 15 140 2013'''

    def get_processed_data(self, sensor_measurement_uncertainty: float, measurements: pd.Series) -> ProcessedSensorData:
        # import pdb
        # pdb.set_trace()
        assert measurements.dtype == float, TypeError(
            "The pandas Series must be float type")
        self.measurements = measurements
        self.sensor_measurement_uncertainty = sensor_measurement_uncertainty

        return ProcessedSensorData(
            min=self.__get_min(),
            max=self.__get_max(),
            stability=self.__get_stability(),
            mean=self.__get_mean(),
            std=self.__get_std(),
            umj=self.__get_Umj(),
            mean_increased_by_umj=self.__get_mean_increased_by_Umj(),
            mean_decreased_by_umj=self.__get_mean_decreased_by_Umj()
        )

    def __get_min(self) -> float:
        return round(self.measurements.min(), 2)

    def __get_max(self) -> float:
        return round(self.measurements.max(), 2)

    def __get_stability(self) -> float:
        return self.measurements.max() - self.measurements.min()

    def __get_mean(self) -> float:
        return self.measurements.mean()

    def __get_std(self) -> float:
        return self.measurements.std()

    def __get_Umj(self) -> float():
        return 2*sqrt(self.measurements.std()**2 + (self.sensor_measurement_uncertainty/2)**2)

    def __get_mean_increased_by_Umj(self) -> float:
        return self.__get_mean() + self.__get_Umj()

    def __get_mean_decreased_by_Umj(self) -> float:
        return self.__get_mean() - self.__get_Umj()


class Sensor:
    def __init__(self, name: str, number_inventory: str, number_serial: str, measurement_uncertiainty: float, measurements: pd.Series, data_processing_strategy: DataSensorAnalyserBase) -> None:
        '''
        Object that contains data from a sensor
        '''
        self.name: str = name
        self.numberInventory: str = number_inventory
        self.numberSerial: str = number_serial
        self.measurementUncertainty: float = measurement_uncertiainty
        self.measurements: pd.Series = measurements
        self.dataProcessingStrategy: DataSensorAnalyserBase = data_processing_strategy
        self.processed_data: ProcessedSensorData = data_processing_strategy.get_processed_data(
            self.measurementUncertainty,
            self.measurements
        )
