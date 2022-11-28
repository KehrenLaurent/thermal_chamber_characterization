'''
This module define classes for cutting data with differently method
'''
from abc import ABC, abstractmethod
from .data_reader import DataReaderBase
import pandas as pd


class DataCutterBase(ABC):
    '''Base class for cut different series off data'''

    def __init__(self, dataReader: DataReaderBase, colunm_mane_for_cutting_period: str) -> None:
        """
        df_with_data : is the dataframe a analyse
        colunm_mane_for_cut_period: name of the column containing the data that will be used to define the periods
        """
        self.data_to_process = dataReader.get_dataframe()
        self.colunm_mane_for_cutting_period = colunm_mane_for_cutting_period
        self.data_processed: pd.DataFrame = None

        self._check_data_to_process()
        super().__init__()

    def _check_data_to_process(self):
        '''check the conformity of data_to_process'''
        assert self.data_to_process.shape[1] >= 10, 'The dataframe must be contains at least 10 columns'
        assert self.data_to_process.shape[0] >= 45, 'The dataframe must be contains at least 45 rows'
        assert self.colunm_mane_for_cutting_period in self.data_to_process.columns, f'{self.colunm_mane_for_cutting_period} is not in the dataframe'

    def get_cutting_data(self) -> pd.DataFrame:
        '''Return the data according to the method used to split the data'''
        if not self.data_processed:
            self._processing_data()
        return self.data_processed

    @abstractmethod
    def _processing_data(self) -> None:
        '''run the processing for cut data'''


class DataCutterAnalysisSignOfDifference(DataCutterBase):
    '''Cuts the data by calculating the difference between each data. 
    Positive values ​​indicate the slope is uphill and negative values ​​indicate the slope is downhill. 
    Each series is cut when the slope goes from a rising to a falling phase'''

    def _processing_data(self) -> None:

        # Get positions of the period change
        series_to_take_to_make_for_cut_data = self.data_to_process[
            self.colunm_mane_for_cutting_period].copy()
        index_of_end_positions = self.__get_end_positions_of_the_period_changes(
            series_to_take_to_make_for_cut_data)

        # Add column with number of period
        dataframe_with_number_of_periode = self.__add_in_dataframe_column_with_number_of_period(
            index_of_end_positions)

        # Set the processed data
        self.data_processed = self.__get_dataframe_compliant_with_fd_x_15140(
            dataframe_with_number_of_periode)

    def __get_end_positions_of_the_period_changes(self, series: pd.Series) -> pd.Index:
        """
        return a pandas Int64Index representing the end off each series of period
        param Series : Series from pandas with the data of one sensor
        """

        # Create a dataframe for calculate the difference between value n and value n - 1
        data_2 = series[1:].reset_index(drop=True)
        df = pd.DataFrame({
            'data': series,
            'data_2': data_2
        })

        df['diff'] = df['data'] - df['data_2']
        df = df.dropna(subset=['diff'])

        # Affection a symbol off each diff, +  for positive data evolution, - for negative data evolution, = for stable data evolution
        df.loc[df['diff'] > 0, 'symbol'] = "+"
        df.loc[df['diff'] < 0, 'symbol'] = "-"
        df.loc[df['diff'] == 0, 'symbol'] = "="

        # Creation of new column for comparing evolution of data between value n and value n - 1
        df['symbol_n'] = df.iloc[1:]['symbol'].reset_index(drop=True)

        # We want to cut the graph at each vertex
        df_to_return = df.loc[(df['symbol_n'] == '+') & (df['symbol'] == '-')]

        # We must add one in index to correct the previous offset
        index_to_return = df_to_return.index + 1

        # TODO : La methode ne fonctionne pas si la valeur pour les pics faibles où nous avons deux valeurs pour le sommet peut faire l'etude des signes sur plusieurs valeur par exemple deux valeurs d'aug et deux de dim.

        return index_to_return

    def __add_in_dataframe_column_with_number_of_period(self, end_positions: pd.Index) -> pd.DataFrame:
        """
        return a pandas dataframe with a new columns with the number of period (1 to ...) by numbering staring from the end
        """
        dataframe_to_return = self.data_to_process.copy()
        position_end = end_positions
        position_start = position_end[:-1]

        position_end_reverse = position_end[::-1]
        position_start_reverse = position_start[::-1]

        list_position = [[p_start, p_end-1] for p_start, p_end in zip(
            position_start_reverse, position_end_reverse)]

        i = 1
        for p_start, p_end in list_position:
            dataframe_to_return.loc[p_start: p_end, 'number_period'] = i
            i += 1

        return dataframe_to_return.dropna()

    def __get_dataframe_compliant_with_fd_x_15140(self, dataframe_with_number_position: pd.DataFrame) -> pd.DataFrame:
        """
        Return a pandas dataframe with a pandas dataframe with a new columns with the number of period (1 to ...) by numbering staring from the end.
        The dataframe is limited is limited to the last two regulation cycles (or more if there are not thirty measurements)
        """
        assert dataframe_with_number_position.shape[0] > 30, "Dataframe must contain more than 30 values"
        assert dataframe_with_number_position['number_period'].max(
        ) >= 2, "Dataframe must contain 2 periods or more"

        i = 2
        while True:
            period = [i for i in range(1, i)]
            if dataframe_with_number_position.loc[dataframe_with_number_position.number_period.isin(period)].shape[0] > 30:
                break

            i += 1

        return dataframe_with_number_position.loc[dataframe_with_number_position.number_period.isin(period)].copy()
