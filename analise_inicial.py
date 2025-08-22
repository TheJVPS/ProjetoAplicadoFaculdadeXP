import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuração de estilo
sns.set_palette("husl")
pd.set_option('display.float_format', '{:.2f}'.format)

# Carregar os dados
df = pd.read_csv('controle_lab_maker.csv', parse_dates=['Data de Uso'])

print("\n=== Estatísticas Descritivas ===")
print(df.describe())

print("\n=== Top 5 Materiais Mais Utilizados ===")
print(df['Material Usado'].value_counts().head(5))

print("\n=== Top 5 Alunos que Mais Consomem ===")
print(df['Nome do Estudante'].value_counts().head(5))

print("\n=== Custo Total por Material ===")
print(df.groupby('Material Usado')['Custo Total'].sum().sort_values(ascending=False).head(10))

