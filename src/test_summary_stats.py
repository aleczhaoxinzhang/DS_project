import pytest
import pandas as pd
import numpy as np
from create_summary_stats import summary_stats 
import load_bbg_data as lbbg  
import clean_data as cld  
import config


def get_test_data():
    DATA_DIR = config.DATA_DIR
    PAPER_END_DT = config.PAPER_END_DT
    
    bbg_df = cld.clean_bbg_data(PAPER_END_DT, data_dir=DATA_DIR)
    one_year_zc_df = cld.clean_one_year_zc(bbg_df.index, PAPER_END_DT, data_dir=DATA_DIR)
    
    return bbg_df, one_year_zc_df

@pytest.fixture
def test_data():
    # Load or simulate test data here. Adjust this example as needed.
    bbg_df, one_year_zc_df = get_test_data()
    return bbg_df, one_year_zc_df


def test_summary_stats_numerical_accuracy(test_data):
    bbg_df, one_year_zc_df = test_data
    
    actual_output = summary_stats(
        bbg_df['dividend yield'],
        bbg_df['index'],
        bbg_df['futures'],
        one_year_zc_df['1_year_yield'],
        one_year_zc_df['1_y_dis_factor']
    )

    expected_output = pd.DataFrame({
    'obs': [354, 354, 354, 354, 354],
    'mean': [2.187, 1076.526, 1077.047, 3.489, 0.966],
    'std': [0.666, 542.016, 540.954, 2.637, 0.025],
    'min': [1.056, 257.070, 257.050, 0.099, 0.908],
    '25%': [1.770, 536.238, 536.800, 0.663, 0.946],
    '50%': [2.051, 1117.885, 1120.375, 3.655, 0.964],
    '75%': [2.727, 1379.128, 1382.875, 5.542, 0.993],
    'max': [3.914, 2423.410, 2421.000, 9.658, 0.999],
    'ρ': [0.988, 0.996, 0.996, 0.996, 0.996]
}, index=['dividend yield', 'index', 'futures', '1_year_yield', '1_y_dis_factor'])

    tolerances = {
        'obs': 0.01,  
        'mean': 0.01,
        'std': 0.01,
        'min': 0.01,
        '25%': 0.01,
        '50%': 0.01,
        '75%': 0.01,
        'max': 0.01,
        'ρ': 0.01
    }

    for col in expected_output.columns:
        for index in expected_output.index:
            expected_value = expected_output.loc[index, col]
            actual_value = actual_output.loc[index, col]
            tolerance = tolerances[col]
            assert abs(expected_value - actual_value) <= abs(expected_value * tolerance), f"{col} for {index} is outside of tolerance"


def test_summary_stats_output_structure(test_data):
    bbg_df, one_year_zc_df = test_data
    result_df = summary_stats(
        bbg_df['dividend yield'],
        bbg_df['index'],
        bbg_df['futures'],
        one_year_zc_df['1_year_yield'],
        one_year_zc_df['1_y_dis_factor']
    )

    expected_columns = ['obs', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'ρ']
    assert all(column in result_df.columns for column in expected_columns), "Not all expected columns are present in the output."

    expected_index = ['dividend yield', 'index', 'futures', '1_year_yield', '1_y_dis_factor']
    assert all(idx in result_df.index for idx in expected_index), "Not all expected indices are present in the output."

def test_summary_stats_data_types(test_data):
    bbg_df, one_year_zc_df = test_data
    result_df = summary_stats(
        bbg_df['dividend yield'],
        bbg_df['index'],
        bbg_df['futures'],
        one_year_zc_df['1_year_yield'],
        one_year_zc_df['1_y_dis_factor']
    )

    assert result_df.dtypes['obs'] == np.int64, "'obs' column is not of type int64."
    for col in ['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'ρ']:
        assert result_df.dtypes[col] == np.float64, f"'{col}' column is not of type float64."

def test_summary_stats_handling_nan_values(test_data):
    bbg_df, one_year_zc_df = test_data

    # Introduce NaN values into the test data
    bbg_df['dividend yield'][0] = np.nan

    result_df = summary_stats(
        bbg_df['dividend yield'],
        bbg_df['index'],
        bbg_df['futures'],
        one_year_zc_df['1_year_yield'],
        one_year_zc_df['1_y_dis_factor']
    )

    # Check if the count (obs) has been adjusted correctly for NaN values
    expected_obs = len(bbg_df['dividend yield']) - 1  # Adjust based on your handling of NaN values
    actual_obs = result_df.loc['dividend yield', 'obs']
    assert actual_obs == expected_obs, "The function does not correctly adjust for NaN values."

'''
# Test summary_stats onsistency  
def generate_or_load_data_of_size(data_size):

    bbg_df = pd.DataFrame({
        'dividend yield': np.random.normal(2.187, 0.666, data_size),
        'index': np.random.normal(1076.526, 542.016, data_size),
        'futures': np.random.normal(1077.047, 540.954, data_size),
    })

    one_year_zc_df = pd.DataFrame({
        '1_year_yield': np.random.normal(3.489, 2.637, data_size),
        '1_y_dis_factor': np.random.normal(0.966, 0.025, data_size),
    })

    return bbg_df, one_year_zc_df

@pytest.mark.parametrize("data_size", [100, 200, 300])
def test_summary_stats_consistency_across_sizes(data_size):
    # Generate or load data of different sizes
    bbg_df, one_year_zc_df = generate_or_load_data_of_size(data_size)  # Implement this function

    result_df = summary_stats(
        bbg_df['dividend yield'],
        bbg_df['index'],
        bbg_df['futures'],
        one_year_zc_df['1_year_yield'],
        one_year_zc_df['1_y_dis_factor']
    )

    # Verify some aspect of consistency, e.g., data types or presence of all expected columns
    assert all(result_df.dtypes == np.float64 or result_df.dtypes == np.int64),\
        "Inconsistent data types across different data sizes."
'''

