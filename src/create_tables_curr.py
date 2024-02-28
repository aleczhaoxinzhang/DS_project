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

    # Table 1
    table_1_curr = cld.format_df(ct.calc_table_1(pr_t, pd_t), False)
    print(table_1_curr)
    path = Path(OUTPUT_DIR) / "table_1_curr.tex"
    table_1_curr.to_latex(path, index=True)

    # Table 2
    table_2_curr = cld.format_df(ct.calc_table_2(bbg_df['index'], pr_t, pd_t), True)
    print(table_2_curr)
    path = Path(OUTPUT_DIR) / "table_2_curr.tex"
    table_2_curr.to_latex(path, index=True)

    
