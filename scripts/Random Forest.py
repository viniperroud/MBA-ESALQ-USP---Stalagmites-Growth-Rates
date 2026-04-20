# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:25:49 2026

@author: vinip
"""

#%% IMPORTAR BIBLIOTECAS
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

#%% CARREGAR DADOS
df = pd.read_csv(r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\df_final_modelagem.csv")

# remover NaNs
df = df.dropna(subset=["growth_rate", "O18", "C13", "temp_interp"])

#%% RANDOM FOREST POR CAVERNA
rf_results = []

for cave, df_cave in df.groupby("caves"):
    
    print("\n" + "="*50)
    print(f"Caverna: {cave} (Random Forest)")
    print("="*50)
    
    # variável dependente
    y = df_cave["growth_rate"]
    
    # variáveis independentes
    X = df_cave[["temp_interp", "O18", "C13"]]
    
    # modelo
    rf = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    
    rf.fit(X, y)
    
    # importância das variáveis
    importances = rf.feature_importances_
    
    print("Importância das variáveis:")
    print(f"Temp: {importances[0]:.3f}")
    print(f"O18:  {importances[1]:.3f}")
    print(f"C13:  {importances[2]:.3f}")
    
    # salvar resultados
    rf_results.append({
        "cave": cave,
        "imp_temp": importances[0],
        "imp_O18": importances[1],
        "imp_C13": importances[2]
    })

#%% TABELA FINAL
df_rf = pd.DataFrame(rf_results)

# arredondar
df_rf = df_rf.round(3)

print("\nTabela final Random Forest:")
print(df_rf)

# salvar
df_rf.to_csv(
    r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\tabela_random_forest.csv",
    index=False
)
