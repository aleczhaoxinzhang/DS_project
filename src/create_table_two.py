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

def calc_regressions(X, y):
    X = sm.add_constant(X)  # Add a constant term
    model = sm.OLS(y, X).fit()
    return model.params.iloc[0], model.rsquared_adj  # Return beta and adjusted R-squared

def calc_table_2(index, pr_t, pd_t):
    # Calculate epsilon_pr_t and epsilon_pd_t
    epsilon_pr_t = pr_t - sm.OLS(pr_t, sm.add_constant(pd_t)).fit().predict()
    epsilon_pd_t = pd_t - sm.OLS(pd_t, sm.add_constant(pr_t)).fit().predict()
    
    # Calculate future one-year S&P 500 returns
    sp500_returns = (index.shift(-12) / index - 1)  # Assuming index is sorted by date
    
    # Limit to in-sample data
    in_sample = (index.index >= '1988-01-29') & (index.index <= '1997-11-30')
    sp500_returns = sp500_returns[in_sample]
    pr_t = pr_t[in_sample]
    pd_t = pd_t[in_sample]
    epsilon_pr_t = epsilon_pr_t[in_sample]
    epsilon_pd_t = epsilon_pd_t[in_sample]
    
    # Perform regressions and collect results
    results = pd.DataFrame(index=['beta', 'adjusted R-squared'], columns=['pr_t', 'pd_t', 'epsilon_pr_t', 'epsilon_pd_t'])
    for var, name in zip([pr_t, pd_t, epsilon_pr_t, epsilon_pd_t], results.columns):
        beta, adj_r_squared = calc_regressions(var, sp500_returns)
        results.loc['beta', name] = beta
        results.loc['adjusted R-squared', name] = adj_r_squared
    
    return results


if __name__ == "__main__":
    if USE_BBG:
        bbg_df = cld.clean_bbg_data(PAPER_END_DT, data_dir=DATA_DIR)
    else:
        bbg_df = lbbg.load_bbg_data(data_dir=DATA_DIR)

    one_year_zc_df = cld.clean_one_year_zc(bbg_df.index, PAPER_END_DT, data_dir=DATA_DIR)

    pr_t = calc_pr(bbg_df, one_year_zc_df)
    pd_t = calc_pd(bbg_df)

    # Table 2
    print(calc_table_2(pr_t, pd_t))
