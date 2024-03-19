"""
This module calculates pr_t and pd_t from the previosuly cleaned current end date data, 
and replicates Table 1 and Table 2 for the current end date.

"""

import pandas as pd
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
import clean_data as cld
import create_tables as ct
import config
import numpy as np
import math
from pathlib import Path

DATA_DIR = config.DATA_DIR
CURR_END_DT = config.CURR_END_DT
OUTPUT_DIR = config.OUTPUT_DIR


if __name__ == "__main__":
    one_year_zc_df = ldzc.load_clean_fed_yield_curve(CURR_END_DT, data_dir=DATA_DIR)
    bbg_df = lbbg.load_clean_bbg_data(CURR_END_DT, data_dir=DATA_DIR)

    pr_t = ct.calc_pr(bbg_df, one_year_zc_df)
    pd_t = ct.calc_pd(bbg_df)
    
    # Check for NaN or Inf values in pr_t
    print("NaN or Inf values in pr_t:")
    print(pr_t[np.isnan(pr_t) | np.isinf(pr_t)])
    
    # Check for NaN or Inf values in pd_t
    print("NaN or Inf values in pd_t:")
    print(pd_t[np.isnan(pd_t) | np.isinf(pd_t)])

    # Check for NaN or Inf values in bbg_df['index']
    print("NaN or Inf values in bbg_df['index']:")
    print(bbg_df['index'][np.isnan(bbg_df['index']) | np.isinf(bbg_df['index'])])


    # Table 1
    table_1_curr = cld.format_df(ct.calc_table_1(pr_t, pd_t), False)
    table_1_curr.columns = table_1_curr.columns.str.replace('%', r'\%')
    table_1_curr.columns = table_1_curr.columns.str.replace('ρ', r'$\rho$')
    print(table_1_curr)
    path = Path(OUTPUT_DIR) / "table_1_curr.tex"
    table_1_curr.to_latex(path, index=True)

    # Table 2
    table_2_curr = cld.format_df(ct.calc_table_2(bbg_df['index'], pr_t, pd_t), True)
    print(table_2_curr)
    table_2_curr.index = table_2_curr.index.map(lambda x: f"${x}$")
    table_2_curr.columns = table_2_curr.columns.map(lambda x: f"${x}$")
    table_2_curr.columns = table_2_curr.columns.str.replace('epsilon_pr_t', r'\epsilon^{pr}_t')
    table_2_curr.columns = table_2_curr.columns.str.replace('epsilon_pd_t', r'\epsilon^{pd}_t')
    path = Path(OUTPUT_DIR) / "table_2_curr.tex"
    table_2_curr.to_latex(path, index=True)

    
