'''
This module define classes for analyse data according to different standards
'''
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import sqrt
import statistics as stat
from datetime import datetime
import pandas as pd
from typing import List

from caracterisation.models import Sensor, Equipement, ProcessedSensorData, ProcessedCaracterisationData


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
        return round(self.measurements.max() - self.measurements.min(), 2)

    def __get_mean(self) -> float:
        return round(self.measurements.mean(), 2)

    def __get_std(self) -> float:
        return round(self.measurements.std(), 2)

    def __get_Umj(self) -> float():
        return round(2*sqrt(self.measurements.std()**2 + (self.sensor_measurement_uncertainty/2)**2), 2)

    def __get_mean_increased_by_Umj(self) -> float:
        return round(self.__get_mean() + self.__get_Umj(), 2)

    def __get_mean_decreased_by_Umj(self) -> float:
        return round(self.__get_mean() - self.__get_Umj(), 2)


@dataclass
class DataCaracterisationAnalyserBase(ABC):
    '''Give the structure of a analyser for temperature caracterisation'''
    setpoint: float = None
    indication: float = None
    sensors: List[Sensor] = None
    serie_time_measurement: pd.Series = None

    @abstractmethod
    def get_processed_data(self) -> ProcessedCaracterisationData:
        '''Return a processed ProcessedCaracterisationData'''


class DataCaracterisationAnalyserFDX15140(DataCaracterisationAnalyserBase):
    """Processing in accordance with the FX15140 """

    def get_processed_data(self, setpoint: float, indication: float, sensors: List[Sensor], serie_time_measurement: pd.Series) -> ProcessedCaracterisationData:
        self.setpoint = setpoint
        self.indication = indication
        self.sensors = sensors
        self.serie_time_measurement = serie_time_measurement

        return ProcessedCaracterisationData(
            time_of_measurement=self.__get_time_of_measurement(),
            stability_max=self.__get_stability_max(),
            homogeneity_max=self.__get_homogeneity_max(),
            air_temperature=self.__get_air_temperature(),
            air_uncertainty=self.__get_air_uncertainty(),
            setpoint_error=self.__get_setpoint_error(),
            indication_error=self.__get_indication_error()
        )

    def __get_time_of_measurement(self) -> float:
        return self.serie_time_measurement.max() - self.serie_time_measurement.min()

    def __get_stability_max(self) -> float:
        return round(max([s.processed_data.stability for s in self.sensors]), 2)

    def __get_homogeneity_max(self) -> float:
        return round(max([s.processed_data.mean_increased_by_umj for s in self.sensors]) - min([s.processed_data.mean_decreased_by_umj for s in self.sensors]), 2)

    def __get_air_temperature(self) -> float:
        return round(sum(s.processed_data.mean for s in self.sensors)/len(self.sensors), 2)

    def __get_air_uncertainty(self) -> float:
        uncertainty_max_of_sensors = max(
            [s.measurementUncertainty for s in self.sensors])/2
        std_mean_of_sensors = stat.stdev(
            [s.processed_data.mean for s in self.sensors])
        std_std_of_sensors = stat.stdev(
            [s.processed_data.std for s in self.sensors])
        number_of_measurements = min(
            [len(s.measurements) for s in self.sensors])

        return round(sqrt(uncertainty_max_of_sensors**2 + sqrt(std_mean_of_sensors**2+std_std_of_sensors**2*(1-(1/number_of_measurements)))), 2)

    def __get_setpoint_error(self) -> float:
        return round(self.indication - self.__get_air_temperature(), 2)

    def __get_indication_error(self) -> float:
        return round(self.setpoint - self.__get_air_temperature(), 2)