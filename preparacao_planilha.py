import pandas as pd

# 1. Ler o arquivo original, que agora tem custo unitário
df = pd.read_csv("controle_lab_maker.csv")

# 2. Visualizar as primeiras linhas
print("Prévia dos dados:")
print(df.head(), "\n")

# 3. Padronizar nomes de colunas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# 4. Tratar valores ausentes (se houver)
df.fillna({
    "quantidade_usada": 0,
    "custo_unitario": 0,
    "custo_total": 0,
    "estoque_restante": 0
}, inplace=True)

# 5. Garantir tipos corretos
df["quantidade_usada"] = pd.to_numeric(df["quantidade_usada"], errors="coerce").fillna(0)
df["custo_unitario"] = pd.to_numeric(df["custo_unitario"], errors="coerce").fillna(0)
df["custo_total"] = pd.to_numeric(df["custo_total"], errors="coerce").fillna(0)
df["estoque_restante"] = pd.to_numeric(df["estoque_restante"], errors="coerce").fillna(0)

# 6. Criar variáveis derivadas (opcional)
# Podemos re-calcular o custo total para garantir consistência
df["custo_total_calculado"] = df["quantidade_usada"] * df["custo_unitario"]

# 7. Padronizar a coluna de data
if "data_de_uso" in df.columns:
    df["data_de_uso"] = pd.to_datetime(df["data_de_uso"], errors="coerce")

# 8. Exportar dados preparados
df.to_csv("uso_materiais_preparado.csv", index=False)

print("Arquivo 'uso_materiais_preparado.csv' gerado com sucesso!")
print("\nDados finais preparados:")
print(pd.read_csv("uso_materiais_preparado.csv").head())