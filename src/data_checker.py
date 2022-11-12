'''
This module define classes for checking quality of data (this is use for check)
'''
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import sqrt
import pandas as pd
from typing import List


@dataclass
class DataCheckerBase(ABC):
    '''Base checker to done structue for verify data compliance with standards'''
    dataframe: pd.DataFrame
    name_column_sensor: str
    name_column_number_period: str

    @abstractmethod
    def is_data_compliance(self) -> bool:
        '''Return the compliance of data according to the tests to be done by the class'''


@dataclass
class DataCheckerEtablishedSystem(DataCheckerBase):
    '''Check data accordingly with the annex C of the nom FD X 15 140'''
    sensor_variance: float = 0.1

    def is_data_compliance(self) -> bool:
        if self.__hypothesis_a_is_true:
            return self.__hypothesis_b_is_true()
        else:
            return self.__hypothesis_c_is_true and self.__hypothesis_d_is_true

    def __hypothesis_a_is_true(self) -> bool:
        '''Check hypothesis a from the annex'''
        return True if self.dataframe[self.name_column_sensor].var()**2 <= self.sensor_variance ** 2 else False

    def __hypothesis_b_is_true(self) -> bool:
        '''Check hypothesis b from the annex'''
        averages = self.__get_couples_averages_of_sensor()
        return all([abs(averages[i-1] - averages[i]) <= 1.96 * sqrt(2*(self.sensor_variance**2/30)) for i in range(1, len(averages))])

    def __hypothesis_c_is_true(self) -> bool:
        '''Check hypothesis c from the annex'''
        variances = self.__get_couples_variances_of_sensor()
        return all([max(variances[i-1]**2/variances[i]**2, variances[i]**2/variances[i-1]**2) <= 2.1 for i in range(1, len(variances))])

    def __hypothesis_d_is_true(self) -> bool:
        '''Check hypothesis d from annex'''
        averages = self.__get_couples_averages_of_sensor()
        variances = self.__get_couples_variances_of_sensor()
        return all([abs(averages[i-1] - averages[i]) <= 2*sqrt((variances[i-1]**2 + variances[i])/30) for i in range(1, min(len(averages), len(variances)))])

    def __get_couples_averages_of_sensor(self) -> List[List[float]]:
        '''return couples averages'''
        couples_averages = [m for m in self.dataframe.groupby(
            [self.name_column_number_period]).mean()[self.name_column_sensor]]

        return couples_averages

    def __get_couples_variances_of_sensor(self) -> List[List[float]]:
        '''return couples variances'''
        couples_variances = [v for v in self.dataframe.groupby(
            [self.name_column_number_period]).var()[self.name_column_sensor]]
        return couples_variances
