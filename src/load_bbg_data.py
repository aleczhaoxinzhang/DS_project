import pandas as pd
import load_zero_coupon as zc
import config
import numpy as np
import math
from pathlib import Path

DATA_DIR = config.DATA_DIR

# this function will be changed to xbbg code at the end
def load_bbg_excel(data_dir=DATA_DIR):
    path = data_dir / 'manual' / 'bbg_data_v2.xlsx'
    df = pd.read_excel(path, sheet_name='Sheet2')
    df = df[['Date', 'dividend yield', 'index', 'futures']]
    df.set_index('Date', inplace=True)
    return df

def load_bbg_data(data_dir=DATA_DIR):
    path = data_dir / "pulled" / "bbg_data.parquet"
    _df = pd.read_parquet(path)
    return _df

if __name__ == "__main__":
    bbg_df = load_bbg_excel()
    path = Path(DATA_DIR) / "pulled" / "bbg_data.parquet"
    bbg_df.to_parquet(path)
    # print(bbg_df['futures'])