# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:55:59 2026

@author: vinip
"""
#Modelagem Estatística - Regressão Linear

#%% importar bibliotecas
import pandas as pd
import statsmodels.api as sm

#%% Carregar os dados 

df = pd.read_csv(r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\df_final_modelagem.csv")

df = df.dropna(subset=["growth_rate", "O18", "C13", "temp_interp"])

#regressão linear múltipla por caverna
results = []

for cave, df_cave in df.groupby("caves"):
    
    print("\n" + "="*50)
    print(f"Caverna: {cave}")
    print("="*50)
    
    # variável dependente
    y = df_cave["growth_rate"]
    
    # variáveis independentes
    X = df_cave[["temp_interp", "O18", "C13"]]
    
    # adicionar intercepto
    X = sm.add_constant(X)
    
    # ajustar modelo
    model = sm.OLS(y, X).fit()
    
    # mostrar resultados
    print(model.summary())
    
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
    
df_results = pd.DataFrame(results)

# arredondar
df_results = df_results.round(3)

print("\nTabela final:")
print(df_results)

df_results.to_csv(r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\tabela_regressao.csv", index=False)

