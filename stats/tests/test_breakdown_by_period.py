import unittest
import csv

import stats.breakdown_by_period as b_b_p


class TestCalc(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_data = self.__get_data_for_mock()

    @staticmethod
    def __get_data_for_mock():
        with open('stats/tests/data_set.csv', 'r', encoding='utf-8') as f:
            r = csv.reader(f, delimiter=";")
            return [l for l in r]

    def test_get_positions_of_the_period_changes(self):
        positions_of_the_period_changes_for_sensor_1 = [10, 18, 27, 36, 44, 53, 62, 70, 79,
                                                        88, 96, 105]
        data_of_the_sensor_1 = [d[1] for d in self.mock_data]
        self.assertListEqual(positions_of_the_period_changes_for_sensor_1,
                             b_b_p.get_positions_of_the_period_changes(data_of_the_sensor_1))
