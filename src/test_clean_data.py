import pandas as pd
import numpy as np
import clean_data as cld
import config
import load_zero_coupon as ldzc
import load_bbg_data as lbbg

# Prepare a specific date range for testing
START_DT = config.START_DT 
CURR_END_DT = config.CURR_END_DT 
DATA_DIR = config.DATA_DIR

bbg_df = cld.clean_bbg_data(CURR_END_DT, data_dir=DATA_DIR)

def test_clean_bbg_data():
    # Check that the DataFrame is not empty
    assert not bbg_df.empty
    
    # Check that the index is a DatetimeIndex
    assert isinstance(bbg_df.index, pd.DatetimeIndex)
    
    # Check start and end date
    assert bbg_df.index.min() >= pd.to_datetime(START_DT)
    assert bbg_df.index.max() <= pd.to_datetime(CURR_END_DT)
    
    # Check the column names
    expected_columns = ['dividend yield', 'index', 'futures']
    assert all(col in bbg_df.columns for col in expected_columns)

    # Check for no missing values in the resulting DataFrame
    assert not bbg_df.isnull().values.any()

    # Check if data is grouped by year and month and last date is selected
    grouped_df = bbg_df.groupby([bbg_df.index.year, bbg_df.index.month])
    for _, group in grouped_df:
        assert group.index[-1] == bbg_df.loc[group.index].index[-1]
    
    # Check that the DataFrame has approximately monthly frequency
    assert all(bbg_df.index[i + 1] - bbg_df.index[i] <= pd.Timedelta(days=35) for i in range(len(bbg_df.index) - 1))

    # Check data types
    assert bbg_df.dtypes['dividend yield'] == float
    assert bbg_df.dtypes['index'] == float
    assert bbg_df.dtypes['futures'] == float


df = cld.clean_one_year_zc(bbg_df.index, CURR_END_DT, DATA_DIR)

def test_clean_one_year_zc():
    # Check that the DataFrame is not empty
    assert not df.empty
    
    # Check that the index is a DatetimeIndex
    assert isinstance(df.index, pd.DatetimeIndex)
     
    # Check start and end date
    assert df.index.min() >= pd.to_datetime(START_DT)
    assert df.index.max() <= pd.to_datetime(CURR_END_DT)
    
    # Check the column rename
    assert '1_year_yield' in df.columns

    # Check for no missing values in the resulting DataFrame
    assert not df.isnull().values.any()

    # Check if '1_y_dis_factor' is calculated correctly
    assert all(df['1_year_yield'] > 0)
    
    # Check if the expected discount factor is calculated directly
    assert np.isclose(df.loc['2017-02-28', '1_y_dis_factor'], 0.990878)
    
    # Check data types
    assert df.dtypes['1_year_yield'] == float
    assert df.dtypes['1_y_dis_factor'] == float
