from caracterisation.data_reader import DataReaderCSV
from caracterisation.data_cutter import DataCutterAnalysisSignOfDifference
from caracterisation.data_checker import DataCheckerEtablishedSystem


class TestDataCheckerEtablishedSystem:
    def test_is_compliance_not_etablished(self):
        dataReader = DataReaderCSV(
            filepath_or_buffer='tests/data_set_regime_not_etablished.csv',
            delimiter=";",
            decimal=","
        )
        dataCutter = DataCutterAnalysisSignOfDifference(
            dataReader=dataReader,
            colunm_mane_for_cutting_period='Sensor_1'
        )

        data = dataCutter.get_cutting_data()

        dataChecker = DataCheckerEtablishedSystem(
            dataframe=data,
            name_column_sensor='Sensor_1',
            name_column_number_period='number_period'
        )

        assert dataChecker.is_data_compliance() == False

    def test_is_compliance_etablished(self):
        dataReader = DataReaderCSV(
            filepath_or_buffer='tests/data_set_regime_etablished.csv',
            delimiter=";",
            decimal=","
        )
        dataCutter = DataCutterAnalysisSignOfDifference(
            dataReader=dataReader,
            colunm_mane_for_cutting_period='Sensor_1'
        )

        data = dataCutter.get_cutting_data()

        dataChecker = DataCheckerEtablishedSystem(
            dataframe=data,
            name_column_sensor='Sensor_1',
            name_column_number_period='number_period'
        )

        assert dataChecker.is_data_compliance() == True
