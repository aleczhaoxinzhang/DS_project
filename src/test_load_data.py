
import pandas as pd
import numpy as np
import pytest
from pathlib import Path

import config
from load_data import load_bbg_excel, load_one_year_zc

DATA_DIR = config.DATA_DIR

def test_load_bbg_excel_returns_dataframe():
    # Test if the function returns a pandas DataFrame
    df = load_bbg_excel()
    assert isinstance(df, pd.DataFrame), "load_bbg_excel should return a pandas DataFrame"

def test_load_bbg_excel_columns():
    # Test if the DataFrame has the expected columns
    df = load_bbg_excel()
    expected_columns = ['dividend yield', 'index', 'futures']
    assert df.columns.tolist() == expected_columns, "load_bbg_excel returned DataFrame has incorrect column names"

def test_load_bbg_excel_invalid_directory():
    # Test if the function raises an error when given an invalid directory
    with pytest.raises(FileNotFoundError):
        load_bbg_excel(data_dir=Path("invalid_directory"))

def test_load_bbg_excel_specific_values():
    # Test if specific values in the DataFrame are correct
    df = load_bbg_excel()
    assert df.loc['1988-01-29', 'dividend yield'] == 3.4909, "Incorrect 'dividend yield' value for 1988-01-29"
    assert df.loc['1988-02-29', 'index'] == 267.82, "Incorrect 'index' value for 1988-02-29"
    assert df.loc['2017-06-30', 'futures'] == 2421.00, "Incorrect 'futures' value for 2017-06-30"

def test_load_one_year_zc_returns_dataframe():
    # Test if the function returns a pandas DataFrame
    bbg_df = load_bbg_excel()
    zc_df = load_one_year_zc(bbg_df.index)
    assert isinstance(zc_df, pd.DataFrame), "load_one_year_zc should return a pandas DataFrame"

def test_load_one_year_zc_columns():
    # Test if the DataFrame has the expected column 'SVENY01'
    bbg_df = load_bbg_excel()
    zc_df = load_one_year_zc(bbg_df.index)
    assert 'SVENY01' in zc_df.columns, "load_one_year_zc returned DataFrame should contain 'SVENY01' column"

def test_load_one_year_zc_date_range():
    # Test if the default date range has the expected start date and end date
    bbg_df = load_bbg_excel()
    zc_df = load_one_year_zc(bbg_df.index)
    assert zc_df.index.min() == pd.Timestamp('1988-01-29'), "load_one_year_zc returned DataFrame has incorrect start date"
    assert zc_df.index.max() == pd.Timestamp('2017-06-30'), "load_one_year_zc returned DataFrame has incorrect end date"

def test_load_one_year_zc_specific_values():
    # Test if specific values in the DataFrame are correct
    bbg_df = load_bbg_excel()
    zc_df = load_one_year_zc(bbg_df.index)
    assert np.isclose(zc_df.loc['1988-01-29', 'SVENY01'], 0.934476, atol=1e-6), "Incorrect 'SVENY01' value for 1988-01-29"
    assert np.isclose(zc_df.loc['1988-02-29', 'SVENY01'], 0.935793, atol=1e-6), "Incorrect 'SVENY01' value for 1988-02-29"
    assert np.isclose(zc_df.loc['2017-06-30', 'SVENY01'], 0.987471, atol=1e-6), "Incorrect 'SVENY01' value for 2017-06-30"


