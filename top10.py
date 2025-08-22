import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuração de estilo
sns.set_palette("husl")
pd.set_option('display.float_format', '{:.2f}'.format)

# Carregar os dados
df = pd.read_csv('controle_lab_maker.csv', parse_dates=['Data de Uso'])

#Gráfico com o top 10 de alunos que mais usaram materiais
plt.figure(figsize=(12, 6))
top_alunos = df.groupby('Nome do Estudante')['Custo Total'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top_alunos.values, y=top_alunos.index)
plt.title('Top 10 Alunos por Custo Total')
plt.xlabel('Custo Total (R$)')
plt.ylabel('Aluno')
plt.tight_layout()
plt.show()