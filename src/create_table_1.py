import pandas as pd
import zero_coupon as zc
import load_data as ld
import config
import numpy as np
import math

DATA_DIR = config.DATA_DIR

bbg_df = ld.load_bbg_excel()
one_year_zc_df = ld.load_one_year_zc(bbg_df.index, data_dir=DATA_DIR)

def calc_pr(bbg_df, one_year_zc_df):
    P_plus = bbg_df['futures'] * one_year_zc_df['SVENY01']
    P_minus = bbg_df['index'] - P_plus
    pr_t = np.log(P_plus / P_minus)
    return pr_t


def calc_pd(bbg_df):
    pd_t = np.log(100 / bbg_df['dividend yield']) # dividend yield is in percentage value
    return pd_t
    

def series_statistics(series1, series2):
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

print(series_statistics(calc_pr(bbg_df, one_year_zc_df), calc_pd(bbg_df)))