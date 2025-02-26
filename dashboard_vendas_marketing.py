import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Conectar ao banco de dados SQLite
def get_data(query):
    conn = sqlite3.connect("vendas_marketing (1).db")
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Consultas SQL para extrair dados
query_vendas = """
    SELECT canal, SUM(valor_venda) as total_vendas
    FROM vendas
    WHERE data_venda >= DATE('now', '-3 months')
    GROUP BY canal
"""
query_top_produtos = """
    SELECT produto, COUNT(*) as quantidade_vendida, AVG(margem_lucro) as margem_media
    FROM vendas
    GROUP BY produto
    ORDER BY quantidade_vendida DESC
    LIMIT 5
"""
query_ticket_medio = """
    SELECT segmento, AVG(valor_venda) as ticket_medio
    FROM vendas
    GROUP BY segmento
"""
query_interacoes = """
    SELECT canal_marketing, COUNT(*) as interacoes
    FROM interacoes_marketing
    GROUP BY canal_marketing
"""

# Carregar dados
df_vendas = get_data(query_vendas)
df_produtos = get_data(query_top_produtos)
df_ticket = get_data(query_ticket_medio)
df_interacoes = get_data(query_interacoes)

# Início do Streamlit
st.set_page_config(page_title="Dashboard Vendas & Marketing", layout="wide")
st.title("Dashboard de Vendas e Marketing")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total de Vendas Outbound", f"R$ {df_vendas[df_vendas['canal']=='Outbound']['total_vendas'].sum():,.2f}")
col2.metric("Total de Vendas Inbound", f"R$ {df_vendas[df_vendas['canal']=='Inbound']['total_vendas'].sum():,.2f}")
col3.metric("Ticket Médio B2B", f"R$ {df_ticket[df_ticket['segmento']=='B2B']['ticket_medio'].values[0]:,.2f}")

# Gráficos
st.subheader("Vendas por Canal")
st.plotly_chart(px.bar(df_vendas, x='canal', y='total_vendas', text='total_vendas', title="Total de Vendas por Canal"))

st.subheader("Top 5 Produtos Vendidos")
st.plotly_chart(px.bar(df_produtos, x='produto', y='quantidade_vendida', text='quantidade_vendida', title="Produtos Mais Vendidos"))

st.subheader("Engajamento por Canal de Marketing")
st.plotly_chart(px.pie(df_interacoes, names='canal_marketing', values='interacoes', title="Interações por Canal"))