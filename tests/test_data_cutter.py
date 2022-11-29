from caracterisation.data_cutter import DataCutterAnalysisSignOfDifference, DataCutterBase
from caracterisation.data_reader import DataReaderCSV


class TestDataCutterAnalysisSignOfDifference:
    def setup_class(self):
        self.dataReader = DataReaderCSV(
            filepath_or_buffer='tests/data_set.csv',
            delimiter=";",
            decimal=","
        )

        self.dataCutter = DataCutterAnalysisSignOfDifference(
            dataReader=self.dataReader,
            colunm_mane_for_cutting_period="Sensor_1"
        )

    def test_get_cutting_data(self):
        df = self.dataCutter.get_cutting_data()

        # Check if we have difference beetween different method of cutting
        check = df['P_manu_s1'] == df['number_period']
        number_check_is_false = check.loc[lambda x: x == False].count()

        assert number_check_is_false == 0, "The breakdowns between the automatic and manual method are different"
