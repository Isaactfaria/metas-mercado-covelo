import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="Sistema de Metas - Mercado Covelo",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .header {
        font-size: 24px !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
        color: #2e7d32;
    }
    .payment-card {
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #2e7d32;
    }
    .metric-title {
        font-size: 16px;
        color: #555;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 20px;
        font-weight: bold;
    }
    .meta-info {
        font-size: 13px;
        color: #666;
        margin-top: 5px;
    }
    .status-badge {
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares
def load_data():
    if not os.path.exists('metas.csv'):
        cols = ['Mes', 'Meta_Comercial_Min', 'Meta_Comercial_Ideal', 'Meta_Comercial_Excelente',
               'Meta_Margem_Min', 'Meta_Margem_Ideal', 'Meta_Margem_Excelente',
               'Valor_Pago_Min', 'Valor_Pago_Ideal', 'Valor_Pago_Excelente']
        pd.DataFrame(columns=cols).to_csv('metas.csv', index=False)
    
    if not os.path.exists('resultados.csv'):
        cols = ['Mes', 'Realizado_Comercial', 'Realizado_Margem']
        pd.DataFrame(columns=cols).to_csv('resultados.csv', index=False)
    
    return pd.read_csv('metas.csv', parse_dates=['Mes']), pd.read_csv('resultados.csv', parse_dates=['Mes'])

def save_data(metas, resultados):
    metas.to_csv('metas.csv', index=False)
    resultados.to_csv('resultados.csv', index=False)

# Carregar dados
metas_df, resultados_df = load_data()

# Sidebar - Configuração
with st.sidebar:
    st.markdown("<div class='header'>⚙️ Configuração de Metas</div>", unsafe_allow_html=True)
    
    # Seletor de período
    col1, col2 = st.columns(2)
    with col1:
        ano = st.selectbox("Ano", range(2023, 2026))
    with col2:
        mes = st.selectbox("Mês", range(1, 13))
    data_meta = datetime(ano, mes, 1)
    
    # Metas Comerciais
    st.markdown("**💰 Metas Comerciais**")
    meta_min = st.number_input("Mínima (R$)", min_value=0.0, value=4000000.0, step=10000.0)
    meta_ideal = st.number_input("Ideal (R$)", min_value=0.0, value=4250000.0, step=10000.0)
    meta_excelente = st.number_input("Excelente (R$)", min_value=0.0, value=4500000.0, step=10000.0)
    
    # Metas de Margem
    st.markdown("**📈 Metas de Margem**")
    margem_min = st.number_input("Mínima (%)", min_value=0.0, max_value=100.0, value=24.0, step=0.1)
    margem_ideal = st.number_input("Ideal (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
    margem_excelente = st.number_input("Excelente (%)", min_value=0.0, max_value=100.0, value=26.0, step=0.1)
    
    # Valores a Pagar
    st.markdown("**💲 Valores a Pagar**")
    valor_min = st.number_input("Mínimo (R$)", min_value=0.0, value=100.0)
    valor_ideal = st.number_input("Ideal (R$)", min_value=0.0, value=300.0)
    valor_excelente = st.number_input("Excelente (R$)", min_value=0.0, value=500.0)
    
    if st.button("💾 Salvar Metas", use_container_width=True):
        nova_meta = {
            'Mes': data_meta,
            'Meta_Comercial_Min': meta_min,
            'Meta_Comercial_Ideal': meta_ideal,
            'Meta_Comercial_Excelente': meta_excelente,
            'Meta_Margem_Min': margem_min,
            'Meta_Margem_Ideal': margem_ideal,
            'Meta_Margem_Excelente': margem_excelente,
            'Valor_Pago_Min': valor_min,
            'Valor_Pago_Ideal': valor_ideal,
            'Valor_Pago_Excelente': valor_excelente
        }
        
        metas_df = metas_df[metas_df['Mes'] != data_meta]
        metas_df = pd.concat([metas_df, pd.DataFrame([nova_meta])], ignore_index=True)
        save_data(metas_df, resultados_df)
        st.success("Metas salvas com sucesso!")
        st.rerun()

# Página principal
st.markdown("<div class='header'>📊 Painel de Performance</div>", unsafe_allow_html=True)

# Seção de resultados
with st.container():
    st.markdown("**📤 Inserir Resultados**")
    
    if not metas_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            mes_selecionado = st.selectbox(
                "Selecione o mês",
                metas_df['Mes'].dt.strftime('%Y-%m'),
                key='select_mes'
            )
            data_resultado = pd.to_datetime(mes_selecionado)
        
        with col2:
            realizado_com = st.number_input("Vendas Realizadas (R$)", min_value=0.0, value=4290000.0, step=10000.0)
        
        realizado_margem = st.number_input("Margem Realizada (%)", min_value=0.0, max_value=100.0, value=24.44, step=0.01)
        
        if st.button("💾 Salvar Resultados", use_container_width=True):
            novo_resultado = {
                'Mes': data_resultado,
                'Realizado_Comercial': realizado_com,
                'Realizado_Margem': realizado_margem
            }
            
            resultados_df = resultados_df[resultados_df['Mes'] != data_resultado]
            resultados_df = pd.concat([resultados_df, pd.DataFrame([novo_resultado])], ignore_index=True)
            save_data(metas_df, resultados_df)
            st.success("Resultados salvos com sucesso!")
            st.rerun()

# Dashboard de Performance
if not resultados_df.empty and not metas_df.empty:
    try:
        dados = pd.merge(metas_df, resultados_df, on='Mes').sort_values('Mes', ascending=False)
        
        if not dados.empty:
            ultimo = dados.iloc[0]
            mes_formatado = ultimo['Mes'].strftime('%B %Y')
            
            # Cálculo dos status e pagamentos
            # Vendas
            if ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Excelente']:
                status_vendas = "✅ Excelente"
                pag_vendas = ultimo['Valor_Pago_Excelente']
                cor_status_vendas = "#2e7d32"
            elif ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Ideal']:
                status_vendas = "🟢 Ideal"
                pag_vendas = ultimo['Valor_Pago_Ideal']
                cor_status_vendas = "#388e3c"
            elif ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Min']:
                status_vendas = "🟡 Mínimo"
                pag_vendas = ultimo['Valor_Pago_Min']
                cor_status_vendas = "#f57c00"
            else:
                status_vendas = "🔴 Abaixo"
                pag_vendas = 0
                cor_status_vendas = "#d32f2f"
            
            # Margem
            if ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Excelente']:
                status_margem = "✅ Excelente"
                pag_margem = ultimo['Valor_Pago_Excelente']
                cor_status_margem = "#2e7d32"
            elif ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Ideal']:
                status_margem = "🟢 Ideal"
                pag_margem = ultimo['Valor_Pago_Ideal']
                cor_status_margem = "#388e3c"
            elif ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Min']:
                status_margem = "🟡 Mínimo"
                pag_margem = ultimo['Valor_Pago_Min']
                cor_status_margem = "#f57c00"
            else:
                status_margem = "🔴 Abaixo"
                pag_margem = 0
                cor_status_margem = "#d32f2f"
            
            total_pagamento = pag_vendas + pag_margem
            
            # Seção de Pagamento (DESTAQUE)
            with st.container():
                st.markdown(f"""
                <div class='payment-card'>
                    <div style='text-align: center; margin-bottom: 15px;'>
                        <h2>VALOR TOTAL A PAGAR</h2>
                        <h1 style='color: #2e7d32; margin: 10px 0;'>R$ {total_pagamento:,.2f}</h1>
                    </div>
                    <div style='display: flex; justify-content: space-around;'>
                        <div>
                            <span class='metric-title'>Vendas</span>
                            <div class='metric-value'>R$ {pag_vendas:,.2f}</div>
                            <span class='status-badge' style='background-color: {cor_status_vendas}; color: white;'>{status_vendas}</span>
                        </div>
                        <div>
                            <span class='metric-title'>Margem</span>
                            <div class='metric-value'>R$ {pag_margem:,.2f}</div>
                            <span class='status-badge' style='background-color: {cor_status_margem}; color: white;'>{status_margem}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Métricas de Performance (SIMPLIFICADO)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div style='margin-bottom: 20px;'>", unsafe_allow_html=True)
                st.markdown("<div class='metric-title'>💰 VENDAS COMERCIAIS</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>R$ {ultimo['Realizado_Comercial']:,.2f}</div>", unsafe_allow_html=True)
                
                st.markdown("""
                <div class='meta-info'>
                    <div>Mínima: R$ {min:,.2f}</div>
                    <div>Ideal: R$ {ideal:,.2f}</div>
                    <div>Excelente: R$ {excelente:,.2f}</div>
                </div>
                """.format(
                    min=ultimo['Meta_Comercial_Min'],
                    ideal=ultimo['Meta_Comercial_Ideal'],
                    excelente=ultimo['Meta_Comercial_Excelente']
                ), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div style='margin-bottom: 20px;'>", unsafe_allow_html=True)
                st.markdown("<div class='metric-title'>📈 MARGEM</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{ultimo['Realizado_Margem']:.2f}%</div>", unsafe_allow_html=True)
                
                st.markdown("""
                <div class='meta-info'>
                    <div>Mínima: {min:.2f}%</div>
                    <div>Ideal: {ideal:.2f}%</div>
                    <div>Excelente: {excelente:.2f}%</div>
                </div>
                """.format(
                    min=ultimo['Meta_Margem_Min'],
                    ideal=ultimo['Meta_Margem_Ideal'],
                    excelente=ultimo['Meta_Margem_Excelente']
                ), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Gráficos Simplificados
            st.markdown("---")
            st.markdown("### 📊 Análise Visual")
            
            # Gráfico de Vendas
            fig_vendas = px.bar(
                dados,
                x='Mes',
                y=['Realizado_Comercial', 'Meta_Comercial_Min', 'Meta_Comercial_Ideal', 'Meta_Comercial_Excelente'],
                title="Vendas Comerciais vs Metas",
                labels={'value': 'Valor (R$)', 'variable': 'Tipo'},
                barmode='group',
                color_discrete_sequence=['#4CAF50', '#FFC107', '#2196F3', '#9C27B0']
            )
            fig_vendas.update_layout(legend_title_text='')
            st.plotly_chart(fig_vendas, use_container_width=True)
            
            # Gráfico de Margem
            fig_margem = px.bar(
                dados,
                x='Mes',
                y=['Realizado_Margem', 'Meta_Margem_Min', 'Meta_Margem_Ideal', 'Meta_Margem_Excelente'],
                title="Margem vs Metas",
                labels={'value': 'Percentual (%)', 'variable': 'Tipo'},
                barmode='group',
                color_discrete_sequence=['#4CAF50', '#FFC107', '#2196F3', '#9C27B0']
            )
            fig_margem.update_layout(legend_title_text='')
            st.plotly_chart(fig_margem, use_container_width=True)
    
    except Exception as e:
        st.error(f"Erro ao processar dados: {str(e)}")
else:
    st.info("ℹ️ Configure as metas e insira resultados para visualizar o dashboard")