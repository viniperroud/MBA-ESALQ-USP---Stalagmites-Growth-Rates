# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 13:58:44 2026

@author: vinip
"""
from IPython import get_ipython
get_ipython().run_line_magic("clear", "")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#%%
#importar dfs
df_isotopes = pd.read_csv("G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\isotopes_compilate.csv", sep = ";")
df_temp = pd.read_csv(r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\Médias decadais Trace 21 cavernas.csv", sep = ";")

# garantir ordenação correta
df_isotopes = df_isotopes.sort_values(by=["caves", "stalagmite", "age"])

# criar a nova coluna com a taxa de crescimento
df_isotopes["growth_rate"] = (
    df_isotopes.groupby(["caves", "stalagmite"])["depth"].diff()
    / df_isotopes.groupby(["caves", "stalagmite"])["age"].diff()
)
df_isotopes = df_isotopes[df_isotopes["growth_rate"] > 0].copy()

#%% Cálculo IQR


iqr_summary = []

for cave, df_cave in df_isotopes.groupby("caves"): #eventualmente, mudar isso pra considerar tambem as estalagmites, ai ira agrupar e calcular IQR por caverna e por amostra.

    gr = df_cave["growth_rate"]

    Q1 = gr.quantile(0.25)
    Q3 = gr.quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    iqr_summary.append({
        "cave": cave,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "lower_limit": lower,
        "upper_limit": upper,
        "n_points": len(gr)
    })

df_iqr = pd.DataFrame(iqr_summary)


# 2) criar lista para armazenar os dados limpos
dfs_clean = []

# 3) loop por caverna
for _, row in df_iqr.iterrows():
    cave_name = row["cave"]
    lower = row["lower_limit"]
    upper = row["upper_limit"]

    # filtrar apenas essa caverna
    df_cave = df_isotopes[df_isotopes["caves"] == cave_name].copy()

    # aplicar limites do IQR
    df_cave_clean = df_cave[
        (df_cave["growth_rate"] >= lower) &
        (df_cave["growth_rate"] <= upper)
    ]

    dfs_clean.append(df_cave_clean)

# 4) juntar todas as cavernas novamente
df_isotopes = pd.concat(dfs_clean, ignore_index=True)
#%% Describe

cols_numeric = ["age", "growth_rate", "O18", "C13"]
df_isotopes[cols_numeric] = df_isotopes[cols_numeric].apply(pd.to_numeric, errors="coerce")

# Loop por caverna
for cave, group in df_isotopes.groupby("caves"):
    
    print("\n" + "=" * 60)
    print(f"Cave: {cave}")
    print("=" * 60)
    
    # Describe apenas das variáveis de interesse
    desc = group[["growth_rate", "O18", "C13"]].describe()
    print(desc)

#%%
#seleção amostra

mask = (
    (df_isotopes["caves"] == "Botuvera Cave") &
    (df_isotopes["stalagmite"] == "BT2")
)

#%%
#%% Histograma

cave_sel = "Cueva de Diamante"

mask = df_isotopes["caves"] == cave_sel

df_isotopes.loc[mask, "growth_rate"].dropna().hist(bins=25)

plt.xlabel("Growth rate (mm/ka)")
plt.ylabel("Frequency")
plt.title(f"Growth rate distribution – {cave_sel}")
plt.show()



#%%
#gráficos O18xC13 
d = df_isotopes[mask]

fig, ax1 = plt.subplots(figsize=(10, 5))

# δ18O – eixo Y esquerdo
ax1.plot(
    d["age"],
    d["O18"],
    linestyle="-",
    color = "blue",
    label="δ¹⁸O"
)

ax1.set_xlabel("Age (ka)")
ax1.set_ylabel("δ¹⁸O (‰ VPDB)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# 🔁 inverter eixo Y do δ18O
ax1.invert_yaxis()

# δ13C – eixo Y direito
ax2 = ax1.twinx()

ax2.plot(
   d["age"],
    d["C13"],
    linestyle="-",
    color="green",
    label="δ¹³C"
)

ax2.set_ylabel("δ¹³C (‰ VPDB)", color="green")
ax2.tick_params(axis="y", labelcolor="green")


# 🔁 inverter eixo Y do δ13C
ax2.invert_yaxis()

# título
plt.title("Cueva del Diamante – Stalagmite DIA")

plt.tight_layout()
plt.show()

#%% GR vs Isotope

isotope = "C13"   # opções: "O18" ou "C13"

df_plot = df_isotopes[mask].sort_values("age")

labels = {
    "O18": "δ¹⁸O (‰ VPDB)",
    "C13": "δ¹³C (‰ VPDB)"
}

plt.figure(figsize=(6, 5))

plt.scatter(
    df_plot["growth_rate"],
    df_plot[isotope],
    color = "green",
    s= 10
)

plt.xlabel("Growth rate (mm/yr)")
plt.ylabel(labels[isotope])

plt.gca().invert_yaxis()
plt.grid(True)

plt.title(f"{labels[isotope]} vs Growth Rate - Cueva del Diamante")

plt.show()

#%% Interpolar temperaturas e gerar gráfics GR vs Temp

#dados do espeleotema selecionado
df_plot = df_isotopes[mask].sort_values("age")

# dados de temperatura correspondentes à mesma caverna e espeleotema
df_temp_plot = df_temp[
    (df_temp["caves"] == df_plot["caves"].iloc[0]) &
    (df_temp["stalagmite"] == df_plot["stalagmite"].iloc[0])
].sort_values("age")

#filtro
df_plot = df_plot[
    (df_plot["age"] >= df_temp_plot["age"].min()) &
    (df_plot["age"] <= df_temp_plot["age"].max())
]

# interpolação linear da temperatura para as idades do espeleotema
df_plot["temp_interp"] = np.interp(
    df_plot["age"],
    df_temp_plot["age"],
    df_temp_plot["temp"]
)

# gráfico exploratório: Growth Rate vs Temperature
plt.figure(figsize=(6, 5))

plt.scatter(
    df_plot["temp_interp"],
    df_plot["growth_rate"],
    s=8,
    color = "red"
)

plt.xlabel("Temperature (°C)")
plt.ylabel("Growth rate (mm/yr)")
plt.grid(True)

plt.title("Growth Rate vs Temperature (interpolated) - Caverna Botuverá")
plt.show()

#%% criar df_final

dfs_final = []

# loop por caverna + estalagmite
for (cave, stal), df_cave in df_isotopes.groupby(["caves", "stalagmite"]):

    df_cave = df_cave.sort_values("age").copy()

    # pegar temperatura correspondente
    df_temp_cave = df_temp[
        (df_temp["caves"] == cave) &
        (df_temp["stalagmite"] == stal)
    ].sort_values("age")

    # pular se não tiver temperatura
    if df_temp_cave.empty:
        continue

    # filtro de idade
    df_cave = df_cave[
        (df_cave["age"] >= df_temp_cave["age"].min()) &
        (df_cave["age"] <= df_temp_cave["age"].max())
    ]

    # interpolar temperatura
    df_cave["temp_interp"] = np.interp(
        df_cave["age"],
        df_temp_cave["age"],
        df_temp_cave["temp"]
    )

    dfs_final.append(df_cave)

# juntar tudo
df_final = pd.concat(dfs_final, ignore_index=True)

df_final = df_final[[
    "caves",
    "stalagmite",
    "latitude",
    "longitude",
    "depth",
    "age",
    "growth_rate",
    "O18",
    "C13",
    "temp_interp"
]].copy()

df_final.to_csv(r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\df_final_modelagem.csv",
    index=False
)