import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuração de estilo
sns.set_palette("husl")
pd.set_option('display.float_format', '{:.2f}'.format)

# Carregar os dados
df = pd.read_csv('controle_lab_maker.csv', parse_dates=['Data de Uso'])

#Gráfico de distribuição de uso dos materiais
plt.figure(figsize=(12, 6))
sns.countplot(y='Material Usado', data=df, order=df['Material Usado'].value_counts().index)
plt.title('Distribuição de Uso de Materiais')
plt.xlabel('Contagem')
plt.ylabel('Material')
plt.tight_layout()
plt.show()