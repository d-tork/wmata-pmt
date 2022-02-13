"""Process WMATA SmarTrip usage for PMT reimbursement."""
from os import path
import argparse
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    level=logging.INFO
)


def main():
    args = get_args()
    filepath = path.normpath(path.join('/', 'src', args.filepath))
    data = get_data(filepath)
    data = add_day_of_week(data)
    data = drop_weekends(data)
    write_out(data)
    sum_refund_total(data)


def get_args():
    parser = argparse.ArgumentParser(description='Process WMATA usage.')
    parser.add_argument('filepath', help='WMATA SmarTrip usage export.')
    args = parser.parse_args()
    return args


def get_data(filepath): 
    logger.info(f'source: {filepath}')
    df = pd.read_csv(filepath)
    return df


def add_day_of_week(df):
    df['Time'] = pd.to_datetime(df['Time'])
    df['day_of_week'] = df['Time'].dt.strftime('%a')
    return df


def drop_weekends(df):
    weekends = ['Sat', 'Sun']
    df_filtered = df.loc[~df['day_of_week'].isin(weekends)]
    return df_filtered

def write_out(df):
    year_month = get_year_month(df)
    outfile = f'{year_month}-metro.csv'
    outpath = path.join('/', 'src', outfile)
    df.to_csv(outpath, index=False)


def get_year_month(df) -> str:
    first_date = df['Time'].iloc[0]
    year_month = first_date.strftime('%Y-%m')
    return year_month


def sum_refund_total(df):
    df['amount'] = (df['Change (+/-)']
        .replace(r'[\$,)]', '', regex=True)
        .replace(r'[(]', '-', regex=True)
    )
    df['amount'] = pd.to_numeric(df['amount'])
    total_spent = df.loc[df['amount'] < 0, 'amount'].sum()
    logger.info(f'total spent: ${total_spent:.2f}')


if __name__ == '__main__':
    main()
