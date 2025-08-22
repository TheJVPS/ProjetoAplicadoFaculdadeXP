import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuração de estilo
sns.set_palette("husl")
pd.set_option('display.float_format', '{:.2f}'.format)

# Carregar os dados
df = pd.read_csv('controle_lab_maker.csv', parse_dates=['Data de Uso'])

#Gráfico de uso de materiais por mês
plt.figure(figsize=(14, 6))
df['Mês'] = df['Data de Uso'].dt.month
uso_mensal = df.groupby('Mês')['Quantidade Usada'].sum()
sns.lineplot(x=uso_mensal.index, y=uso_mensal.values, marker='o')
plt.title('Uso de Materiais ao Longo dos Meses')
plt.xlabel('Mês')
plt.ylabel('Quantidade Total Utilizada')
plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dec'])
plt.grid(True)
plt.savefig('uso_mes.png')
plt.show()