import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def gerar_dados_maker(num_registros=500):
    """
    Gera um DataFrame com dados simulados para um laboratório Maker.

    Args:
        num_registros (int): O número de linhas (registros) a serem geradas.

    Returns:
        pandas.DataFrame: O DataFrame com os dados simulados.
    """
    # Listas de dados para simular
    estudantes = [f'Estudante_{i}' for i in range(1, 21)]
    materiais = [
        'Filamento PLA', 'Filamento ABS', 'Resina SLA', 'Placa de MDF',
        'Placa de Acrílico', 'Motor de Passo', 'Servo Motor',
        'Protoboard', 'Raspberry Pi', 'Arduino UNO', 'LED',
        'Resistor', 'Sensor Ultrassônico'
    ]
    custo_unitario_medio = {
        'Filamento PLA': 100, 'Filamento ABS': 120, 'Resina SLA': 250,
        'Placa de MDF': 30, 'Placa de Acrílico': 50, 'Motor de Passo': 60,
        'Servo Motor': 45, 'Protoboard': 15, 'Raspberry Pi': 200,
        'Arduino UNO': 80, 'LED': 1, 'Resistor': 0.5, 'Sensor Ultrassônico': 20
    }
    estoque_inicial = {
        'Filamento PLA': 50, 'Filamento ABS': 40, 'Resina SLA': 30,
        'Placa de MDF': 100, 'Placa de Acrílico': 80, 'Motor de Passo': 75,
        'Servo Motor': 90, 'Protoboard': 200, 'Raspberry Pi': 25,
        'Arduino UNO': 50, 'LED': 500, 'Resistor': 1000, 'Sensor Ultrassônico': 120
    }

    # Gerando os dados aleatórios
    dados = {
        'Nome do Estudante': np.random.choice(estudantes, num_registros),
        'Material Usado': np.random.choice(materiais, num_registros),
        'Quantidade Usada': np.random.randint(1, 10, num_registros)
    }

    df = pd.DataFrame(dados)

    # Adicionando o Custo Unitário e calculando Custo Total e Estoque Restante
    df['Custo Unitario'] = df['Material Usado'].map(custo_unitario_medio)
    df['Custo Total'] = df['Quantidade Usada'] * df['Custo Unitario']
    df['Estoque Restante'] = df.apply(
        lambda row: estoque_inicial.get(row['Material Usado'], 0) - row['Quantidade Usada'],
        axis=1
    )

    # Gerando datas aleatórias nos últimos 6 meses
    hoje = datetime.now()
    seis_meses_atras = hoje - timedelta(days=180)
    datas_aleatorias = [
        seis_meses_atras + timedelta(days=np.random.randint(0, 180))
        for _ in range(num_registros)
    ]
    df['Data de Uso'] = datas_aleatorias

    # Ordenando por data
    df = df.sort_values(by='Data de Uso').reset_index(drop=True)

    # Selecionando as colunas finais
    df = df[['Nome do Estudante', 'Material Usado', 'Quantidade Usada', 'Custo Unitario', 'Custo Total', 'Data de Uso', 'Estoque Restante']]
    
    return df

# Gerar o DataFrame
df_dados_maker = gerar_dados_maker()

# Salvar o DataFrame em um arquivo CSV
nome_arquivo = 'controle_lab_maker.csv'
df_dados_maker.to_csv(nome_arquivo, index=False)

print(f'Arquivo "{nome_arquivo}" gerado com sucesso!')
print('As primeiras 5 linhas do arquivo são:')
print(df_dados_maker.head())