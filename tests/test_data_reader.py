from src.data_reader import DataReaderBase, DataReaderCSV
import unittest


class TestDataReaderBase(unittest.TestCase):

    def test_have_method_get_dataframe(self):
        self.assertTrue(hasattr(DataReaderBase, 'get_dataframe'),
                        'DataReaderBase must have a function get_dataframe')

    def test_have_method_check_config(self):
        self.assertTrue(hasattr(DataReaderBase, 'check_config'),
                        'DataReaderBase must have a function check_config')


class TestDataReaderCSV(unittest.TestCase):
    filepath_or_buffer = 'data_set.csv'
    delimiter = '.'
    decimal = '.'

    def setUp(self) -> None:
        self.dataReader = DataReaderCSV(
            filepath_or_buffer=self.filepath_or_buffer,
            delimiter=self.delimiter,
            decimal=self.decimal
        )

    def test_class_initialisation(self):
        self.assertEqual(self.dataReader.filepath_or_buffer, self.filepath_or_buffer,
                         'Filepath or buffer is not correctly assigned during class initialization.')
        self.assertEqual(self.dataReader.delimiter, self.delimiter,
                         "Delimiter is not correctly assigned during class initialization")
        self.assertEqual(self.dataReader.decimal, self.decimal,
                         'decimal is not correctly assigned during class initialization.')

