"""
This module cleans the raw data from Bloomberg and the Federal Reserve.
The 1-year expiry future prices throughout the period are interpolated from the active futures data.
It saves the both the paper and current end date cleaned data to separate parquet files for future use.
The module also selects the 1-year zero-coupon yield corresponding to the Bloomberg dates, and saves the 
discount factors to a parquet file for future use.

"""

import pandas as pd
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
import config
import numpy as np
import math
from pathlib import Path
from scipy.interpolate import PchipInterpolator

DATA_DIR = config.DATA_DIR
USE_BBG = config.USE_BBG
START_DT = config.START_DT
PAPER_END_DT = config.PAPER_END_DT
CURR_END_DT = config.CURR_END_DT

if USE_BBG:
    def clean_bbg_data(end_date, data_dir=DATA_DIR):
        df = lbbg.load_bbg_data(data_dir)

        df = df.loc[START_DT : end_date]

        df.index = pd.to_datetime(df.index)
        
        # Group by year and month, and select the last date in each group
        return df.groupby([df.index.year, df.index.month]).tail(1)
else:
    def clean_bbg_data(end_date, data_dir=DATA_DIR):
        df, future_df, maturity_df = lbbg.load_bbg_data(data_dir)

        df = df.loc[START_DT : end_date]
        future_df = future_df.loc[START_DT : end_date]
        maturity_df = maturity_df.loc[START_DT : end_date]

        for index, row in maturity_df.iterrows():
            # Count the number of zeros in the row
            zero_count = (row == 0).sum()
            
            # If there are exactly two zeros
            if zero_count > 1:
                # Find the indices of the columns with zero values
                zero_cols = row[row == 0].index
                # Update the second column with zero value to -1
                maturity_df.loc[index, zero_cols[1]] = -1
        
        future_df = future_df[maturity_df >= 0]
        maturity_df = maturity_df[maturity_df >= 0]

        interpolated_futures = []
        for date in future_df.index:
            # Constructing a new DataFrame
            new_df = pd.DataFrame({
                'future': future_df.loc[date],
                'maturity': maturity_df.loc[date]
                })
            # Dropping rows with NaN values in the first column
            new_df = new_df.dropna(subset=['future'])
            interpolator = PchipInterpolator(new_df['maturity'], new_df['future'])
            interpolated_futures.append(interpolator([12])[0])
        
        df['futures'] = interpolated_futures

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
    # Clean the data up to the paper end date
    bbg_df = clean_bbg_data(PAPER_END_DT, data_dir=DATA_DIR)
    one_year_zc_df = clean_one_year_zc(bbg_df.index, PAPER_END_DT, data_dir=DATA_DIR)

    path = Path(DATA_DIR) / "pulled" / "clean_bbg_paper_data.parquet"
    bbg_df.to_parquet(path)

    path = Path(DATA_DIR) / "pulled" / "clean_one_y_zc_paper.parquet"
    one_year_zc_df.to_parquet(path)

    # Clean the data up to the current end date
    bbg_df = clean_bbg_data(CURR_END_DT, data_dir=DATA_DIR)

    one_year_zc_df = clean_one_year_zc(bbg_df.index, CURR_END_DT, data_dir=DATA_DIR)

    path = Path(DATA_DIR) / "pulled" / "clean_bbg_curr_data.parquet"
    bbg_df.to_parquet(path)

    path = Path(DATA_DIR) / "pulled" / "clean_one_y_zc_curr.parquet"
    one_year_zc_df.to_parquet(path)
    

