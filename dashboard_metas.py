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

# Dados de usuários e senhas (em produção, esses dados devem ser armazenados de forma segura)
USERS = {
    'cristiano': 'C123456',
    'dandara': 'D123456',
    'adriana': 'A123456',
    'carla': 'C123456'
}

# Tela de login
if not st.session_state.get('user_authenticated', False):
    st.title('Sistema de Metas - Mercado Covelo')
    
    with st.form('login_form'):
        st.markdown('### Faça login para continuar')
        username = st.text_input('Usuário')
        password = st.text_input('Senha', type='password')
        submit = st.form_submit_button('Entrar')

        if submit:
            if username in USERS and password == USERS[username]:
                st.success('Login realizado com sucesso!')
                st.session_state['user_authenticated'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error('Usuário ou senha incorretos')
    
    # Se não está autenticado, para aqui
    st.stop()

# Se chegou aqui, o usuário está autenticado
st.title('Sistema de Metas - Mercado Covelo')

# Mostrar nome do usuário logado
st.sidebar.markdown(f"**Usuário:** {st.session_state['username']}")



# Se o usuário está autenticado, mostra o dashboard
if st.session_state.get('user_authenticated', False):
    # Configuração robusta do locale para português
    try:
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
                        locale.setlocale(locale.LC_TIME, '')
                    except locale.Error:
                        locale.setlocale(locale.LC_TIME, 'C')
                        st.warning("Locale pt_BR não encontrado, usando sistema alternativo")
                        st.info("Os meses serão exibidos em português usando o dicionário MESES_PT")

    # Dicionário de meses em português (solução alternativa)
    MESES_PT = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    # Funções auxiliares
    def formatar_mes_ano(data):
        """Formata data em português usando MESES_PT"""
        try:
            if not isinstance(data, pd.Timestamp):
                data = pd.to_datetime(data)
            return f"{MESES_PT[data.month]} {data.year}"
        except:
            return f"{MESES_PT.get(data.month, 'Mês Desconhecido')} {data.year}"

    def formatar_moeda(valor):
        """Formata valor monetário no padrão brasileiro"""
        return f"R$ {valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

    # Funções principais
    def load_data():
        """Carrega os dados do sistema"""
        return pd.DataFrame(), pd.DataFrame()

    def save_data(metas, resultados):
        """Salva os dados do sistema"""
        pass

    def processar_dados():
        """Processa e exibe os dados do dashboard"""
        pass

    # Carregar dados
    metas_df, resultados_df = load_data()

    # Exibir tabela de funcionários filtrados
    funcionarios_filtrados = pd.DataFrame()  # Substituir com a tabela de funcionários filtrados
    if not funcionarios_filtrados.empty:
        # Criar uma visualização mais compacta para a sidebar
        st.markdown("<style>.funcionario-item {padding: 5px; border-bottom: 1px solid #eee;}</style>", unsafe_allow_html=True)
        
        for _, funcionario in funcionarios_filtrados.iterrows():
            status = "✅" if funcionario['Ativo'] else "❌"
            with st.container():
                cols = st.columns([1, 4, 3, 1])
                with cols[0]:
                    st.markdown(f"<div class='funcionario-item'>{status}</div>", unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"<div class='funcionario-item'>{funcionario['Nome']}</div>", unsafe_allow_html=True)
                with cols[2]:
                    st.markdown(f"<div class='funcionario-item'>{funcionario['Cargo']}</div>", unsafe_allow_html=True)
                with cols[3]:
                    if st.button("✏️", key=f"edit_{funcionario['Nome']}"):
                        st.session_state.editando_funcionario = funcionario['Nome']
                        st.rerun()
                    
                    if st.button("🗑️", key=f"del_{funcionario['Nome']}"):
                        if st.button("✅ Confirmar", key=f"confirm_del_{funcionario['Nome']}"):
                            st.session_state.funcionarios_df = st.session_state.funcionarios_df[st.session_state.funcionarios_df['Nome'] != funcionario['Nome']]
                            save_funcionarios(st.session_state.funcionarios_df)
                            st.rerun()
    else:
        st.info("Nenhum funcionário encontrado com os filtros selecionados.")

    # Chamar a função principal
    processar_dados()

    # Adicionar script de seleção automática para campos de número
    st.markdown("""
    <script>
        // Função para selecionar o conteúdo do campo
        function autoSelectInput(event) {
            if (event.target.type === 'number') {
                event.target.select();
            }
        }

        // Adiciona o evento de clique para todos os campos de número
        document.addEventListener('DOMContentLoaded', function() {
            const numberInputs = document.querySelectorAll('input[type="number"]');
            numberInputs.forEach(input => {
                input.addEventListener('click', autoSelectInput);
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
    if 'Mes' in df.columns and 'Mes_formatado' not in df.columns:
        df['Mes_formatado'] = df['Mes'].apply(formatar_mes_ano)
    return df

def render_employee_list(employees, setor):
    """Renderiza a lista de funcionários dentro do card do setor"""
    # Define cores e nomes de exibição baseados no setor
    setor_info = {
        'ADM': {
            'display_name': 'ADM/OPERACIONAL',
            'icon': '👥',
            'border': '#3498db',
            'bg': '#f0f8ff',
            'header_bg': '#e3f2fd'
        },
        'Comercial': {
            'display_name': 'COMERCIAL/GERÊNCIA',
            'icon': '👔',
            'border': '#2ecc71',
            'bg': '#f0fdf4',
            'header_bg': '#dcfce7'
        }
    }
    
    # Usa as informações do setor ou padrão
    setor_data = setor_info.get(setor, {
        'display_name': setor,
        'icon': '👤',
        'border': '#e0e0e0',
        'bg': '#fafafa',
        'header_bg': '#f5f5f5'
    })
    
    # Extrai as cores para facilitar o uso
    colors = {
        'border': setor_data['border'],
        'bg': setor_data['bg'],
        'header_bg': setor_data['header_bg']
    }
    
    if not employees:
        st.markdown(f"""
        <div style='
            padding: 12px;
            background: {colors['bg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            color: #666;
            text-align: center;
            margin: 8px 0;
            font-size: 0.95em;
        '>
            Nenhum funcionário ativo neste setor
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Container principal da lista de funcionários
    st.markdown(f"""
    <div style='
        border: 1px solid {colors['border']};
        border-radius: 8px;
        overflow: hidden;
        margin: 15px 0 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    '>
        <div style='
            background: {colors['header_bg']};
            padding: 10px 15px;
            border-bottom: 1px solid {colors['border']};
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            color: #2c3e50;
        '>
            <span>{setor_data['icon']} {setor_data['display_name']} ({len(employees)} {'' if len(employees) == 1 else 'membros'})</span>
            <span>Total: <strong>{formatar_moeda(sum(emp['total'] for emp in employees))}</strong></span>
        </div>
    """, unsafe_allow_html=True)
    
    # Cabeçalho das colunas
    st.markdown("""
    <div style='
        display: grid;
        grid-template-columns: 1.5fr 1fr 1fr 1fr;
        gap: 10px;
        padding: 12px 15px;
        font-weight: 600;
        font-size: 0.9em;
        color: #5d6d7e;
        background: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
    '>
        <div>Funcionário</div>
        <div style='text-align: right;'>Vendas</div>
        <div style='text-align: right;'>Margem</div>
        <div style='text-align: right;'>Total</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Container para a lista de funcionários
    with st.container():
        st.markdown("<div style='max-height: 300px; overflow-y: auto; padding: 0 5px 10px 5px;'>", unsafe_allow_html=True)
        
        for i, emp in enumerate(employees):
            # Garantir que os valores existam no dicionário
            vendas = emp.get('vendas', 0)
            margem = emp.get('margem', 0)
            total = emp.get('total', 0)
            
            # Alterna o fundo para melhor legibilidade
            bg_color = '#ffffff' if i % 2 == 0 else '#f8fafc'
            
            st.markdown(f"""
            <div style='
                display: grid;
                grid-template-columns: 1.5fr 1fr 1fr 1fr;
                gap: 10px;
                align-items: center;
                padding: 10px 15px;
                background: {bg_color};
                font-size: 0.95em;
                transition: all 0.2s ease;
                border-bottom: 1px solid #f1f5f9;
            ' 
            onmouseover="this.style.backgroundColor='#f1f7fe'" 
            onmouseout="this.style.backgroundColor='{bg_color}'"
            >
                <div>
                    <div style='font-weight: 500;'>{emp['nome']}</div>
                    <div style='color: #7f8c8d; font-size: 0.85em;'>{emp['cargo']}</div>
                </div>
                <div style='text-align: right; color: #2980b9;'>
                    {formatar_moeda(vendas) if vendas else 'R$ 0,00'}
                </div>
                <div style='text-align: right; color: #e67e22;'>
                    {formatar_moeda(margem) if margem else 'R$ 0,00'}
                </div>
                <div style='text-align: right; font-weight: 600; color: #27ae60;'>
                    {formatar_moeda(total) if total else 'R$ 0,00'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Fechar o container principal
        st.markdown("</div>", unsafe_allow_html=True)

def render_aba_funcionarios():
    """Renderiza a aba de gerenciamento de funcionários"""
    # Inicializar o DataFrame de funcionários se não existir
    if 'funcionarios_df' not in st.session_state:
        st.session_state.funcionarios_df = load_funcionarios()
    
    # Título e métricas
    st.markdown("## 👥 Gerenciamento de Funcionários")
    
    # Seção de métricas
    total_funcionarios = len(st.session_state.funcionarios_df)
    ativos = len(st.session_state.funcionarios_df[st.session_state.funcionarios_df['Ativo'] == True])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Funcionários", total_funcionarios)
    with col2:
        st.metric("Funcionários Ativos", ativos)
    
    st.markdown("---")
    
    # Seção de adicionar/editar funcionário
    if 'editando_funcionario' in st.session_state and st.session_state.editando_funcionario is not None:
        # Modo de edição
        with st.form("form_editar_funcionario"):
            st.markdown("### ✏️ Editar Funcionário")
            
            idx = st.session_state.editando_funcionario
            
            # Verificar se o índice é válido
            if idx < 0 or idx >= len(st.session_state.funcionarios_df):
                st.error("Erro: Funcionário não encontrado.")
                del st.session_state.editando_funcionario
                st.rerun()
                
            funcionario = st.session_state.funcionarios_df.iloc[idx]
            
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome", value=funcionario['Nome'], key="editar_nome")
            with col2:
                novo_cargo = st.text_input("Cargo", value=funcionario['Cargo'], key="editar_cargo")
            
            novo_setor = st.selectbox(
                "Setor", 
                ["Comercial", "ADM"],
                index=0 if funcionario['Setor'] == 'Comercial' else 1,
                key="editar_setor"
            )
            
            ativo = st.checkbox("Ativo", value=bool(funcionario['Ativo']), key="editar_ativo")
            
            # Botões fora do with col para evitar duplicação
            submitted = st.form_submit_button("💾 Salvar Alterações")
            canceled = st.form_submit_button("❌ Cancelar")
            
            if submitted:
                if novo_nome and novo_cargo:
                    st.session_state.funcionarios_df.at[idx, 'Nome'] = novo_nome
                    st.session_state.funcionarios_df.at[idx, 'Cargo'] = novo_cargo
                    st.session_state.funcionarios_df.at[idx, 'Setor'] = novo_setor
                    st.session_state.funcionarios_df.at[idx, 'Ativo'] = ativo
                    save_funcionarios(st.session_state.funcionarios_df)
                    del st.session_state.editando_funcionario
                    st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios.")
            
            if canceled:
                del st.session_state.editando_funcionario
                st.rerun()
    else:
        # Modo de adição
        with st.form("form_adicionar_funcionario"):
            st.markdown("### ➕ Adicionar Novo Funcionário")
            
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome", key="novo_nome")
            with col2:
                novo_cargo = st.text_input("Cargo", key="novo_cargo")
            
            novo_setor = st.selectbox(
                "Setor", 
                ["Comercial", "ADM"],
                key="novo_setor"
            )
            
            if st.form_submit_button("Adicionar Funcionário"):
                if novo_nome and novo_cargo:
                    novo_funcionario = pd.DataFrame({
                        'Nome': [novo_nome],
                        'Cargo': [novo_cargo],
                        'Setor': [novo_setor],
                        'Ativo': [True]
                    })
                    st.session_state.funcionarios_df = pd.concat(
                        [st.session_state.funcionarios_df, novo_funcionario], 
                        ignore_index=True
                    )
                    save_funcionarios(st.session_state.funcionarios_df)
                    st.success("Funcionário adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios.")
    
    st.markdown("---")
    
    # Seção de lista de funcionários
    st.markdown("### 📋 Lista de Funcionários")
    
    # Filtros em linhas separadas para evitar colunas no sidebar
    filtro_setor = st.selectbox(
        "Filtrar por setor",
        ["Todos"] + st.session_state.funcionarios_df['Setor'].unique().tolist(),
        key="filtro_setor"
    )
    filtro_status = st.selectbox(
        "Filtrar por status",
        ["Todos", "Ativos", "Inativos"],
        key="filtro_status"
    )
    
    # Aplicar filtros
    funcionarios_filtrados = st.session_state.funcionarios_df.copy()
    if filtro_setor != "Todos":
        funcionarios_filtrados = funcionarios_filtrados[funcionarios_filtrados['Setor'] == filtro_setor]
    if filtro_status == "Ativos":
        funcionarios_filtrados = funcionarios_filtrados[funcionarios_filtrados['Ativo'] == True]
    elif filtro_status == "Inativos":
        funcionarios_filtrados = funcionarios_filtrados[funcionarios_filtrados['Ativo'] == False]
    
    # Exibir a tabela de funcionários
    if len(funcionarios_filtrados) > 0:
        # Usar um contêiner para cada funcionário com botões nativos do Streamlit
        for idx, row in funcionarios_filtrados.iterrows():
            status = "✅" if row['Ativo'] else "❌"
            
            # Criar uma coluna para cada linha de funcionário
            col1, col2, col3 = st.columns([6, 1, 1])
            
            with col1:
                st.markdown(f"**{row['Nome']}** - {row['Cargo']} ({row['Setor']}) {status}")
                
            # Botão de editar
            with col2:
                if st.button("✏️", key=f"editar_{idx}"):
                    st.session_state.editando_funcionario = idx
                    st.rerun()
                    
            # Botão de excluir
            with col3:
                if st.button("🗑️", key=f"excluir_{idx}"):
                    st.session_state.excluir_funcionario = idx
                    st.rerun()
            
            # Linha divisória
            st.markdown("---")
        
        # Processar exclusão em um formulário separado
        if 'excluir_funcionario' in st.session_state and st.session_state.excluir_funcionario is not None:
            with st.form("form_confirmar_exclusao"):
                idx = st.session_state.excluir_funcionario
                if 0 <= idx < len(st.session_state.funcionarios_df):
                    nome = st.session_state.funcionarios_df.iloc[idx]['Nome']
                    st.warning(f"Tem certeza que deseja excluir o funcionário {nome}?")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("✅ Confirmar"):
                            st.session_state.funcionarios_df = st.session_state.funcionarios_df.drop(
                                index=idx).reset_index(drop=True)
                            save_funcionarios(st.session_state.funcionarios_df)
                            st.success(f"Funcionário {nome} excluído com sucesso!")
                            if 'excluir_funcionario' in st.session_state:
                                del st.session_state.excluir_funcionario
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("❌ Cancelar"):
                            if 'excluir_funcionario' in st.session_state:
                                del st.session_state.excluir_funcionario
                            st.rerun()
                else:
                    st.error("Erro: Funcionário não encontrado.")
                    if 'excluir_funcionario' in st.session_state:
                        del st.session_state.excluir_funcionario
                    st.rerun()
    else:
        st.info("Nenhum funcionário encontrado com os filtros selecionados.")
    
    # Atualizar contagem de funcionários ativos na sessão
    funcionarios_ativos = st.session_state.funcionarios_df[st.session_state.funcionarios_df['Ativo'] == True]
    st.session_state.qtd_comercial = len(funcionarios_ativos[funcionarios_ativos['Setor'] == 'Comercial'])
    st.session_state.qtd_adm = len(funcionarios_ativos[funcionarios_ativos['Setor'] == 'ADM'])
    st.session_state.qtd_comercial = len(funcionarios_ativos[funcionarios_ativos['Setor'] == 'Comercial'])
    st.session_state.qtd_adm = len(funcionarios_ativos[funcionarios_ativos['Setor'] == 'ADM'])

def load_funcionarios():
    """Carrega os dados dos funcionários do arquivo CSV"""
    if not os.path.exists('funcionarios.csv'):
        # Criar arquivo com dados iniciais se não existir
        funcionarios = pd.DataFrame({
            'Setor': ['Comercial', 'Comercial', 'ADM', 'ADM'],
            'Nome': ['Funcionário 1', 'Funcionário 2', 'Funcionário 3', 'Funcionário 4'],
            'Cargo': ['Vendedor', 'Vendedor', 'Assistente', 'Gerente'],
            'Ativo': [True, True, True, True]
        })
        funcionarios.to_csv('funcionarios.csv', index=False)
    else:
        # Carregar do arquivo e garantir que a coluna 'Ativo' seja booleana
        funcionarios = pd.read_csv('funcionarios.csv')
        # Converter a coluna 'Ativo' para booleano, tratando strings como 'True'/'False'
        if 'Ativo' in funcionarios.columns:
            funcionarios['Ativo'] = funcionarios['Ativo'].astype(str).str.lower().map({'true': True, 'false': False, 'True': True, 'False': False})
    
    return funcionarios

def save_funcionarios(funcionarios):
    """Salva os dados dos funcionários no arquivo CSV"""
    # Criar uma cópia para não modificar o DataFrame original
    df_to_save = funcionarios.copy()
    # Garantir que a coluna 'Ativo' seja salva como string 'True'/'False'
    if 'Ativo' in df_to_save.columns:
        df_to_save['Ativo'] = df_to_save['Ativo'].astype(bool)
    # Salvar o DataFrame
    df_to_save.to_csv('funcionarios.csv', index=False)
    # Atualizar a contagem de funcionários ativos
    if 'funcionarios_df' in st.session_state:
        st.session_state.funcionarios_df = load_funcionarios()

# Funções auxiliares (mantidas as mesmas)
def load_data():
    # Inicializar variáveis
    metas = None
    resultados = None
    
    # Carregar dados dos funcionários primeiro
    if 'funcionarios_df' not in st.session_state:
        st.session_state.funcionarios_df = load_funcionarios()
    
    # Contar funcionários ativos por setor
    funcionarios_ativos = st.session_state.funcionarios_df[st.session_state.funcionarios_df['Ativo'] == True]
    qtd_comercial = len(funcionarios_ativos[funcionarios_ativos['Setor'] == 'Comercial'])
    qtd_adm = len(funcionarios_ativos[funcionarios_ativos['Setor'] == 'ADM'])
    
    # Atualizar contagem na sessão para uso consistente
    st.session_state.qtd_comercial = qtd_comercial
    st.session_state.qtd_adm = qtd_adm
    
    # Verificar se o arquivo de metas existe, caso contrário, criar um novo
    if not os.path.exists('metas.csv') or os.path.getsize('metas.csv') == 0:
        # Valores padrão iniciais
        data = {
            'Mes': [pd.Timestamp.now().replace(day=1).normalize()],
            'Meta_Comercial_Min': [4000000.0],
            'Meta_Comercial_Ideal': [4250000.0],
            'Meta_Comercial_Excelente': [4500000.0],
            'Meta_Margem_Min': [24.0],
            'Meta_Margem_Ideal': [25.0],
            'Meta_Margem_Excelente': [26.0],
            'Valor_Pago_Min_ADM': [50.0 * qtd_adm],
            'Valor_Pago_Ideal_ADM': [150.0 * qtd_adm],
            'Valor_Pago_Excelente_ADM': [250.0 * qtd_adm],
            'Valor_Pago_Min_Comercial': [50.0 * qtd_comercial],
            'Valor_Pago_Ideal_Comercial': [150.0 * qtd_comercial],
            'Valor_Pago_Excelente_Comercial': [250.0 * qtd_comercial],
            'Qtd_Funcionarios_ADM': [qtd_adm],
            'Qtd_Funcionarios_Comercial': [qtd_comercial]
        }
        metas = pd.DataFrame(data)
        metas.to_csv('metas.csv', index=False)
    else:
        # Carregar dados existentes
        metas = pd.read_csv('metas.csv', parse_dates=['Mes'])
        
        # Verificar e atualizar colunas se necessário (migração)
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
    
    # Verificar se o arquivo de resultados existe, caso contrário, criar um novo
    if not os.path.exists('resultados.csv') or os.path.getsize('resultados.csv') == 0:
        # Criar um DataFrame vazio com as colunas necessárias
        resultados = pd.DataFrame(columns=['Mes', 'Realizado_Comercial', 'Realizado_Margem'])
        # Salvar o arquivo vazio para uso futuro
        resultados.to_csv('resultados.csv', index=False)
    else:
        # Carregar resultados existentes
        resultados = pd.read_csv('resultados.csv', parse_dates=['Mes'])
    
    # Garantir que as datas estão no mesmo formato
    metas['Mes'] = pd.to_datetime(metas['Mes']).dt.normalize()
    resultados['Mes'] = pd.to_datetime(resultados['Mes']).dt.normalize()
    
    # Se já existirem valores salvos, dividir pelo número de funcionários ativos para exibição
    if not metas.empty and 'Qtd_Funcionarios_ADM' in metas.columns and 'Qtd_Funcionarios_Comercial' in metas.columns:
        qtd_adm = metas['Qtd_Funcionarios_ADM'].iloc[0] if not metas['Qtd_Funcionarios_ADM'].empty else 1
        qtd_comercial = metas['Qtd_Funcionarios_Comercial'].iloc[0] if not metas['Qtd_Funcionarios_Comercial'].empty else 1
        
        # Dividir os valores pelo número de funcionários para exibição
        metas['Valor_Pago_Min_ADM'] = metas['Valor_Pago_Min_ADM'] / qtd_adm if qtd_adm > 0 else 0
        metas['Valor_Pago_Ideal_ADM'] = metas['Valor_Pago_Ideal_ADM'] / qtd_adm if qtd_adm > 0 else 0
        metas['Valor_Pago_Excelente_ADM'] = metas['Valor_Pago_Excelente_ADM'] / qtd_adm if qtd_adm > 0 else 0
        metas['Valor_Pago_Min_Comercial'] = metas['Valor_Pago_Min_Comercial'] / qtd_comercial if qtd_comercial > 0 else 0
        metas['Valor_Pago_Ideal_Comercial'] = metas['Valor_Pago_Ideal_Comercial'] / qtd_comercial if qtd_comercial > 0 else 0
        metas['Valor_Pago_Excelente_Comercial'] = metas['Valor_Pago_Excelente_Comercial'] / qtd_comercial if qtd_comercial > 0 else 0
    
    # Formatar os DataFrames para exibir meses em português
    metas = formatar_dataframe(metas)
    resultados = formatar_dataframe(resultados)
    
    return metas, resultados

def save_data(metas, resultados):
    """Salva os dados de metas e resultados nos arquivos CSV"""
    # Atualizar a quantidade de funcionários ativos por setor
    # ...
    if 'funcionarios_df' in st.session_state:
        funcionarios_ativos = st.session_state.funcionarios_df[st.session_state.funcionarios_df['Ativo'] == True]
        qtd_comercial = len(funcionarios_ativos[funcionarios_ativos['Setor'] == 'Comercial'])
        qtd_adm = len(funcionarios_ativos[funcionarios_ativos['Setor'] == 'ADM'])
        
        # Atualizar as quantidades de funcionários nas metas
        metas['Qtd_Funcionarios_ADM'] = qtd_adm
        metas['Qtd_Funcionarios_Comercial'] = qtd_comercial
        
        # Atualizar contagem na sessão para uso consistente
        st.session_state.qtd_comercial = qtd_comercial
        st.session_state.qtd_adm = qtd_adm
        
        # Multiplicar os valores de pagamento pelo número de funcionários ativos
        if 'Valor_Pago_Min_ADM' in metas.columns:
            metas['Valor_Pago_Min_ADM'] = metas['Valor_Pago_Min_ADM'] * qtd_adm
            metas['Valor_Pago_Ideal_ADM'] = metas['Valor_Pago_Ideal_ADM'] * qtd_adm
            metas['Valor_Pago_Excelente_ADM'] = metas['Valor_Pago_Excelente_ADM'] * qtd_adm
            metas['Valor_Pago_Min_Comercial'] = metas['Valor_Pago_Min_Comercial'] * qtd_comercial
            metas['Valor_Pago_Ideal_Comercial'] = metas['Valor_Pago_Ideal_Comercial'] * qtd_comercial
            metas['Valor_Pago_Excelente_Comercial'] = metas['Valor_Pago_Excelente_Comercial'] * qtd_comercial
    
    # Salvar os dados
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
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Vendas", "📈 Margem", "💲 Pagamentos", "👥 Funcionários"])
    
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
    
    # Adicionar o painel de funcionários na aba correspondente
    with tab4:
        if 'render_aba_funcionarios' in globals():
            # Ajustar o layout para a sidebar
            st.markdown("**Gerenciar Funcionários**")
            render_aba_funcionarios()
        else:
            st.error("Erro: Função render_aba_funcionarios não encontrada.")
    
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
    
    # Fechando a sidebar
    
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
            
            # Mapeamento de níveis para nomes de coluna
            nivel_para_coluna = {
                'minimo': 'Min',
                'ideal': 'Ideal',
                'excelente': 'Excelente'
            }
            
            # Determinar níveis de desempenho
            if ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Excelente']:
                status_vendas = "Excelente"
                status_vendas_class = "badge-success"
                nivel_vendas = 'excelente'
            elif ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Ideal']:
                status_vendas = "Ideal"
                status_vendas_class = "badge-success"
                nivel_vendas = 'ideal'
            elif ultimo['Realizado_Comercial'] >= ultimo['Meta_Comercial_Min']:
                status_vendas = "Mínimo"
                status_vendas_class = "badge-warning"
                nivel_vendas = 'minimo'
            else:
                status_vendas = "Não atingido"
                status_vendas_class = "badge-danger"
                nivel_vendas = None
            
            if ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Excelente']:
                status_margem = "Excelente"
                status_margem_class = "badge-success"
                nivel_margem = 'excelente'
            elif ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Ideal']:
                status_margem = "Ideal"
                status_margem_class = "badge-success"
                nivel_margem = 'ideal'
            elif ultimo['Realizado_Margem'] >= ultimo['Meta_Margem_Min']:
                status_margem = "Mínimo"
                status_margem_class = "badge-warning"
                nivel_margem = 'minimo'
            else:
                status_margem = "Não atingido"
                status_margem_class = "badge-danger"
                nivel_margem = None
            
            # Inicializar totais
            pag_vendas_adm = 0
            pag_vendas_comercial = 0
            pag_margem_adm = 0
            pag_margem_comercial = 0
            
            # Dicionário para armazenar pagamentos por funcionário
            pagamentos_por_funcionario = {}
            
            # Calcular pagamentos por funcionário
            for _, funcionario in st.session_state.funcionarios_df[st.session_state.funcionarios_df['Ativo'] == True].iterrows():
                setor = funcionario['Setor']
                
                # Determinar valor base do funcionário baseado no cargo (aqui você pode adicionar lógica personalizada)
                # Por enquanto, vamos usar um valor fixo para demonstração
                valor_base = 1000  # Valor base que será ajustado pelo nível de desempenho
                
                # Obter sufixo da coluna baseado no nível
                sufixo_vendas = nivel_para_coluna.get(nivel_vendas, 'Min')
                sufixo_margem = nivel_para_coluna.get(nivel_margem, 'Min')
                
                # Calcular pagamento por vendas
                if nivel_vendas:
                    coluna = f'Valor_Pago_{sufixo_vendas}_{setor}'
                    pag_vendas = ultimo.get(coluna, 0)
                else:
                    pag_vendas = 0
                
                # Calcular pagamento por margem
                if nivel_margem:
                    coluna = f'Valor_Pago_{sufixo_margem}_{setor}'
                    pag_margem = ultimo.get(coluna, 0)
                else:
                    pag_margem = 0
                
                # Armazenar pagamento do funcionário
                pagamentos_por_funcionario[funcionario['Nome']] = {
                    'Setor': setor,
                    'Cargo': funcionario['Cargo'],
                    'Pagamento_Vendas': pag_vendas,
                    'Pagamento_Margem': pag_margem,
                    'Total': pag_vendas + pag_margem
                }
                
                # Acumular totais por setor
                if setor == 'ADM':
                    pag_vendas_adm += pag_vendas
                    pag_margem_adm += pag_margem
                else:  # Comercial
                    pag_vendas_comercial += pag_vendas
                    pag_margem_comercial += pag_margem
            
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
            
            # Preparar dados dos funcionários ativos por setor com seus respectivos pagamentos
            funcionarios_por_setor = {}
            for setor in ['ADM', 'Comercial']:
                # Filtrar funcionários ativos do setor
                funcionarios_setor = [
                    func for func_name, func in pagamentos_por_funcionario.items() 
                    if func['Setor'] == setor
                ]
                
                # Inicializar lista de funcionários para o setor
                funcionarios_por_setor[setor] = []
                if funcionarios_setor:
                    for func_nome, func in pagamentos_por_funcionario.items():
                        if func['Setor'] == setor:  # Garantir que estamos pegando apenas funcionários do setor atual
                            funcionarios_por_setor[setor].append({
                                'nome': func_nome,
                                'cargo': func['Cargo'],
                                'vendas': func['Pagamento_Vendas'],
                                'margem': func['Pagamento_Margem'],
                                'total': func['Total']
                            })
            
            # Card ADM
            with st.container():
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
                
                # Renderizar a lista de funcionários do ADM
                with st.container():
                    st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
                    render_employee_list(funcionarios_por_setor.get('ADM', []), 'ADM')
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Card Comercial
            with st.container():
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
                
                # Renderizar a lista de funcionários do Comercial
                with st.container():
                    st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
                    render_employee_list(funcionarios_por_setor.get('Comercial', []), 'Comercial')
                    st.markdown("</div>", unsafe_allow_html=True)
            
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
Versão 1.3 - 18/07/2025
</div>
""", unsafe_allow_html=True)