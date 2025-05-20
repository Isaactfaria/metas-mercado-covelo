import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Configuração da página DEVE SER A PRIMEIRA COISA NO SCRIPT
st.set_page_config(
    page_title="Sistema de Metas - Mercado Covelo",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dicionário de meses em português (solução alternativa)
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# Função para formatar data em português
def formatar_mes_ano(data):
    try:
        # Garante que a data é um objeto datetime
        if not isinstance(data, pd.Timestamp):
            data = pd.to_datetime(data)
        
        return f"{MESES_PT[data.month]} {data.year}"
    except Exception as e:
        # Fallback caso algo dê errado
        try:
            return f"{MESES_PT[data.month]} {data.year}"
        except:
            return str(data)

# Função para formatar valores monetários
def formatar_moeda(valor):
    if isinstance(valor, (int, float)):
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return valor

# Estilos CSS personalizados - Versão Aprimorada
st.markdown("""
<style>
    :root {
        --primary-color: #2e7d32;
        --secondary-color: #4a4a4a;
        --adm-color: #1976d2;
        --comercial-color: #e65100;
        --success-color: #388e3c;
        --warning-color: #f57c00;
        --danger-color: #d32f2f;
        --light-bg: #f5f7fa;
        --card-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f9f9f9;
    }
    
    .header {
        font-size: 32px !important;
        font-weight: 700 !important;
        margin-bottom: 30px !important;
        color: var(--primary-color);
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 10px;
    }
    
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }
    
    .dashboard-title {
        font-size: 28px;
        font-weight: 600;
        color: var(--secondary-color);
    }
    
    .dashboard-date {
        font-size: 16px;
        color: #666;
        background: #f0f0f0;
        padding: 8px 15px;
        border-radius: 20px;
    }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: var(--card-shadow);
        border-top: 6px solid var(--primary-color);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        min-height: 200px;
        width: 100%;
    }
    
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: var(--secondary-color);
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .card-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--primary-color);
        margin: 15px 0;
        min-height: 50px;
    }
    
    .status-badge {
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: 600;
        display: inline-block;
        margin: 10px 0;
        min-width: 120px;
        text-align: center;
    }
    
    .card-metas {
        font-size: 12px;
        color: #666;
        margin: 5px 0;
        padding: 5px 10px;
        background: var(--light-bg);
        border-radius: 5px;
        width: 100%;
        text-align: center;
        min-height: 30px;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        margin-top: 20px;
        width: 100%;
    }
    
    .metric-item {
        background: var(--light-bg);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        min-height: 150px;
        transition: transform 0.3s ease;
    }
    
    .metric-item:hover {
        transform: translateY(-5px);
        box-shadow: var(--card-shadow);
    }
    
    .metric-title {
        font-size: 16px;
        color: var(--secondary-color);
        margin-bottom: 12px;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
        color: var(--primary-color);
        min-height: 40px;
    }
    
    .card-subvalue {
        font-size: 16px;
        color: #666;
        margin-bottom: 5px;
    }
    
    .status-badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        display: inline-block;
        margin-top: 10px;
    }
    
    .badge-success {
        background-color: var(--success-color);
        color: white;
    }
    
    .badge-warning {
        background-color: var(--warning-color);
        color: white;
    }
    
    .badge-danger {
        background-color: var(--danger-color);
        color: white;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-top: 15px;
    }
    
    .metric-item {
        background: var(--light-bg);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    
    .metric-title {
        font-size: 14px;
        color: var(--secondary-color);
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .total-card {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        border-radius: 15px;
        padding: 30px;
        margin: 30px 0;
        text-align: center;
        box-shadow: var(--card-shadow);
    }
    
    .total-title {
        font-size: 24px;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 15px;
    }
    
    .total-value {
        font-size: 42px;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 10px;
    }
    
    .total-subtitle {
        font-size: 16px;
        color: #666;
    }
    
    .setor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .setor-title {
        font-size: 20px;
        font-weight: 600;
    }
    
    .setor-title.adm {
        color: var(--adm-color);
    }
    
    .setor-title.comercial {
        color: var(--comercial-color);
    }
    
    .setor-total {
        font-size: 18px;
        font-weight: 600;
        color: #666;
        padding: 5px 10px;
        border-radius: 4px;
        margin-left: 10px;
    }
    
    .setor-total.adm {
        color: var(--adm-color);
        background-color: rgba(25, 118, 210, 0.1);
    }
    
    .setor-total.comercial {
        color: var(--comercial-color);
        background-color: rgba(230, 81, 0, 0.1);
    }
    
    .divider {
        height: 1px;
        background: #eee;
        margin: 25px 0;
    }
    
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1b5e20;
        transform: translateY(-2px);
    }
    
    .sidebar .sidebar-content {
        background: #f5f7fa;
    }
    
    .sidebar-title {
        font-size: 20px;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid #ddd;
    }
    
    .tab-content {
        padding: 15px 0;
    }
    
    /* Tooltip personalizado */
    [data-tooltip] {
        position: relative;
    }
    
    [data-tooltip]:hover:after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: #333;
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 100;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares
def load_data():
    if not os.path.exists('metas.csv'):
        cols = ['Mes', 'Meta_Comercial_Min', 'Meta_Comercial_Ideal', 'Meta_Comercial_Excelente',
               'Meta_Margem_Min', 'Meta_Margem_Ideal', 'Meta_Margem_Excelente',
               'Valor_Pago_Min_ADM', 'Valor_Pago_Ideal_ADM', 'Valor_Pago_Excelente_ADM',
               'Valor_Pago_Min_Comercial', 'Valor_Pago_Ideal_Comercial', 'Valor_Pago_Excelente_Comercial']
        pd.DataFrame(columns=cols).to_csv('metas.csv', index=False)
    
    if not os.path.exists('resultados.csv'):
        cols = ['Mes', 'Realizado_Comercial', 'Realizado_Margem']
        pd.DataFrame(columns=cols).to_csv('resultados.csv', index=False)
    
    # Verificar e atualizar colunas se necessário (migração)
    metas = pd.read_csv('metas.csv', parse_dates=['Mes'])
    if 'Valor_Pago_Min' in metas.columns and 'Valor_Pago_Min_ADM' not in metas.columns:
        # Migrar dados antigos para o novo formato
        metas['Valor_Pago_Min_ADM'] = metas['Valor_Pago_Min'] * 0.5  # 50% para ADM/Operacional
        metas['Valor_Pago_Ideal_ADM'] = metas['Valor_Pago_Ideal'] * 0.5
        metas['Valor_Pago_Excelente_ADM'] = metas['Valor_Pago_Excelente'] * 0.5
        
        metas['Valor_Pago_Min_Comercial'] = metas['Valor_Pago_Min'] * 0.5  # 50% para Comercial/Gerência
        metas['Valor_Pago_Ideal_Comercial'] = metas['Valor_Pago_Ideal'] * 0.5
        metas['Valor_Pago_Excelente_Comercial'] = metas['Valor_Pago_Excelente'] * 0.5
        
        # Remover colunas antigas
        metas = metas.drop(columns=['Valor_Pago_Min', 'Valor_Pago_Ideal', 'Valor_Pago_Excelente'], errors='ignore')