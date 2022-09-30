"""
This module allows you to split data into periods when there is a periodic phenomenon.
"""
import pandas as pd


def get_positions_of_the_period_changes(data: pd.Series) -> pd.Int64Index:
    """
    return a pandas Int64Index representing the end off each series of period
    param Series : Series from pandas with the data of one sensor
    """

    # Create a dataframe for calculate the difference between value n and value n - 1
    data_2 = data[1:].reset_index(drop=True)
    df = pd.DataFrame({
        'data': data,
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
