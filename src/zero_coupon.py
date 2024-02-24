import pandas as pd
import requests
from io import BytesIO
from pathlib import Path

import config
DATA_DIR = config.DATA_DIR


def pull_fed_yield_curve():
    """
    Download the latest yield curve from the Federal Reserve
    
    This is the published data using Gurkaynak, Sack, and Wright (2007) model
    """
    
    url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"
    response = requests.get(url)
    pdf_stream = BytesIO(response.content)
    df = pd.read_csv(pdf_stream, skiprows=9, index_col=0, parse_dates=True)
    cols = ['SVENY' + str(i).zfill(2) for i in range(1, 31)]
    return df[cols]

def load_fed_yield_curve(data_dir=DATA_DIR):
    path = data_dir / "pulled" / "fed_yield_curve.parquet"
    _df = pd.read_parquet(path)
    return _df
    

if __name__ == "__main__":
    df = pull_fed_yield_curve()
    path = Path(DATA_DIR) / "pulled" / "fed_yield_curve.parquet"
    # df.loc['1988-01-29':'2017-06-30', ['SVENY01']].to_csv(DATA_DIR / "pulled" / 'one_year_zc.csv')
    df.to_parquet(path)