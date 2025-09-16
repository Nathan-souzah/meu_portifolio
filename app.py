import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title='📊 Dashboard Vendas', layout='wide')

# Carregar dados
@st.cache_data
def load_data(path='data/sales.csv'):
    df = pd.read_csv(path, parse_dates=['date'])
    df['sales'] = df['quantity'] * df['unit_price']
    return df

df = load_data()

st.title(' 📊 Dashboard de Vendas')

# Sidebar Filtros
st.sidebar.header('Filtros')
min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input('📆 Intervalo de datas', [min_date, max_date])
region = st.sidebar.multiselect('🌎 Região', options=sorted(df['region'].unique()), default=[])

# Garantir que date_range tenha 2 datas
if isinstance(date_range, datetime):
    start = end = pd.to_datetime(date_range)
elif len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    st.error("❌Selecione um intervalo de datas válido.")
    st.stop()

# Aplicar filtros
mask = (df['date'] >= start) & (df['date'] <= end)

if region:
    mask &= df['region'].isin(region)

filtered = df.loc[mask].copy()

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Faturamento (R$)', f"{filtered['sales'].sum():,.2f}")
with col2:
    st.metric('Pedidos', int(filtered['order_id'].nunique()))
with col3:
    ticket = filtered['sales'].sum() / max(1, filtered['order_id'].nunique())
    st.metric('Ticket médio (R$)', f"{ticket:,.2f}")

st.markdown('---')

# Série temporal
sales_by_day = filtered.groupby('date', as_index=False)['sales'].sum()
if sales_by_day.empty:
    st.warning('❌ Sem dados para o período selecionado.')
else:
    fig = px.line(sales_by_day, x='date', y='sales', title='💵 Vendas por dia', markers=True)
    st.plotly_chart(fig, use_container_width=True)

# Top produtos
st.subheader('🥇 Top produtos')
top_produtos = (
    filtered.groupby('product', as_index=False)
    .agg(total_sales=('sales','sum'), total_qty=('quantity', 'sum'))
    .sort_values('total_sales', ascending=False)
)
st.dataframe(top_produtos)

# Download dados filtrados
csv = filtered.to_csv(index=False)
st.download_button('⬇️ Baixar dados filtrados (CSV)', csv, file_name='sales_filtered.csv', mime='text/csv')
