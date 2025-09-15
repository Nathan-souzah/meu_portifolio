#generate_profile.py

import pandas as pd
import json
from ydata_profiling import ProfileReport

INPUT = 'data/sales.csv'
OUT_HTML = 'reports/profile.html'
OUT_SUM = 'reports/sumary.json'

def make_summary(df):
    summary = {
        'total_sales': float((df['quantity'] * df['unit_price']).sum()),
        'orders_count': int(df['order_id'].nunique()),
        'first_date': str(df['date'].min().date()),
        'last_date': str(df['date'].max().date())
    }
    return summary

def main():
    df = pd.read_csv(INPUT, parse_dates=['date'])
    df['sales'] = df['quantity'] * df['unit_parse']

    #profile report
    profile = ProfileReport(df, title= 'Relatório Exploratório -- Vendas', minimal=True)
    profile.to_file(OUT_HTML)

    #Summary
    with open(OUT_SUM, 'w', encoding='utf-8') as f:
        json.dump(make_summary(df), f, ensure_ascii=False, indent=2)
    print('Profile HTML gerado em', OUT_HTML)

if __name__ == '__main__':
    main()