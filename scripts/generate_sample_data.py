import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# cria a pasta 'data' se não existir
os.makedirs("data", exist_ok=True)

np.random.seed(42)

n_days = 120
start = datetime(2025, 5, 1)
rows = []

products = ['Produto A', 'Produto B', 'Produto C', 'Produto D']
regions = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

order_id = 1000

for i in range(n_days):
    day = start + timedelta(days=i)
    orders_today = np.random.poisson(15)  # nº médio de pedidos por dia
    for _ in range(max(1, orders_today)):
        order_id += 1
        product = np.random.choice(products, p=[0.32, 0.25, 0.23, 0.20])
        qty = int(np.random.choice([1, 2, 3, 4], p=[0.6, 0.2, 0.1, 0.1]))

        unit_price = {
            'Produto A': 150.0,
            'Produto B': 299.9,
            'Produto C': 49.5,
            'Produto D': 89.0
        }

        region = np.random.choice(regions)

        rows.append({
            'date': day.strftime('%Y-%m-%d'),
            'order_id': order_id,
            'customer_id': f'CUST-{np.random.randint(1, 500):03d}',
            'product': product,
            'quantity': qty,
            'unit_price': unit_price[product],
            'region': region
        })

# salva em CSV
pd.DataFrame(rows).to_csv('data/sales.csv', index=False)
print('Gerado: data/sales.csv -- linhas:', len(rows))
