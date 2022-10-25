from utils.data_reader import DataReaderCSV
from utils.data_cutter import DataCutterAnalysisSignOfDifference
from utils.data_checker import DataCheckerEtablishedSystem
from utils.data_analyser import DataAnalyserFDX15140

# Récupérer les données
dataReader = DataReaderCSV('utils/tests/data_set.csv',
                           delimiter=";", decimal=",")

# Faire le découpage par période
dataCutter = DataCutterAnalysisSignOfDifference(dataReader, "Sensor_1")
df = dataCutter.get_cutting_data()

# Prendre prendre des périodes pour avoir au moins 30 mesures et au moins deux périodes

# Instancier les class sensors avec les périodes retenues

# Faire les test "Regime établi par méthode statistique pour l'ensemble des sondes"

# Si régime établi instancier la class Cartographie
