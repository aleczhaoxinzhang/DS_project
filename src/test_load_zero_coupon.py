import pandas as pd
import pytest
import numpy as np
from pathlib import Path

import config
import load_zero_coupon

DATA_DIR = config.DATA_DIR

def test_pull_fed_yield_curve():
    df = load_zero_coupon.pull_fed_yield_curve()
    
    # Check if the function returns a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Test if the DataFrame has the expected columns
    expected_columns = expected_columns = ['SVENY01', 'SVENY02', 'SVENY03', 'SVENY04', 'SVENY05', 
                    'SVENY06', 'SVENY07', 'SVENY08', 'SVENY09', 'SVENY10', 
                    'SVENY11', 'SVENY12', 'SVENY13', 'SVENY14', 'SVENY15', 
                    'SVENY16', 'SVENY17', 'SVENY18', 'SVENY19', 'SVENY20', 
                    'SVENY21', 'SVENY22', 'SVENY23', 'SVENY24', 'SVENY25', 
                    'SVENY26', 'SVENY27', 'SVENY28', 'SVENY29', 'SVENY30']
    assert all(col in df.columns for col in expected_columns)

    # Test if the DataFrame has at least one row of data
    assert len(df) > 0
    
    # Test if the function raises an error when given an invalid data directory
    with pytest.raises(FileNotFoundError):
        load_zero_coupon.load_fed_yield_curve(data_dir=Path("invalid_directory"))


def test_load_fed_yield_curve():
    # Assuming there is a parquet file at the specified path
    df = load_zero_coupon.load_fed_yield_curve()

    # Test if the default date range has the expected start date and end date
    assert df.index.min() == pd.Timestamp('1961-06-14')
    assert df.index.max() >= pd.Timestamp('2024-02-16')
    
    # Test numbers
    assert np.isclose(df.loc['2017-06-30', 'SVENY03'], 1.5719000101)
    assert np.isclose(df.loc['2017-06-30', 'SVENY30'], 3.040899992)

