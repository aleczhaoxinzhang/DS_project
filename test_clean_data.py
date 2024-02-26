import pandas as pd
import numpy as np
import pytest
import clean_data
import config
import load_zero_coupon as ldzc
import load_bbg_data as lbbg

# Prepare a specific date range for testing
START_DT = config.START_DT 
PAPER_END_DT = config.PAPER_END_DT 
DATA_DIR = config.DATA_DIR
USE_BBG = config.USE_BBG

if USE_BBG:
        bbg_df = clean_data.clean_bbg_data(data_dir=DATA_DIR)
else:
    bbg_df = lbbg.load_bbg_data(data_dir=DATA_DIR)

df = clean_data.clean_one_year_zc(bbg_df.index, PAPER_END_DT, DATA_DIR)

def test_clean_one_year_zc():
    # Check start and end date
    assert df.index.min() >= pd.to_datetime(START_DT)
    assert df.index.max() <= pd.to_datetime(PAPER_END_DT)
    
    # Check the column rename
    assert '1_year_yield' in df.columns

    # Check for no missing values in the resulting DataFrame
    assert not df.isnull().values.any()

    # Check if '1_y_dis_factor' is calculated correctly
    assert all(df['1_y_dis_factor'] > 0)
    
    # Check if the expected discount factor is calculated directly
    assert np.isclose(df.loc['2017-02-28', '1_y_dis_factor'], 0.990878)