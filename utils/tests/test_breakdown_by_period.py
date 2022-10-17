from pdb import set_trace
import unittest
import pandas as pd
import utils.breakdown_by_period as b_b_p


class TestCalc(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_data: pd.DataFrame = self.__get_data_for_mock()

    @staticmethod
    def __get_data_for_mock() -> pd.DataFrame:
        df = pd.read_csv('utils/tests/data_set.csv',
                         delimiter=";", decimal=',')
        return df

    def test_get_positions_of_the_period_changes(self):
        positions_of_the_period_changes_for_sensor_1 = [8, 16, 25, 34, 42, 51]
        series_sensor_1 = self.mock_data['Sensor_1']
        position = b_b_p.get_positions_of_the_period_changes(
            series_sensor_1).tolist()

        self.assertEqual(
            positions_of_the_period_changes_for_sensor_1, position)

    def test_add_in_dataframe_column_with_number_of_period(self):
        df = b_b_p.add_in_dataframe_column_with_number_of_period(
            self.mock_data, 'Sensor_1')

        # Check if the column number_period is add
        self.assertIn('number_period', df.columns.tolist())

        # compare the manual and algorith method of numerotation of period
        number_of_row = df.shape[0]
        number_of_row_with_manual_and_algo_number_period_is_the_same = df[
            df['P_manu_s1'] == df['number_period']].shape[0]

        # if all row is true the cut method is the same with manual and algo method
        self.assertEqual(
            number_of_row, number_of_row_with_manual_and_algo_number_period_is_the_same)

    def test_get_dataframe_compliant_with_fd_x_15140(self):
        df = b_b_p.get_dataframe_compliant_with_fd_x_15140(
            self.mock_data, 'Sensor_1')

        # Check if the dataframe have 30 values or more
        self.assertGreaterEqual(df.shape[0], 30)

        # check if the dataframe have 2 cycles or more
        self.assertGreaterEqual(df.groupby('number_period').size().shape[0], 2)


if __name__ == "__main__":
    unittest.main()
