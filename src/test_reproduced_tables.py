import pandas as pd
import numpy as np
<<<<<<< HEAD
import create_tables_curr as ctc
import create_tables as ct
import clean_data as cld
=======
import create_tables_curr as ct
>>>>>>> main

import config

DATA_DIR = config.DATA_DIR
<<<<<<< HEAD
CURR_END_DT = config.CURR_END_DT

bbg_df = cld.clean_bbg_data(CURR_END_DT, data_dir=DATA_DIR)
one_year_zc_df = cld.clean_one_year_zc(bbg_df.index, CURR_END_DT, data_dir=DATA_DIR)

pr_t = ct.calc_pr(bbg_df, one_year_zc_df)
pd_t = ct.calc_pd(bbg_df)

# Tolerances for each column
tolerances = {
    'obs': 0.00,
=======

# Tolerances for each column
tolerances = {
>>>>>>> main
    'mean': 0.01,
    'std': 0.01,
    'min': 0.01,
    '25%': 0.01,
    '50%': 0.01,
    '75%': 0.01,
    'max': 0.01,
    'ρ': 0.01,
    'Correlation': 0.01,
    'pr_t': 0.01,
    'pd_t': 0.01,
    'epsilon_pr_t': 0.01,
    'epsilon_pd_t': 0.01,
    'R²': 0.01
}

# Test function for Table 1
def test_table1():
    # Use the actual output of ct.calc_table_1(pr_t, pd_t)
<<<<<<< HEAD
    table1 = ct.calc_table_1(pr_t, pd_t)
=======
    table1 = ct.calc_table_1(ct.pr_t, ct.pd_t)
>>>>>>> main
    
    # Define the expected (desired) values for Table 1
    expected_table1 = pd.DataFrame({'obs': [433, 433], 'mean': [3.857, 3.904], 'std': [1.058, 0.291],
                                    'min': [2.348, 3.241], '25%': [2.994, 3.763], '50%': [3.515, 3.928],
                                    '75%': [4.697, 4.089], 'max': [7.104, 4.551], 'ρ': [0.958, 0.988],
                                    'Correlation': [0.192, 0.192]})
    
    # 1. Check the shape of the table
    expected_shape = (2, 10)  # Assuming 2 rows and 10 columns
    assert table1.shape == expected_shape, f"Table 1 shape mismatch. Expected {expected_shape}, got {table1.shape}"

    # 2. Check data types of columns
    expected_dtypes = ['int64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64']
    actual_dtypes = [str(dtype) for dtype in table1.dtypes]
    assert actual_dtypes == expected_dtypes, f"Table 1 data types mismatch. Expected {expected_dtypes}, got {actual_dtypes}"

    # 3. Check the number of decimal places for float columns
    for col in table1.select_dtypes(include=['float64']):
        max_decimals = table1[col].apply(lambda x: len(str(x).split('.')[-1])).max()
        assert max_decimals <= 3, f"Column {col} in Table 1 has more than 3 decimal places"

    # 4. Check if 'obs' column has positive integers
    assert all(table1['obs'] > 0), "Column 'obs' in Table 1 contains non-positive integers"

    # 5. Check if 'Correlation' column values are between -1 and 1
    assert all(table1['Correlation'].between(-1, 1)), "Column 'Correlation' in Table 1 contains values outside the range [-1, 1]"

    # 6. Check numerical values with tolerances
    for col in expected_table1.columns:
        assert np.allclose(table1[col], expected_table1[col], atol=tolerances[col]), f"Column {col} in Table 1 exceeds tolerance of {tolerances[col]}"

<<<<<<< HEAD

# Test function for Table 2
def test_table2():
    # Use the actual output of ct.calc_table_2(bbg_df['index'], pr_t, pd_t)
    table2 = ct.calc_table_2(bbg_df['index'], pr_t, pd_t)
=======
# Test function for Table 2
def test_table2():
    # Use the actual output of ct.calc_table_2(bbg_df['index'], pr_t, pd_t)
    table2 = ct.calc_table_2(ct.bbg_df['index'], ct.pr_t, ct.pd_t)
>>>>>>> main
    
    # Define the expected (desired) values for Table 2
    expected_table2 = pd.DataFrame({'pr_t': [0.01, 0.02], 'pd_t': [0.03, 0.04], 'epsilon_pr_t': [0.05, 0.06], 'epsilon_pd_t': [0.07, 0.08]})
   
    # 1. Check the shape of the table
    expected_shape = (2, 4)  # Assuming 2 rows and 4 columns
    assert table2.shape == expected_shape, f"Table 2 shape mismatch. Expected {expected_shape}, got {table2.shape}"

    # 2. Check data types of columns
    expected_dtypes = ['float64', 'float64', 'float64', 'float64']
    actual_dtypes = [str(dtype) for dtype in table2.dtypes]
    assert actual_dtypes == expected_dtypes, f"Table 2 data types mismatch. Expected {expected_dtypes}, got {actual_dtypes}"

    # 3. Check the number of decimal places for float columns
    for col in table2.select_dtypes(include=['float64']):
        max_decimals = table2[col].apply(lambda x: len(str(x).split('.')[-1])).max()
        assert max_decimals <= 3, f"Column {col} in Table 2 has more than 3 decimal places"

    # 4. Check if 'pr_t' and 'pd_t' column values are between -1 and 1
    assert all(table2['pr_t'].between(-1, 1)), "Column 'pr_t' in Table 2 contains values outside the range [-1, 1]"
    assert all(table2['pd_t'].between(-1, 1)), "Column 'pd_t' in Table 2 contains values outside the range [-1, 1]"

    # 5. Check if 'epsilon_pr_t' and 'epsilon_pd_t' column values are positive
    assert all(table2['epsilon_pr_t'] >= 0), "Column 'epsilon_pr_t' in Table 2 contains negative values"
    assert all(table2['epsilon_pd_t'] >= 0), "Column 'epsilon_pd_t' in Table 2 contains negative values"

    # 6. Check numerical values with tolerances
    for col in expected_table2.columns:
        assert np.allclose(table2[col], expected_table2[col], atol=tolerances[col]), f"Column {col} in Table 2 exceeds tolerance of {tolerances[col]}"




