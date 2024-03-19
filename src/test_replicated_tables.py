import pytest
import config
<<<<<<< HEAD
import clean_data as cld
import create_tables as ct
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
=======
>>>>>>> main

from create_tables import calc_table_1, calc_table_2

DATA_DIR = config.DATA_DIR
<<<<<<< HEAD
PAPER_END_DT = config.PAPER_END_DT

bbg_df = cld.clean_bbg_data(PAPER_END_DT, data_dir=DATA_DIR)
one_year_zc_df = cld.clean_one_year_zc(bbg_df.index, PAPER_END_DT, data_dir=DATA_DIR)

pr_t = ct.calc_pr(bbg_df, one_year_zc_df)
pd_t = ct.calc_pd(bbg_df)
=======
>>>>>>> main

# Define fixtures for Table 1 and Table 2 data
@pytest.fixture
def table1_data():
<<<<<<< HEAD
    a = calc_table_1(pr_t, pd_t)
=======
    a = calc_table_1()
>>>>>>> main
    return a

@pytest.fixture
def table2_data():
<<<<<<< HEAD
    return calc_table_2(bbg_df['index'], pr_t, pd_t)
=======
    return calc_table_2()
>>>>>>> main

# Test function for Table 1
def test_table1(table1_data):
    # Expected data types for Table 1
    expected_dtypes = {
        'obs': 'int',
        'mean': 'float',
        'std': 'float',
        'min': 'float',
        '25%': 'float',
        '50%': 'float',
        '75%': 'float',
        'max': 'float',
        'ρ': 'float',
        'Correlation': 'float'
    }

    # Check data types
    for column, dtype in expected_dtypes.items():
        assert table1_data[column].dtype == dtype, f"Data type for {column} is incorrect. Expected {dtype}, got {table1_data[column].dtype}"

    # Check number of decimal places
    for column in table1_data.columns:
        max_decimals = table1_data[column].apply(lambda x: len(str(x).split('.')[-1]) if '.' in str(x) else 0).max()
        assert max_decimals <= 3, f"Number of decimal places for {column} exceeds 3"

    # Check values within tolerance for each column
    tolerance = {
        'obs': 10,
        'mean': 0.1,
        'std': 0.1,
        'min': 0.1,
        '25%': 0.1,
        '50%': 0.1,
        '75%': 0.1,
        'max': 0.1,
        'ρ': 0.05,
        'Correlation': 0.05
    }
    expected_values = {
        'obs': 348,
        'mean': 3.992,
        'std': 0.531,
        'min': 2.677,
        '25%': 3.630,
        '50%': 3.992,
        '75%': 4.195,
        'max': 6.631,
        'ρ': 0.915,
        'Correlation': 0.874
    }
    for column in table1_data.columns:
        actual_value = table1_data[column].mean() if column != 'obs' else table1_data[column].iloc[0]
        assert abs(actual_value - expected_values[column]) <= tolerance[column], f"{column} value is out of tolerance. Expected {expected_values[column]}, got {actual_value}"

    # Check for positive values (example for 'std' column)
    assert table1_data['std'].min() > 0, "Standard deviation contains non-positive values"

    # Check correlation coefficient range
    assert table1_data['Correlation'].between(-1, 1).all(), "Correlation coefficient is out of range [-1, 1]"


# Test function for Table 2
def test_table2(table2_data):
    # Expected data types for Table 2
    expected_dtypes = {
        'pr_t': 'float',
        'pd_t': 'float',
        'epsilon_pr_t': 'float',
        'epsilon_pd_t': 'float'
    }

    # Check data types
    for column, dtype in expected_dtypes.items():
        assert table2_data[column].dtype == dtype, f"Data type for {column} is incorrect. Expected {dtype}, got {table2_data[column].dtype}"

    # Check number of decimal places
    for column in table2_data.columns:
        max_decimals = table2_data[column].apply(lambda x: len(str(x).split('.')[-1]) if '.' in str(x) else 0).max()
        assert max_decimals <= 3, f"Number of decimal places for {column} exceeds 3"

    # Check values within tolerance for each column
    tolerance = {
        'pr_t': 0.05,
        'pd_t': 0.05,
        'epsilon_pr_t': 0.05,
        'epsilon_pd_t': 0.05
    }
    expected_values = {
        'pr_t': -0.138,
        'pd_t': -0.193,
        'epsilon_pr_t': -0.160,
        'epsilon_pd_t': 0.098
    }
    for column in table2_data.columns:
        actual_value = table2_data[column].mean()
        assert abs(actual_value - expected_values[column]) <= tolerance[column], f"{column} value is out of tolerance. Expected {expected_values[column]}, got {actual_value}"

    # Check if the R² values are within a reasonable range (0 to 1)
    assert 0 <= table2_data['epsilon_pr_t'].mean() <= 1,"R² value for epsilon_pr_t is out of range"
    assert 0 <= table2_data['epsilon_pd_t'].mean() <= 1, "R² value for epsilon_pd_t is out of range"

    # Check if the correlation between pr_t and pd_t is within a reasonable range (-1 to 1)
    correlation = table2_data[['pr_t', 'pd_t']].corr().iloc[0, 1]
    assert -1 <= correlation <= 1, f"Correlation between pr_t and pd_t is out of range: {correlation}"
    


