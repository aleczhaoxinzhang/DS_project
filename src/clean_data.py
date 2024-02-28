import pandas as pd
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
import config
import numpy as np
import math

DATA_DIR = config.DATA_DIR
USE_BBG = config.USE_BBG
START_DT = config.START_DT
PAPER_END_DT = config.PAPER_END_DT

if USE_BBG:
    def clean_bbg_data(end_date, data_dir=DATA_DIR):
        df = lbbg.load_bbg_data(data_dir)

        df = df.loc[START_DT : end_date]

        df.index = pd.to_datetime(df.index)
        
        # Group by year and month, and select the last date in each group
        return df.groupby([df.index.year, df.index.month]).tail(1)
else:
    def clean_bbg_data(end_date, data_dir=DATA_DIR):
        df = lbbg.load_bbg_data(data_dir)

        df = df.loc[START_DT : end_date]

        return df


def clean_one_year_zc(dates_select, end_date, data_dir=DATA_DIR):
    # Download the latest yield curve from the Federal Reserve
    df_zc = ldzc.load_fed_yield_curve(data_dir)
    # Select the one-year zero-coupon bond yield
    df_zc = df_zc.loc[START_DT : end_date, ['SVENY01']]

    df_zc.index = pd.to_datetime(df_zc.index)

    # Fill in missing values, some dates's values are missing, replace with the closest date's value
    df_zc = df_zc.fillna(method='ffill')

    # Select the dates matching the bbg dates
    df_zc = df_zc.loc[dates_select]

    df_zc = df_zc.rename(columns={'SVENY01': '1_year_yield'})

    # Convert to discount factor
    df_zc['1_y_dis_factor'] = np.exp(-df_zc['1_year_yield'] / 100)

    return df_zc


def format_df(df, all_col):
    if all_col:
        df = df.applymap(lambda x: '{:.3f}'.format(x))
    else:
        df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: '{:.3f}'.format(x))
    return df


if __name__ == "__main__":
    bbg_df = clean_bbg_data(PAPER_END_DT, data_dir=DATA_DIR)
    one_year_zc_df = clean_one_year_zc(bbg_df.index, PAPER_END_DT, data_dir=DATA_DIR)
    # print(one_year_zc_df)

    

