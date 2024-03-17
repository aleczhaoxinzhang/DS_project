"""
This module loads the S&P 500 index, Dividend yields, and all active futures during 
the given period from Bloomberg. It then saves the pulled raw data to separate parquet files for future use.
Functions to load the raw/clean data from the parquet file are also provided for future use.

"""

import pandas as pd
import load_zero_coupon as zc
import config
import numpy as np
import math
from pathlib import Path

DATA_DIR = config.DATA_DIR
USE_BBG = config.USE_BBG
START_DT = config.START_DT
PAPER_END_DT = config.PAPER_END_DT
CURR_END_DT = config.CURR_END_DT


if USE_BBG:
    from xbbg import blp

    def pull_bbg_data(end_date):
        bbg_df = pd.DataFrame()
        bbg_df['dividend yield'] = blp.bdh("SPX Index","EQY_DVD_YLD_12m", START_DT, end_date)[("SPX Index","EQY_DVD_YLD_12m")]
        
        bbg_df['index'] = blp.bdh("SPX Index","px_last", START_DT, end_date)[("SPX Index","px_last")]
        
        bbg_df['futures'] = pd.concat([blp.bdh("SP1 Index","px_last", START_DT, "1997-08-31")[("SP1 Index","px_last")],
                                        blp.bdh("ES1 Index","px_last", "1997-09-30", end_date)[("ES1 Index","px_last")]])
        
        bbg_df.index.name = 'Date'

        return bbg_df
else:
    # this function will be changed to xbbg code at the end
    def load_bbg_excel(data_dir=DATA_DIR):
        # load dividend yield and index data from excel
        path = data_dir / 'manual' / 'bbg_data_v2.xlsx'
        df = pd.read_excel(path, sheet_name='Sheet2')
        df = df[['Date', 'dividend yield', 'index']]
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index)

        # load futures data
        path = data_dir / 'manual' / 'bbg_data_futures.xlsx'
        future_df = pd.read_excel(path, sheet_name='future prices')
        maturity_df = pd.read_excel(path, sheet_name='maturities')
        future_df.set_index('Date', inplace=True)
        future_df.index = pd.to_datetime(future_df.index)
        maturity_df.set_index('Date', inplace=True)
        maturity_df.index = pd.to_datetime(maturity_df.index)
        return df, future_df, maturity_df

def load_bbg_data(data_dir=DATA_DIR):
    path = data_dir / "pulled" / "bbg_data.parquet"
    _df = pd.read_parquet(path)
    path = Path(DATA_DIR) / "pulled" / "bbg_future_data.parquet"
    _future_df = pd.read_parquet(path)
    path = Path(DATA_DIR) / "pulled" / "bbg_maturity_data.parquet"
    _maturity_df = pd.read_parquet(path)

    return _df, _future_df, _maturity_df


def load_clean_bbg_data(end_date, data_dir=DATA_DIR):
    if end_date == PAPER_END_DT:
        path = Path(DATA_DIR) / "pulled" / "clean_bbg_paper_data.parquet"
    elif end_date == CURR_END_DT:
        path = Path(DATA_DIR) / "pulled" / "clean_bbg_curr_data.parquet"
    else:
        raise ValueError("Invalid end date")
    _df = pd.read_parquet(path)
    return _df


if __name__ == "__main__":
    if USE_BBG:
        bbg_df = pull_bbg_data(CURR_END_DT)
    else:
        bbg_df, future_df, maturity_df = load_bbg_excel()
    
    path = Path(DATA_DIR) / "pulled" / "bbg_data.parquet"
    bbg_df.to_parquet(path)
    path = Path(DATA_DIR) / "pulled" / "bbg_future_data.parquet"
    future_df.to_parquet(path)
    path = Path(DATA_DIR) / "pulled" / "bbg_maturity_data.parquet"
    maturity_df.to_parquet(path)

    # print(maturity_df)
    
    