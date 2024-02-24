import pandas as pd
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
import config
import numpy as np
import math

DATA_DIR = config.DATA_DIR

def clean_one_year_zc(dates_select, data_dir=DATA_DIR):
    # Download the latest yield curve from the Federal Reserve
    df_zc = ldzc.load_fed_yield_curve(data_dir)
    # Select the one-year zero-coupon bond yield
    df_zc = df_zc.loc['1988-01-29':'2017-06-30', ['SVENY01']]

    # Fill in missing values, some dates's values are missing, replace with the closest date's value
    df_zc = df_zc.fillna(method='ffill')

    # Select the dates matching the bbg dates
    df_zc = df_zc.loc[dates_select]

    # Convert to discount factor
    df_zc = np.exp(-df_zc / 100)
    return df_zc

if __name__ == "__main__":
    bbg_df = lbbg.load_bbg_data(data_dir=DATA_DIR)
    one_year_zc_df = ldzc.load_one_year_zc(bbg_df.index, data_dir=DATA_DIR)
    # print(one_year_zc_df)

