import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuração de estilo
sns.set_palette("husl")
pd.set_option('display.float_format', '{:.2f}'.format)

# Carregar os dados
df = pd.read_csv('controle_lab_maker.csv', parse_dates=['Data de Uso'])

#Gráfico de custo por estação
# Correlação entre quantidade e custo
correlacao = df[['Quantidade Usada', 'Custo Total']].corr()
print("\n=== Correlação entre Quantidade e Custo ===")
print(correlacao)

# Materiais por estação (testando H5)
df['Estação'] = df['Data de Uso'].dt.month.apply(lambda x: 'Verão' if x in [1,2,12] else
                                                'Outono' if x in [3,4,5] else
                                                'Inverno' if x in [6,7,8] else 'Primavera')

plt.figure(figsize=(12, 6))
sns.boxplot(x='Estação', y='Custo Total', data=df)
plt.title('Distribuição de Custos por Estação')
plt.ylabel('Custo (R$)')
plt.xlabel('Estação do Ano')
plt.tight_layout()
plt.show()