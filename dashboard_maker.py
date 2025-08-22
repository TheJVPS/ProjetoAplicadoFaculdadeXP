import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import datetime

# --- 1. CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Gestão de Materiais Maker",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard de Gestão do Laboratório Maker")
st.markdown("---")

# --- 2. CARREGAMENTO E PRÉ-PROCESSAMENTO DOS DADOS (COM CACHE) ---
@st.cache_resource
def carregar_dados_e_treinar_modelo():
    try:
        df = pd.read_csv("uso_materiais_preparado.csv")
        df['data_de_uso'] = pd.to_datetime(df['data_de_uso'])
        df['mes'] = df['data_de_uso'].dt.month

        # Treinar o modelo de Machine Learning
        materiais = sorted(df['material_usado'].unique())
        encoder = OneHotEncoder(handle_unknown='ignore')
        materiais_encoded = encoder.fit_transform(df[['material_usado']]).toarray()
        materiais_df = pd.DataFrame(materiais_encoded, columns=encoder.get_feature_names_out(['material_usado']))

        features = ['mes'] + list(materiais_df.columns)
        X = df[['mes']].join(materiais_df)
        y = df['quantidade_usada']
        
        modelo = LinearRegression()
        modelo.fit(X, y)

        return df, modelo, encoder, features, materiais

    except FileNotFoundError:
        st.error("Arquivo 'uso_materiais_preparado.csv' não encontrado. Por favor, execute o script de geração e preparação de dados primeiro.")
        st.stop()

df, modelo, encoder, features, materiais = carregar_dados_e_treinar_modelo()

# --- 3. SEÇÃO DE VISUALIZAÇÃO DOS DADOS HISTÓRICOS ---
st.header("Análise dos Dados Históricos")

# Gráfico de uso por mês
st.subheader("Uso de Materiais ao Longo do Tempo")
df_mensal = df.groupby(df['data_de_uso'].dt.to_period('M')).agg(
    total_gasto=('custo_total', 'sum'),
    quantidade_usada=('quantidade_usada', 'sum')
).reset_index()
df_mensal['data_de_uso'] = df_mensal['data_de_uso'].astype(str)

fig_uso_mensal = px.line(
    df_mensal,
    x='data_de_uso',
    y='quantidade_usada',
    labels={'data_de_uso': 'Mês', 'quantidade_usada': 'Quantidade Total Usada'},
    title='Quantidade Total de Materiais Usados por Mês'
)
st.plotly_chart(fig_uso_mensal, use_container_width=True)

# Gráfico de uso por material
st.subheader("Uso Total por Tipo de Material")
df_material_total = df.groupby('material_usado').agg(
    total_gasto=('custo_total', 'sum'),
    quantidade_usada=('quantidade_usada', 'sum')
).reset_index().sort_values(by='quantidade_usada', ascending=False)

fig_material_total = px.bar(
    df_material_total,
    x='material_usado',
    y='quantidade_usada',
    labels={'material_usado': 'Material', 'quantidade_usada': 'Quantidade Total Usada'},
    title='Quantidade Total Usada por Material'
)
st.plotly_chart(fig_material_total, use_container_width=True)


# --- 4. SEÇÃO DE PREVISÃO INTERATIVA (NA BARRA LATERAL) ---
st.sidebar.header("⚙️ Ferramenta de Previsão Pontual")
st.sidebar.subheader("Analise um cenário específico")

material_selecionado = st.sidebar.selectbox("Selecione o Material", materiais)
mes_selecionado = st.sidebar.number_input(
    "Mês para a Previsão (1-12)",
    min_value=1,
    max_value=12,
    value=10,
    step=1
)
estoque_atual = st.sidebar.number_input(
    f"Estoque Atual de {material_selecionado}",
    min_value=0,
    value=100
)
custo_unitario_atual = st.sidebar.number_input(
    f"Custo Unitário de {material_selecionado} (R$)",
    min_value=0.0,
    value=df[df['material_usado'] == material_selecionado]['custo_unitario'].mean(),
    format="%.2f"
)
estoque_seguranca = st.sidebar.number_input(
    "Estoque Mínimo de Segurança",
    min_value=0,
    value=20
)

# Botão para gerar o relatório
if st.sidebar.button("Gerar Relatório de Previsão"):
    st.markdown("---")
    st.header("📝 Relatório de Previsão Pontual")

    # Preparar os dados para o modelo
    cenario = pd.DataFrame(np.zeros((1, len(features))), columns=features)
    cenario['mes'] = mes_selecionado
    coluna_material = f'material_usado_{material_selecionado}'
    if coluna_material in cenario.columns:
        cenario[coluna_material] = 1
    
    # Fazer a previsão de demanda
    demanda_prevista = modelo.predict(cenario)[0]
    custo_estimado = demanda_prevista * custo_unitario_atual
    estoque_projetado = estoque_atual - demanda_prevista
    
    # Exibir métricas e resultados
    col1, col2, col3 = st.columns(3)
    col1.metric("Demanda Prevista", f"{demanda_prevista:.2f} un.")
    col2.metric("Custo Estimado", f"R$ {custo_estimado:.2f}")
    col3.metric("Estoque Projetado", f"{estoque_projetado:.2f} un.")
    
    st.subheader("Recomendação de Compra")
    if estoque_projetado < estoque_seguranca:
        quantidade_a_comprar = (estoque_seguranca - estoque_projetado) + demanda_prevista
        st.success(
            f"**Recomendado comprar!** O estoque projetado ({estoque_projetado:.2f} un.) "
            f"está abaixo do nível de segurança ({estoque_seguranca} un.)."
        )
        st.info(
            f"**Quantidade sugerida:** {quantidade_a_comprar:.2f} unidades para atender a demanda e manter o estoque de segurança."
        )
    else:
        st.success(
            f"**Não é necessário comprar.** O estoque projetado ({estoque_projetado:.2f} un.) "
            f"é suficiente para cobrir a demanda."
        )

# --- 5. NOVA SEÇÃO PARA PROJEÇÃO FUTURA ---
st.markdown("---")
st.header("📈 Projeção de Estoque e Ponto de Compra")
st.markdown("Veja em que mês seu estoque projetado será insuficiente, com base na demanda futura.")

# Adicionamos novos inputs específicos para essa análise
material_projecao = st.selectbox("Selecione o Material para Projeção", materiais, key='projecao_material')
estoque_inicial_projecao = st.number_input(
    f"Estoque Inicial de {material_projecao}",
    min_value=0,
    value=150,
    key='projecao_estoque'
)
estoque_seguranca_projecao = st.number_input(
    "Estoque de Segurança para Projeção",
    min_value=0,
    value=20,
    key='projecao_seguranca'
)

if st.button("Projetar Estoque e Encontrar Ponto de Compra"):
    
    # Lógica de projeção
    estoque_restante = estoque_inicial_projecao
    mes_atual = datetime.datetime.now().month
    mes_compra_encontrado = None
    meses_projecao = []
    
    for i in range(12): # Projeta para os próximos 12 meses
        mes_proximo = (mes_atual + i - 1) % 12 + 1
        
        # Preparar o cenário para a previsão de demanda
        cenario_futuro = pd.DataFrame(np.zeros((1, len(features))), columns=features)
        cenario_futuro['mes'] = mes_proximo
        coluna_material = f'material_usado_{material_projecao}'
        if coluna_material in cenario_futuro.columns:
            cenario_futuro[coluna_material] = 1

        demanda_prevista = modelo.predict(cenario_futuro)[0]
        
        estoque_restante -= demanda_prevista
        meses_projecao.append({
            "Mês": mes_proximo,
            "Demanda Prevista": f"{demanda_prevista:.2f}",
            "Estoque Projetado": f"{estoque_restante:.2f}",
        })
        
        if estoque_restante <= estoque_seguranca_projecao and mes_compra_encontrado is None:
            mes_compra_encontrado = mes_proximo
    
    # Exibir a tabela de projeção
    st.subheader(f"Projeção Mês a Mês para {material_projecao}")
    df_projecao = pd.DataFrame(meses_projecao)
    st.dataframe(df_projecao, use_container_width=True)
    
    # Exibir a conclusão
    st.subheader("Conclusão")
    if mes_compra_encontrado:
        meses_do_ano = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        mes_nome = meses_do_ano[mes_compra_encontrado - 1]
        st.error(f"Seu estoque de **{material_projecao}** será insuficiente (abaixo do nível de segurança) no mês de **{mes_nome}**.")
        st.warning("Recomendação: Considere realizar a compra no mês anterior a este.")
    else:
        st.success(
            "Seu estoque atual é suficiente para o próximo ano. Não é necessário programar uma compra."
        )