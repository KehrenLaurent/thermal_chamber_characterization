from tkinter.ttk import Separator
import unittest
import pandas as pd
import stats.breakdown_by_period as b_b_p


class TestCalc(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_data: pd.DataFrame = self.__get_data_for_mock()

    @staticmethod
    def __get_data_for_mock() -> pd.DataFrame:
        df = pd.read_csv('stats/tests/data_set.csv',
                         delimiter=";", decimal=',')
        return df

    def test_get_positions_of_the_period_changes(self):
        positions_of_the_period_changes_for_sensor_1 = [10, 18, 27, 36, 44, 53, 62, 70, 79,
                                                        88, 96, 105]
        series_sensor_1 = self.mock_data['Sensor_1']
        position = b_b_p.get_positions_of_the_period_changes(series_sensor_1)
        self.assertListEqual(
            positions_of_the_period_changes_for_sensor_1, position)
