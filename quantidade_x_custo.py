import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuração de estilo
sns.set_palette("husl")
pd.set_option('display.float_format', '{:.2f}'.format)

# Carregar os dados
df = pd.read_csv('controle_lab_maker.csv', parse_dates=['Data de Uso'])

#Gráfico de relação entre quantidade e custo 
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Quantidade Usada', y='Custo Total', hue='Material Usado', data=df, s=100)
plt.title('Relação entre Quantidade Usada e Custo por Material')
plt.xlabel('Quantidade Usada')
plt.ylabel('Custo Total (R$)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()