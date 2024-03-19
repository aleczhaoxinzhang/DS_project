"""
This script creates summary statistics for the dividend yield, index, futures, and 1-year zero coupon bond yield and discount factor.

"""

import pandas as pd
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
import clean_data as cld
import config
import numpy as np
import math
from pathlib import Path

DATA_DIR = config.DATA_DIR
OUTPUT_DIR = config.OUTPUT_DIR
PAPER_END_DT = config.PAPER_END_DT


def summary_stats(series1, series2, series3, series4, series5):   
    # Summary statistics for each series
    summary1 = series1.describe()
    summary2 = series2.describe()
    summary3 = series3.describe()
    summary4 = series4.describe()
    summary5 = series5.describe()
    
    # Autocorrelation for each series
    autocorr1 = series1.autocorr(lag=1)
    autocorr2 = series2.autocorr(lag=1)
    autocorr3 = series3.autocorr(lag=1)
    autocorr4 = series4.autocorr(lag=1)
    autocorr5 = series5.autocorr(lag=1)
    
    # Combine all statistics into a DataFrame
    stats_df = pd.concat([summary1, summary2, summary3, summary4, summary5], axis=1)
    stats_df.columns = [series1.name, series2.name, series3.name, series4.name, series5.name]
    stats_df.loc['Autocorrelation'] = [autocorr1, autocorr2, autocorr3, autocorr4, autocorr5]

    stats_df = stats_df.round(3)
    stats_df = stats_df.transpose()
    stats_df['count'] = np.ceil(stats_df['count']).astype(int)
    stats_df = stats_df.rename(columns={'count': 'obs', 'Autocorrelation': 'ρ'})
    
    return stats_df


if __name__ == "__main__":
    bbg_df = lbbg.load_clean_bbg_data(PAPER_END_DT, data_dir=DATA_DIR)
    one_year_zc_df = ldzc.load_clean_fed_yield_curve(PAPER_END_DT, data_dir=DATA_DIR)
    summary_stats_df = cld.format_df(summary_stats(bbg_df['dividend yield'], bbg_df['index'], 
                                      bbg_df['futures'], one_year_zc_df['1_year_yield'], 
                                      one_year_zc_df['1_y_dis_factor']), False)
    summary_stats_df.index = [
    "Dividend Yield",
    "Index",
    "Futures",
    "1-Year Yield",
    "1-Year Discount Factor"
    ]   
    print(summary_stats_df)
    summary_stats_df.columns = summary_stats_df.columns.str.replace('%', r'\%')
    summary_stats_df.columns = summary_stats_df.columns.str.replace('ρ', r'$\rho$')
    path = Path(OUTPUT_DIR) / "summary_stats.tex"
    summary_stats_df.to_latex(path, index=True)
    
