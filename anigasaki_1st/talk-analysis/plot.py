# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams


# import csv files.
df_data = pd.read_csv('data.csv', index_col=0)
df_clr = pd.read_csv('color.csv')

# convert to minutes.
df_data = df_data/60

# general plot settings
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio',
                               'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
sns.set_palette(df_clr['Color'])

# heatmap part
plt.figure()
g1 = sns.heatmap(df_data.T, square=True, cbar_kws={
                 'label': '会話時間 (分)'}, cmap='viridis')
g1.set(xlabel='話', ylabel='キャラクター')
plt.savefig('heatmap.png', format="png", dpi=300, bbox_inches="tight")

# clustering part
g2 = sns.clustermap(df_data, metric='correlation',
                    z_score=0, cmap='viridis', cbar_kws={'label': 'Row Z-score'})
plt.savefig('clustermap.png', format="png", dpi=300, bbox_inches="tight")

# Allign the dataframe for violin plot
df_melt = df_data.melt()

# violin plot part
ax = plt.subplots(figsize=(12, 9))
ax = sns.violinplot(x='variable', y="value", data=df_melt,
                    inner="quartile", color="0.85")
sns.swarmplot(x=df_melt['variable'], y=df_melt['value'])
ax.set(xlabel='キャラクター', ylabel='会話時間 (分)')
plt.savefig('violin.png', format="png", dpi=300, bbox_inches="tight")

ax = plt.subplots(figsize=(12, 9))
ax = sns.barplot(x='variable', y="value", data=df_melt, capsize=.2)
ax.set(xlabel='キャラクター', ylabel='会話時間 (分)')
plt.savefig('bar.png', format="png", dpi=300, bbox_inches="tight")
