import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pingouin as pg
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'
 
#%% Importando o banco de dados
 
df = pd.read_csv(r"G:\Meu Drive\MBA ESALQ USP\TCC\Bancos de Dados\df_final_modelagem.csv")
 
# Variáveis utilizadas na clusterização (TC incluída)
variaveis = ['growth_rate', 'temp_interp', 'O18', 'C13']
 
# Removendo linhas com valores ausentes
df_kmeans = df[['caves'] + variaveis].dropna().copy()
 
# Separando apenas as variáveis numéricas
dados_cluster = df_kmeans[variaveis]
 
#%% Estatísticas descritivas
 
print(dados_cluster.describe())
# As variáveis estão em escalas distintas — padronização necessária
 
#%% Padronização por Z-Score
 
dados_pad = dados_cluster.apply(zscore, ddof=1)
 
print(np.round(dados_pad.mean(), 3))
print(np.round(dados_pad.std(), 3))
 
#%% Identificação do número de clusters — Método do Cotovelo (Elbow)
 
elbow = []
K = range(1, 11)
for k in K:
    kmeanElbow = KMeans(n_clusters=k, init='random', random_state=100).fit(dados_pad)
    elbow.append(kmeanElbow.inertia_)
 
plt.figure(figsize=(16, 8), dpi=600)
plt.plot(K, elbow, marker='o')
plt.xlabel('Nº Clusters', fontsize=16)
plt.xticks(range(1, 11))
plt.ylabel('WCSS', fontsize=16)
plt.title('Método de Elbow', fontsize=16)
plt.show()
 
#%% Identificação do número de clusters — Método da Silhueta
 
silhueta = []
I = range(2, 11)
for i in I:
    kmeansSil = KMeans(n_clusters=i, init='random', random_state=100).fit(dados_pad)
    silhueta.append(silhouette_score(dados_pad, kmeansSil.labels_))
 
plt.figure(figsize=(16, 8), dpi=600)
plt.plot(range(2, 11), silhueta, color='purple', marker='o')
plt.xlabel('Nº Clusters', fontsize=16)
plt.ylabel('Silhueta Média', fontsize=16)
plt.title('Método da Silhueta', fontsize=16)
plt.axvline(x=silhueta.index(max(silhueta)) + 2, linestyle='dotted', color='red')
plt.show()
 
print("Silhouette scores:", dict(zip(range(2, 11), [round(s, 3) for s in silhueta])))
 
#%% K-means final
 
# Ajuste o valor de K após observar os gráficos acima
K_final = 3  # <- altere se necessário
 
kmeans_final = KMeans(n_clusters=K_final, init='random', random_state=100).fit(dados_pad)
 
# Adicionando os clusters ao dataframe
df_kmeans['cluster_kmeans'] = kmeans_final.labels_
dados_pad['cluster_kmeans'] = kmeans_final.labels_
df_kmeans['cluster_kmeans'] = df_kmeans['cluster_kmeans'].astype('category')
dados_pad['cluster_kmeans'] = dados_pad['cluster_kmeans'].astype('category')
 
#%% Coordenadas dos centroides
 
cent_finais = pd.DataFrame(kmeans_final.cluster_centers_)
cent_finais.columns = variaveis
cent_finais.index.name = 'cluster'
print(cent_finais)
 
#%% quais variáveis mais discriminam os clusters
 
# growth_rate
pg.anova(dv='growth_rate',
         between='cluster_kmeans',
         data=dados_pad,
         detailed=True).T
 
# temp_interp
pg.anova(dv='temp_interp',
         between='cluster_kmeans',
         data=dados_pad,
         detailed=True).T
 
# O18
pg.anova(dv='O18',
         between='cluster_kmeans',
         data=dados_pad,
         detailed=True).T
 
# C13
pg.anova(dv='C13',
         between='cluster_kmeans',
         data=dados_pad,
         detailed=True).T
 
#%% Gráfico 3D interativo dos clusters
 
fig = px.scatter_3d(df_kmeans,
                    x='temp_interp',
                    y='growth_rate',
                    z='O18',
                    color='cluster_kmeans',
                    symbol='caves',
                    title='K-means — TC, Temperatura e δ¹⁸O')
 
fig.write_html('kmeans_3d.html')
 
#%% Distribuição das cavernas por cluster
 
distribuicao = pd.crosstab(df_kmeans['caves'], df_kmeans['cluster_kmeans'])
print("\nDistribuição absoluta:")
print(distribuicao)
 
distribuicao_pct = pd.crosstab(df_kmeans['caves'], df_kmeans['cluster_kmeans'],
                                normalize='index').round(2) * 100
print("\nDistribuição relativa (%):")
print(distribuicao_pct)
 
#%% Perfil médio dos clusters (variáveis originais)
 
perfil = df_kmeans.groupby('cluster_kmeans', observed=True)[variaveis].mean().T
print("\nPerfil médio dos clusters:")
print(perfil.round(2))