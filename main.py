import pdb
from utils.data_reader import DataReaderCSV
from utils.data_cutter import DataCutterAnalysisSignOfDifference
from utils.data_checker import DataCheckerEtablishedSystem
from utils.data_analyser import DataSensorAnalyserFDX15140, Sensor

# Récupérer les données
dataReader = DataReaderCSV('utils/tests/data_set.csv',
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

# Si régime établi instancier la class Cartographie
pdb.set_trace()
