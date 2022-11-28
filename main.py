import pdb
from caracterisation.data_reader import DataReaderCSV
from caracterisation.data_cutter import DataCutterAnalysisSignOfDifference
from caracterisation.data_checker import DataCheckerEtablishedSystem
from caracterisation.data_analyser import DataSensorAnalyserFDX15140, Sensor, Equipement, Cartographie, DataCaracterisationAnalyserFDX15140

import pandas as pd

# Récupérer les données
dataReader = DataReaderCSV('src/tests/data_set.csv',
                           delimiter=";", decimal=",")

# Faire le découpage par période
dataCutter = DataCutterAnalysisSignOfDifference(dataReader, "Sensor_1")
df = dataCutter.get_cutting_data()

# Faire les test "Regime établi par méthode statistique pour l'ensemble des sondes"
if DataCheckerEtablishedSystem(df, 'Sensor_1', 'number_period').is_data_compliance():
    print('OK')
else:
    print('NOK')

# first sensor
s1 = Sensor(name='Sensor_1', number_inventory='PP8-KIT-0001', number_serial='1frfrr', measurement_uncertiainty=0.2,
            measurements=df['Sensor_1'], data_processing_strategy=DataSensorAnalyserFDX15140())

sensors_data = [
    {
        'name': 'Sensor_1',
        'number_inventory': 'PP8-KIT-0001',
        'number_serial': 'serie_1',
        'measurement_uncertiainty': 0.2,
        'measurements': df['Sensor_1'],
        'data_processing_strategy': DataSensorAnalyserFDX15140()
    },
    {
        'name': 'Sensor_2',
        'number_inventory': 'PP8-KIT-0002',
        'number_serial': 'serie_2',
        'measurement_uncertiainty': 0.2,
        'measurements': df['Sensor_2'],
        'data_processing_strategy': DataSensorAnalyserFDX15140()
    },
]

sensors = [Sensor(**kwargs) for kwargs in sensors_data]
dateheure = pd.to_datetime(df['dateheure'], format="%d/%m/%Y %H:%M")
equipement = Equipement('Chambre froide', 'PP9-ref-0001',
                        'hdge', 'Liebherr', 'LKV1610', 5.0, 5.0, 300.0, 350.0, 50.0)
cartographie = Cartographie(
    equipement, sensors, dateheure, 5, 3, DataCaracterisationAnalyserFDX15140())


# Si régime établi instancier la class Cartographie
pdb.set_trace()
