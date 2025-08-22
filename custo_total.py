import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuração de estilo
sns.set_palette("husl")
pd.set_option('display.float_format', '{:.2f}'.format)

# Carregar os dados
df = pd.read_csv('controle_lab_maker.csv', parse_dates=['Data de Uso'])

#Gráfico de custo total por material 
plt.figure(figsize=(12, 6))
custo_por_material = df.groupby('Material Usado')['Custo Total'].sum().sort_values(ascending=False)
sns.barplot(x=custo_por_material.values, y=custo_por_material.index)
plt.title('Custo Total por Material')
plt.xlabel('Custo Total (R$)')
plt.ylabel('Material')
plt.tight_layout()
plt.savefig('custo_total.png')
plt.show()