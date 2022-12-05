from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from typing import List


@dataclass
class ProcessedSensorData:
    '''object that contains statistics for a sensor after data processing'''
    min: float
    max: float
    stability: float
    mean: float
    std: float
    umj: float
    mean_increased_by_umj: float
    mean_decreased_by_umj: float


@dataclass
class ProcessedCaracterisationData:
    '''object that contains statistics for a caracterisation after data processing'''
    time_of_measurement: datetime
    stability_max: float
    homogeneity_max: float
    air_temperature: float
    air_uncertainty: float
    setpoint_error: float
    indication_error: float


@dataclass
class Equipement:
    name: str
    numberInventaire: str
    numberSerie: str
    marque: str
    reference: str
    setpoint: float
    indicator: float
    internal_heigth: float
    internal_width: float
    internal_depth: float
    ventilation: bool = True
    aeration: bool = False


class Sensor:
    def __init__(self, name: str, number_inventory: str, number_serial: str, measurement_uncertiainty: float, measurements: pd.Series, data_processing_strategy) -> None:
        '''
        Object that contains data from a sensor
        '''
        self.name: str = name
        self.numberInventory: str = number_inventory
        self.numberSerial: str = number_serial
        self.measurementUncertainty: float = measurement_uncertiainty
        self.measurements: pd.Series = measurements
        self.dataProcessingStrategy = data_processing_strategy
        self.processed_data: ProcessedSensorData = data_processing_strategy.get_processed_data(
            self.measurementUncertainty,
            self.measurements
        )


@dataclass
class Cartographie:

    def __init__(self, equipement: Equipement, sensors: List[Sensor], datetimeSerie: pd.Series, cible: float, emt: float, data_processing_data_strategy) -> None:
        self.equipement = equipement
        self.sensors = sensors
        self.datetimeSerie = datetimeSerie
        self.cible = cible
        self.emt = emt
        self.processed_data = data_processing_data_strategy.get_processed_data(
            self.equipement.setpoint,
            self.equipement.indicator,
            self.sensors,
            self.datetimeSerie
        )
