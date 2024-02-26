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
        path = data_dir / 'manual' / 'bbg_data_v2.xlsx'
        df = pd.read_excel(path, sheet_name='Sheet2')
        df = df[['Date', 'dividend yield', 'index', 'futures']]
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index)
        return df

def load_bbg_data(data_dir=DATA_DIR):
    path = data_dir / "pulled" / "bbg_data.parquet"
    _df = pd.read_parquet(path)
    return _df

if __name__ == "__main__":
    if USE_BBG:
        bbg_df = pull_bbg_data(CURR_END_DT)
    else:
        bbg_df = load_bbg_excel()
    
    path = Path(DATA_DIR) / "pulled" / "bbg_data.parquet"
    bbg_df.to_parquet(path)
    # print(bbg_df['futures'])
    