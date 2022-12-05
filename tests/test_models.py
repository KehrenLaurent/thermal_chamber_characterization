from caracterisation.models import ProcessedSensorData, ProcessedCaracterisationData, Equipement, Sensor, Cartographie
from caracterisation.data_analyser import package/module
from datetime import datetime
import pandas as pd

class TestProcessedSensorData:
    data = {
        'min': 0,
        'max': 3,
        'stability': 0.5,
        'mean': 1.5,
        'std': 0.3,
        'umj': 0.9,
        'mean_increased_by_umj': 1.5 + 0.9,
        'mean_decreased_by_umj':  1.5 - 0.9
    }

    def test_initialisation(self):
        processedSensorData = ProcessedSensorData(
            **self.data
        )

        for key, value in self.data.items():
            assert value == processedSensorData.__getattribute__(
                key), f'for attribute {key} value does\'nt match'

class TestProcessedCaracterisationData:
    data = {
        'time_of_measurement': datetime(2022, 12, 5, 12, 00, 00),
        'stability_max': 0.5,
        'homogeneity_max': 0.5,
        'air_temperature': 1.5,
        'air_uncertainty': 0.6,
        'setpoint_error': 0.5,
        'indication_error': 0.6
    }

    def test_initialisation(self):
        processedCaracterisationData = ProcessedCaracterisationData(
            **self.data
        )

        for key, value in self.data.items():
            assert value == processedCaracterisationData.__getattribute__(
                key), f'for attribute {key} value does\'nt match'


class TestSensor:
    data = {
        'name': 'name',
        'numberInventory': 'numberInventory',
        'numberSerial': 'numberSerial',
        'measurementUncertainty': 0.2,
        'measurements': pd.Series([1., 2., 3.])
        'dataProcessingStrategy': 
    }