

from caracterisation.data_reader import DataReaderBase, DataReaderCSV
from datetime import datetime
import pytest


class TestDataReaderCSV:
    filepath_or_buffer = 'tests/data_set.csv'
    delimiter = ';'
    decimal = ','
    sensors_name = [f'Sensor_{x}' for x in range(1, 10)]
    columns_name = ['dateheure', ] + sensors_name

    def setup_class(self):
        self.dataReader = DataReaderCSV(
            filepath_or_buffer=self.filepath_or_buffer,
            delimiter=self.delimiter,
            decimal=self.decimal
        )

    def test_class_initialisation(self):
        assert self.dataReader.filepath_or_buffer == self.filepath_or_buffer
        assert self.dataReader.delimiter == self.delimiter
        assert self.dataReader.decimal == self.decimal

    def test_get_dataframe_columns_is_complete(self):
        df = self.dataReader.get_dataframe()
        df_columns_name = df.columns.tolist()

        # Check if df columns is complete
        for name in self.columns_name:
            assert name in df_columns_name

    def test_type_of_columns(self):
        df = self.dataReader.get_dataframe()

        assert df['dateheure'].dtype == datetime
        for s in self.sensors_name:
            assert df[s].dtype == float
