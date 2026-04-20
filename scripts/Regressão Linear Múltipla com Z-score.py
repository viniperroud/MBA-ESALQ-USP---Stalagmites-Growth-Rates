# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 18:27:52 2026

@author: vinip
"""

#%% importar bibliotecas
import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

#%% Carregar os dados 
df = pd.read_csv(r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\df_final_modelagem.csv")

df = df.dropna(subset=["growth_rate", "O18", "C13", "temp_interp"])

#%% regressão linear múltipla com Z-SCORE por caverna
results = []

for cave, df_cave in df.groupby("caves"):
    
    print("\n" + "="*50)
    print(f"Caverna: {cave} (Z-score)")
    print("="*50)
    
    # variável dependente
    y = df_cave["growth_rate"]
    
    # variáveis independentes
    X = df_cave[["temp_interp", "O18", "C13"]]
    
    # z-score
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X = pd.DataFrame(
        X_scaled,
        columns=["temp_interp", "O18", "C13"],
        index=df_cave.index
    )
    
    # adicionar intercepto
    X = sm.add_constant(X)
    
    # ajustar modelo
    model = sm.OLS(y, X).fit()
    
    # mostrar resultados
    print(model.summary())
    
    # salvar resultados
    results.append({
        "cave": cave,
        "coef_temp": model.params["temp_interp"],
        "coef_O18": model.params["O18"],
        "coef_C13": model.params["C13"],
        "p_temp": model.pvalues["temp_interp"],
        "p_O18": model.pvalues["O18"],
        "p_C13": model.pvalues["C13"],
        "R2": model.rsquared
    })

# tabela final
df_results = pd.DataFrame(results)

# arredondar
df_results = df_results.round(3)

print("\nTabela final (Z-score):")
print(df_results)

df_results.to_csv(
    r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\tabela_regressao_zscore.csv",
    index=False
)
