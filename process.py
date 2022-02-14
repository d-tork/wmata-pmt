"""Process WMATA SmarTrip usage for PMT reimbursement."""
from os import path
import sys
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    level=logging.INFO
)


def main():
    raw_data = get_input()
    data = convert_input_to_df(raw_data)
    data = add_day_of_week(data)
    data = drop_weekends(data)
    data = parse_amounts(data)

    display_data(data)
    sum_amount_spent(data)
    write_out(data)


def get_input(): 
    file_contents = sys.stdin.readlines()
    if not file_contents:
        raise ValueError('No data passed. \
            You must pipe it with " < filename.csv" after `docker run ...`.')
    return file_contents

def convert_input_to_df(raw_data: list) -> pd.DataFrame:
    no_whitespace_rows = [s.strip() for s in raw_data]
    list_of_lists = [s.split(',') for s in no_whitespace_rows]
    header_row = list_of_lists.pop(0)
    df = pd.DataFrame(list_of_lists, columns=header_row)
    return df


def add_day_of_week(df):
    df['Time'] = pd.to_datetime(df['Time'])
    df['day_of_week'] = df['Time'].dt.strftime('%a')
    df = df.sort_values('Time')
    return df


def drop_weekends(df):
    weekends = ['Sat', 'Sun']
    df_filtered = df.loc[~df['day_of_week'].isin(weekends)]
    return df_filtered


def parse_amounts(df):
    df['amount'] = (df['Change (+/-)']
        .replace(r'[\$,)]', '', regex=True)
        .replace(r'[(]', '-', regex=True)
    )
    df['amount'] = pd.to_numeric(df['amount'])
    return df


def sum_amount_spent(df):
    negative_amounts = df.loc[df['amount'] < 0]
    total_spent = negative_amounts['amount'].sum()
    logger.info(f'\n\n total spent: ${total_spent:.2f}')


def display_data(df):
    cols = ['Time', 'day_of_week', 'Operator', 'amount']
    display_df = df.loc[df['amount'] < 0, cols]
    print('\n', display_df)


def write_out(df):
    year_month = get_year_month(df)
    outfile = f'{year_month}-metro.csv'
    outpath = path.join('/', 'data', outfile)
    df.to_csv(outpath, index=False)


def get_year_month(df) -> str:
    first_date = df['Time'].iloc[0]
    year_month = first_date.strftime('%Y-%m')
    return year_month


if __name__ == '__main__':
    main()
