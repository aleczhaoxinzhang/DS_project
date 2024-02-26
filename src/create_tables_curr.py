import pandas as pd
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
import clean_data as cld
import create_tables as ct
import config
import numpy as np
import math

DATA_DIR = config.DATA_DIR
USE_BBG = config.USE_BBG
CURR_END_DT = config.CURR_END_DT


if __name__ == "__main__":
    if USE_BBG:
        bbg_df = cld.clean_bbg_data(CURR_END_DT, data_dir=DATA_DIR)
    else:
        bbg_df = lbbg.load_bbg_data(data_dir=DATA_DIR)

    one_year_zc_df = cld.clean_one_year_zc(bbg_df.index, CURR_END_DT, data_dir=DATA_DIR)

    pr_t = ct.calc_pr(bbg_df, one_year_zc_df)
    pd_t = ct.calc_pd(bbg_df)

    # Table 1
    print(ct.calc_table_1(pr_t, pd_t))

    # Table 2
    print(ct.calc_table_2(bbg_df['index'], pr_t, pd_t))
    
