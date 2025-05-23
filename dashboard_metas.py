import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import locale
import streamlit.components.v1 as components

# Configuração da página DEVE SER A PRIMEIRA COISA NO SCRIPT
st.set_page_config(
    page_title="Sistema de Metas - Mercado Covelo",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração robusta do locale para português
try:
    # Tenta configurar o locale
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Portuguese')
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_TIME, '')  # Usa o locale padrão do sistema
                except locale.Error:
                    locale.setlocale(locale.LC_TIME, 'C')  # Fallback para locale padrão do sistema
                    st.warning("Locale pt_BR não encontrado, usando sistema alternativo")
                    st.info("Os meses serão exibidos em português usando o dicionário MESES_PT")

# Dicionário de meses em português (solução alternativa)
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# Função para formatar data em português usando MESES_PT
def formatar_mes_ano(data):
    try:
        # Garante que a data é um objeto datetime
        if not isinstance(data, pd.Timestamp):
            data = pd.to_datetime(data)
        
        # Usa o dicionário MESES_PT para garantir que o mês sempre apareça em português
        return f"{MESES_PT[data.month]} {data.year}"
    except:
        return f"{MESES_PT.get(data.month, 'Mês Desconhecido')} {data.year}"

# Adicionar script de seleção automática para campos de número
st.markdown("""
<script>
    // Função para selecionar o conteúdo do campo
    function autoSelectInput(event) {
        if (event.target.type === 'number') {
            event.target.select();
        }
    }

    // Adicionar evento de clique para todos os campos de número
    document.addEventListener('DOMContentLoaded', function() {
        // Adicionar evento de clique para campos existentes
        const numberInputs = document.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.addEventListener('click', autoSelectInput);
        });

        // Adicionar evento de mutação para novos campos
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1 && node.querySelector('input[type="number"]')) {
                            const newInputs = node.querySelectorAll('input[type="number"]');
                            newInputs.forEach(input => {
                                input.addEventListener('click', autoSelectInput);
                            });
                        }
                    });
                }
            });
        });

        // Observar mudanças no DOM
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
</script>
""", unsafe_allow_html=True)

# Configuração robusta do locale para português
try:
    # Tenta configurar o locale
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Portuguese')
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_TIME, '')  # Usa o locale padrão do sistema
                except locale.Error:
                    locale.setlocale(locale.LC_TIME, 'C')  # Fallback para locale padrão do sistema
                    st.warning("Locale pt_BR não encontrado, usando sistema alternativo")
                    st.info("Os meses serão exibidos em português usando o dicionário MESES_PT")

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

# Função para formatar data em português
def formatar_mes_ano(data):
    # Garante que a data é um objeto datetime
    if not isinstance(data, pd.Timestamp):
        data = pd.to_datetime(data)
    
    # Usa locale para formatar a data
    return data.strftime('%B %Y').title()

# Função para formatar valores monetários
def formatar_moeda(valor):
    # Formata o valor com separador de milhar (.) e decimal (,)
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Função auxiliar para formatar DataFrame com meses em português
def formatar_dataframe(df):
    if 'Mes' in df.columns:
        # Ordena por data original
        df = df.sort_values('Mes', ascending=False)
    return df

# Funções auxiliares (mantidas as mesmas)
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
        
        # Salvar o arquivo atualizado
        metas.to_csv('metas.csv', index=False)
    
    resultados = pd.read_csv('resultados.csv', parse_dates=['Mes'])
    
    # Garantir que as datas estão no mesmo formato
    metas['Mes'] = pd.to_datetime(metas['Mes']).dt.normalize()
    resultados['Mes'] = pd.to_datetime(resultados['Mes']).dt.normalize()
    
    # Formatar os DataFrames para exibir meses em português
    metas = formatar_dataframe(metas)
    resultados = formatar_dataframe(resultados)
    
    # Garantir que a coluna Mes_formatado existe em ambos os DataFrames
    if 'Mes_formatado' not in metas.columns:
        metas['Mes_formatado'] = metas['Mes'].apply(formatar_mes_ano)
    if 'Mes_formatado' not in resultados.columns:
        resultados['Mes_formatado'] = resultados['Mes'].apply(formatar_mes_ano)
    
    return metas, resultados

def save_data(metas, resultados):
    metas.to_csv('metas.csv', index=False)
    resultados.to_csv('resultados.csv', index=False)

# Carregar dados
metas_df, resultados_df = load_data()

# Sidebar - Configuração (melhorada visualmente)
with st.sidebar:
    st.markdown("<div class='sidebar-title'>⚙️ Configuração de Metas</div>", unsafe_allow_html=True)
    
    # Seletor de período
    st.markdown("**📅 Período**")
    col1, col2 = st.columns(2)
    with col1:
        ano = st.selectbox("Ano", range(2023, 2027))
    with col2:
        mes_nome = st.selectbox("Mês", list(MESES_PT.values()))
        mes_numero = list(MESES_PT.keys())[list(MESES_PT.values()).index(mes_nome)]
    
    data_meta = datetime(ano, mes_numero, 1)
    
    # Abas para organização
    tab1, tab2, tab3 = st.tabs(["💰 Vendas", "📈 Margem", "💲 Pagamentos"])
    
    with tab1:
        st.markdown("**Metas Comerciais**")
        meta_min = st.number_input("Mínima (R$)", min_value=0.0, value=4000000.0, step=10000.0, key="meta_min")
        meta_ideal = st.number_input("Ideal (R$)", min_value=0.0, value=4250000.0, step=10000.0, key="meta_ideal")
        meta_excelente = st.number_input("Excelente (R$)", min_value=0.0, value=4500000.0, step=10000.0, key="meta_excelente")
    
    with tab2:
        st.markdown("**Metas de Margem**")
        margem_min = st.number_input("Mínima (%)", min_value=0.0, max_value=100.0, value=24.0, step=0.1, key="margem_min")
        margem_ideal = st.number_input("Ideal (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.1, key="margem_ideal")
        margem_excelente = st.number_input("Excelente (%)", min_value=0.0, max_value=100.0, value=26.0, step=0.1, key="margem_excelente")
    
    with tab3:
        st.markdown("**Valores a Pagar - ADM/Operacional**")
        valor_min_adm = st.number_input("Mínimo - ADM (R$)", min_value=0.0, value=50.0, key="valor_min_adm")
        valor_ideal_adm = st.number_input("Ideal - ADM (R$)", min_value=0.0, value=150.0, key="valor_ideal_adm")
        valor_excelente_adm = st.number_input("Excelente - ADM (R$)", min_value=0.0, value=250.0, key="valor_excelente_adm")
        
        st.markdown("**Valores a Pagar - Comercial/Gerência**")
        valor_min_comercial = st.number_input("Mínimo - Comercial (R$)", min_value=0.0, value=50.0, key="valor_min_comercial")
        valor_ideal_comercial = st.number_input("Ideal - Comercial (R$)", min_value=0.0, value=150.0, key="valor_ideal_comercial")
        valor_excelente_comercial = st.number_input("Excelente - Comercial (R$)", min_value=0.0, value=250.0, key="valor_excelente_comercial")
    
    if st.button("💾 Salvar Metas", use_container_width=True, key="save_metas"):
        nova_meta = {
            'Mes': data_meta,
            'Meta_Comercial_Min': meta_min,
            'Meta_Comercial_Ideal': meta_ideal,
            'Meta_Comercial_Excelente': meta_excelente,
            'Meta_Margem_Min': margem_min,
            'Meta_Margem_Ideal': margem_ideal,
            'Meta_Margem_Excelente': margem_excelente,
            'Valor_Pago_Min_ADM': valor_min_adm,
            'Valor_Pago_Ideal_ADM': valor_ideal_adm,
            'Valor_Pago_Excelente_ADM': valor_excelente_adm,
            'Valor_Pago_Min_Comercial': valor_min_comercial,
            'Valor_Pago_Ideal_Comercial': valor_ideal_comercial,
            'Valor_Pago_Excelente_Comercial': valor_excelente_comercial
        }
        
        metas_df = metas_df[metas_df['Mes'] != pd.to_datetime(data_meta).normalize()]
        metas_df = pd.concat([metas_df, pd.DataFrame([nova_meta])], ignore_index=True)
        save_data(metas_df, resultados_df)
        st.success("Metas salvas com sucesso!")
        st.rerun()

# Página principal - Layout aprimorado
st.markdown("<div class='header'>📊 Painel de Performance</div>", unsafe_allow_html=True)

# Seção de resultados - Mais organizada
with st.expander("📤 Inserir Resultados", expanded=True):
    if not metas_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            opcoes_meses = [formatar_mes_ano(dt) for dt in metas_df['Mes'].unique()]
            mes_selecionado = st.selectbox(
                "Selecione o mês",
                opcoes_meses,
                key='select_mes'
            )
            try:
                data_resultado = pd.to_datetime(mes_selecionado, format='%B %Y').normalize()
            except:
                data_resultado = metas_df['Mes'].iloc[0]
        
        with col2:
            realizado_atual = resultados_df[resultados_df['Mes'] == data_resultado]['Realizado_Comercial']
            valor_inicial = float(realizado_atual.values[0]) if not realizado_atual.empty else 0.0
            
            # Campos de input com seleção automática usando o componente personalizado
            vendas_realizadas = st.number_input(
                "Vendas Realizadas (R$)",
                min_value=0.0,
                value=valor_inicial,
                step=10000.0
            )
    
        margem_atual = resultados_df[resultados_df['Mes'] == data_resultado]['Realizado_Margem']
        margem_inicial = float(margem_atual.values[0]) if not margem_atual.empty else 0.0
        margem_realizada = st.number_input(
            "Margem Realizada (%)",
            min_value=0.0,
            max_value=100.0,
            value=margem_inicial,
            step=0.01
        )
        
        if st.button("💾 Salvar Resultados", use_container_width=True, key="save_resultados"):
            novo_resultado = {
                'Mes': data_resultado,
                'Realizado_Comercial': vendas_realizadas,
                'Realizado_Margem': margem_realizada
            }
            
            resultados_df = resultados_df[resultados_df['Mes'] != data_resultado]
            resultados_df = pd.concat([resultados_df, pd.DataFrame([novo_resultado])], ignore_index=True)
            save_data(metas_df, resultados_df)
            st.success("Resultados salvos com sucesso!")
            st.rerun()

# Dashboard de Performance - Versão Aprimorada
def processar_dados():
    try:
        if not resultados_df.empty and not metas_df.empty:
            # Fazer o merge dos dados
            dados = pd.merge(metas_df, resultados_df, on='Mes', how='left').sort_values('Mes', ascending=False)
            
            # Obter o mês selecionado
            mes_selecionado = st.session_state.select_mes if 'select_mes' in st.session_state else None
            
            try:
                data_selecionada = pd.to_datetime(mes_selecionado, format='%B %Y').normalize() if mes_selecionado else None
            except:
                data_selecionada = dados['Mes'].iloc[0]
            
            if data_selecionada is not None and data_selecionada in dados['Mes'].values:
                dados_filtrados = dados[dados['Mes'] == data_selecionada]
                if not dados_filtrados.empty:
                    ultimo = dados_filtrados.iloc[0]
                else:
                    ultimo = dados.iloc[0]
                    st.warning(f"Dados não encontrados para {mes_selecionado}, mostrando {formatar_mes_ano(ultimo['Mes'])}")
            else:
                ultimo = dados.iloc[0]
            
            mes_formatado = formatar_mes_ano(ultimo['Mes'])
            
            # Cálculo dos status e pagamentos (mantido igual)
            if ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Excelente']:
                status_vendas = "Excelente"
                status_vendas_class = "badge-success"
                pag_vendas_adm = ultimo['Valor_Pago_Excelente_ADM']
                pag_vendas_comercial = ultimo['Valor_Pago_Excelente_Comercial']
            elif ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Ideal']:
                status_vendas = "Ideal"
                status_vendas_class = "badge-success"
                pag_vendas_adm = ultimo['Valor_Pago_Ideal_ADM']
                pag_vendas_comercial = ultimo['Valor_Pago_Ideal_Comercial']
            elif ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Min']:
                status_vendas = "Mínimo"
                status_vendas_class = "badge-warning"
                pag_vendas_adm = ultimo['Valor_Pago_Min_ADM']
                pag_vendas_comercial = ultimo['Valor_Pago_Min_Comercial']
            else:
                status_vendas = "Não atingido"
                status_vendas_class = "badge-danger"
                pag_vendas_adm = 0
                pag_vendas_comercial = 0
            
            if ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Excelente']:
                status_margem = "Excelente"
                status_margem_class = "badge-success"
                pag_margem_adm = ultimo['Valor_Pago_Excelente_ADM']
                pag_margem_comercial = ultimo['Valor_Pago_Excelente_Comercial']
            elif ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Ideal']:
                status_margem = "Ideal"
                status_margem_class = "badge-success"
                pag_margem_adm = ultimo['Valor_Pago_Ideal_ADM']
                pag_margem_comercial = ultimo['Valor_Pago_Ideal_Comercial']
            elif ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Min']:
                status_margem = "Mínimo"
                status_margem_class = "badge-warning"
                pag_margem_adm = ultimo['Valor_Pago_Min_ADM']
                pag_margem_comercial = ultimo['Valor_Pago_Min_Comercial']
            else:
                status_margem = "Não atingido"
                status_margem_class = "badge-danger"
                pag_margem_adm = 0
                pag_margem_comercial = 0
            
            total_adm = pag_vendas_adm + pag_margem_adm
            total_comercial = pag_vendas_comercial + pag_margem_comercial
            total_pagamento = total_adm + total_comercial
            
            # Header do dashboard
            st.markdown(f"""
            <div class='dashboard-header'>
                <div class='dashboard-title'>Resumo de Performance</div>
                <div class='dashboard-date' data-tooltip='Período de análise'>{mes_formatado}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Seção de Pagamento - Destaque Total
            st.markdown(f"""
            <div class='total-card'>
                <div class='total-title'>VALOR TOTAL A PAGAR</div>
                <div class='total-value'>R$ {formatar_moeda(total_pagamento)}</div>
                <div class='total-subtitle'>Distribuição entre os setores</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Cards de performance
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📊 Performance Comercial</div>
                    <div class="card-value">R$ {formatar_moeda(float(ultimo['Realizado_Comercial']))}</div>
                    <div class="status-badge {status_vendas_class}">{status_vendas}</div>
                    <div class="card-metas">Mínimo: R$ {formatar_moeda(float(ultimo['Meta_Comercial_Min']))}</div>
                    <div class="card-metas">Ideal: R$ {formatar_moeda(float(ultimo['Meta_Comercial_Ideal']))}</div>
                    <div class="card-metas">Excelente: R$ {formatar_moeda(float(ultimo['Meta_Comercial_Excelente']))}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>📉 Performance de Margem</div>
                    <div class='card-value'>{formatar_moeda(float(ultimo['Realizado_Margem']))}%</div>
                    <div class='status-badge {status_margem_class}'>{status_margem}</div>
                    <div class='card-metas'>Mínimo: {formatar_moeda(float(ultimo['Meta_Margem_Min']))}%</div>
                    <div class='card-metas'>Ideal: {formatar_moeda(float(ultimo['Meta_Margem_Ideal']))}%</div>
                    <div class='card-metas'>Excelente: {formatar_moeda(float(ultimo['Meta_Margem_Excelente']))}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Divisão visual
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # Seção por setor
            st.markdown("### 💼 Distribuição por Setor")
            
            # Card ADM
            st.markdown(f"""
            <div class='card'>
                <div class='setor-header'>
                    <div class='setor-title adm'>👥 ADM/OPERACIONAL</div>
                    <div class='setor-total adm'>Total: R$ {formatar_moeda(total_adm)}</div>
                </div>
                <div class='metric-grid'>
                    <div class='metric-item'>
                        <div class='metric-title'>Pagamento por Vendas</div>
                        <div class='metric-value'>R$ {formatar_moeda(pag_vendas_adm)}</div>
                        <div class='status-badge {status_vendas_class}'>{status_vendas}</div>
                    </div>
                    <div class='metric-item'>
                        <div class='metric-title'>Pagamento por Margem</div>
                        <div class='metric-value'>R$ {formatar_moeda(pag_margem_adm)}</div>
                        <div class='status-badge {status_margem_class}'>{status_margem}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Card Comercial
            st.markdown(f"""
            <div class='card'>
                <div class='setor-header'>
                    <div class='setor-title comercial'>👔 COMERCIAL/GERÊNCIA</div>
                    <div class='setor-total comercial'>Total: R$ {formatar_moeda(total_comercial)}</div>
                </div>
                <div class='metric-grid'>
                    <div class='metric-item'>
                        <div class='metric-title'>Pagamento por Vendas</div>
                        <div class='metric-value'>R$ {formatar_moeda(pag_vendas_comercial)}</div>
                        <div class='status-badge {status_vendas_class}'>{status_vendas}</div>
                    </div>
                    <div class='metric-item'>
                        <div class='metric-title'>Pagamento por Margem</div>
                        <div class='metric-value'>R$ {formatar_moeda(pag_margem_comercial)}</div>
                        <div class='status-badge {status_margem_class}'>{status_margem}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gráfico de comparação
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("### 📊 Comparação entre Setores")
            
            dados_pagamentos = pd.DataFrame({
                'Setor': ['ADM/Operacional', 'Comercial/Gerência'],
                'Pagamento Total': [total_adm, total_comercial],
                'Pagamento Vendas': [pag_vendas_adm, pag_vendas_comercial],
                'Pagamento Margem': [pag_margem_adm, pag_margem_comercial]
            })
            
            fig_pagamentos = px.bar(
                dados_pagamentos,
                x='Setor',
                y=['Pagamento Vendas', 'Pagamento Margem'],
                title="Distribuição de Pagamentos por Setor",
                labels={'value': 'Valor (R$)', 'variable': 'Tipo'},
                barmode='group',
                color_discrete_sequence=['#1976d2', '#e65100']
            )
            fig_pagamentos.update_layout(
                legend_title_text='',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig_pagamentos, use_container_width=True)
            

        else:
            st.warning("Nenhum dado encontrado para processar.")
    except Exception as e:
        st.error(f"Erro ao processar os dados: {str(e)}")

# Chamar a função principal
processar_dados()

# Adicionar versão no rodapé
st.markdown("""
<div style='text-align: center; margin-top: 20px; color: #666; font-size: 12px;'>
Versão 1.2.2.4
</div>
""", unsafe_allow_html=True)