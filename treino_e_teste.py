import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import datetime

# --- 1. CARREGAR E PREPARAR OS DADOS ---
# Carregamos os dados preparados do script anterior
df = pd.read_csv("uso_materiais_preparado.csv")

# Converter a coluna de data para o tipo datetime
df['data_de_uso'] = pd.to_datetime(df['data_de_uso'])

# Extrair o mês da data para usar como variável preditora
df['mes'] = df['data_de_uso'].dt.month

# --- 2. TREINAR O MODELO DE MACHINE LEARNING ---
# Codificar a variável categórica 'material_usado'
encoder = OneHotEncoder(handle_unknown='ignore')
materiais_encoded = encoder.fit_transform(df[['material_usado']]).toarray()
materiais_df = pd.DataFrame(materiais_encoded, columns=encoder.get_feature_names_out(['material_usado']))

# Definir variáveis preditoras (X) e alvo (y)
features = ['mes'] + list(materiais_df.columns)
X = df[['mes']].join(materiais_df)
y = df['quantidade_usada']

# Treinar o modelo de Regressão Linear
modelo = LinearRegression()
modelo.fit(X, y)

# --- 3. FUNÇÃO PARA FAZER PREVISÕES E GERAR O RELATÓRIO ---
def gerar_relatorio_de_compra(mes, material, estoque_atual, custo_unitario_atual, estoque_seguranca):
    """
    Gera um relatório completo de previsão e recomendação de compra.

    Args:
        mes (int): O mês para o qual a previsão será feita (ex: 9 para Setembro).
        material (str): O nome exato do material (ex: 'Filamento PLA').
        estoque_atual (int): O número de unidades em estoque atualmente.
        custo_unitario_atual (float): O custo por unidade do material.
        estoque_seguranca (int): O estoque mínimo que você deseja manter.

    Returns:
        None: Imprime o relatório diretamente no console.
    """
    # 3.1. Pré-processar a entrada para o modelo
    cenario = pd.DataFrame(np.zeros((1, len(features))), columns=features)
    cenario['mes'] = mes
    
    coluna_material = f'material_usado_{material}'
    if coluna_material in cenario.columns:
        cenario[coluna_material] = 1
    else:
        print(f"Erro: O material '{material}' não foi encontrado nos dados de treino. Por favor, verifique a grafia.")
        return

    # 3.2. Fazer a previsão de demanda usando o modelo de ML
    demanda_prevista = modelo.predict(cenario)[0]
    
    # 3.3. Aplicar a lógica de negócio
    custo_estimado = demanda_prevista * custo_unitario_atual
    estoque_projetado = estoque_atual - demanda_prevista
    
    # 3.4. Gerar a recomendação de compra
    recomendacao = "Não é necessário comprar no momento."
    quantidade_a_comprar = 0
    
    if estoque_projetado < estoque_seguranca:
        recomendacao = "Recomendado comprar para manter o estoque de segurança."
        # Sugere a compra de unidades suficientes para atingir o estoque de segurança + a demanda prevista
        quantidade_a_comprar = (estoque_seguranca - estoque_projetado) + demanda_prevista
        
    # --- 4. EXIBIR O RELATÓRIO ---
    print("\n" + "="*50)
    print(f"RELATÓRIO DE GESTÃO PARA {material.upper()} - MÊS {mes}")
    print("="*50)
    print(f"Estoque Atual: {estoque_atual} unidades")
    print(f"Custo Unitário Atual: R${custo_unitario_atual:.2f}")
    print(f"Estoque de Segurança: {estoque_seguranca} unidades")
    print("-" * 50)
    print(f"** Demanda Prevista: {demanda_prevista:.2f} unidades **")
    print(f"** Custo Estimado: R${custo_estimado:.2f} **")
    print(f"** Estoque Projetado: {estoque_projetado:.2f} unidades **")
    print("-" * 50)
    print(f"Recomendação de Compra: {recomendacao}")
    if quantidade_a_comprar > 0:
        print(f"Quantidade Sugerida: {quantidade_a_comprar:.2f} unidades")
    print("="*50 + "\n")


# --- 5. EXECUÇÃO DO RELATÓRIO PARA UM CENÁRIO EXEMPLO ---
# Você pode alterar esses valores para testar diferentes cenários
mes_de_previsao = 12  # Mês de setembro
material_de_previsao = 'Filamento PLA'
estoque_atual_do_material = 5
custo_atual_do_material = 105.00
estoque_minimo_seguranca = 5

gerar_relatorio_de_compra(
    mes_de_previsao,
    material_de_previsao,
    estoque_atual_do_material,
    custo_atual_do_material,
    estoque_minimo_seguranca
)