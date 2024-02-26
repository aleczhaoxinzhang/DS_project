import pandas as pd
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
import clean_data as cld
import config
import numpy as np
import math

DATA_DIR = config.DATA_DIR
USE_BBG = config.USE_BBG
PAPER_END_DT = config.PAPER_END_DT


def calc_pr(bbg_df, one_year_zc_df):
    P_plus = bbg_df['futures'] * one_year_zc_df['1_y_dis_factor']
    P_minus = bbg_df['index'] - P_plus
    pr_t = np.log(P_plus / P_minus)
    pr_t = pr_t.rename('pr')
    return pr_t


def calc_pd(bbg_df):
    pd_t = np.log(100 / bbg_df['dividend yield']) # dividend yield is in percentage value
    pd_t = pd_t.rename('pd')
    return pd_t
    

def calc_table_1(series1, series2):
    # Summary statistics for each series
    summary1 = series1.describe()
    summary2 = series2.describe()
    
    # Correlation coefficient
    correlation = series1.corr(series2)
    
    # Autocorrelation for each series
    autocorr1 = series1.autocorr(lag=1)
    autocorr2 = series2.autocorr(lag=1)

    # Combine all statistics into a DataFrame
    stats_df = pd.concat([summary1, summary2], axis=1)
    stats_df.columns = ['pr', 'pd']
    stats_df.loc['Autocorrelation'] = [autocorr1, autocorr2]
    stats_df.loc['Correlation'] = [correlation, correlation]

    stats_df = stats_df.round(3)
    
    return stats_df.transpose()


if __name__ == "__main__":
    if USE_BBG:
        bbg_df = cld.clean_bbg_data(PAPER_END_DT, data_dir=DATA_DIR)
    else:
        bbg_df = lbbg.load_bbg_data(data_dir=DATA_DIR)

    one_year_zc_df = cld.clean_one_year_zc(bbg_df.index, PAPER_END_DT, data_dir=DATA_DIR)

    pr_t = calc_pr(bbg_df, one_year_zc_df)
    pd_t = calc_pd(bbg_df)

    # Table 1
    print(calc_table_1(pr_t, pd_t))
    