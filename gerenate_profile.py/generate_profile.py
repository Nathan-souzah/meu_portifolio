#generate_profile.py

import pandas as pd
import json
import sweetviz as sv

#caminhos dos arquivos
INPUT = 'data/sales.csv'
OUT_HTML = 'reports/profile.html'
OUT_SUM = 'reports/summary.json'

def make_summary(df: pd.DataFrame) -> dict:
    """Gera um resumo rápido das vendas"""
    summary = {
        'total_sales': float((df['quantity'] * df['unit_price']).sum()),
        'orders_count': int(df['order_id'].nunique()),
        'first_date': str(df['date'].min().date()),
        'last_date': str(df['date'].max().date())
    }
    return summary

def main():
    df = pd.read_csv(INPUT, parse_dates=['date'])
    df['sales'] = df['quantity'] * df['unit_price']

    report = sv.analyze(df)
    report.show_html(OUT_HTML) 
    
    #Gera resumo JSON
    with open(OUT_SUM, 'w', encoding='utf-8') as f:
        json.dump(make_summary(df), f, ensure_ascii=False, indent=2)
    print('Profile HTML gerado em', OUT_HTML)
    print('Resumo JSON gerado em', OUT_SUM)

if __name__ == '__main__':
    main()