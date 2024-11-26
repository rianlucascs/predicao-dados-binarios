import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Graphs:
    """
    Classe para criar gráficos estatísticos e visualizações avançadas usando Matplotlib e Seaborn.
    
    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados.
        column (list/str): Colunas a serem usadas no gráfico.
        figsize (tuple): Tamanho do gráfico (largura, altura).
        linewidth (float): Espessura das linhas para gráficos de linha.
        marker (str): Marcador para gráficos de linha.
        title (str): Título do gráfico.
        xlabel (str): Rótulo do eixo X.
        ylabel (str): Rótulo do eixo Y.
        bins (int): Número de bins para histogramas.
        seta (bool): Define se deve exibir anotações no gráfico.
    """

    def __init__(self, df, column, figsize=(10, 6), linewidth=2, marker=None, title='', 
                 xlabel='Data', ylabel='', bins=None, seta=False):
        self.df = df
        self.column = column
        self.figsize = figsize
        self.linewidth = linewidth
        self.marker = marker
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.bins = bins
        self.seta = seta

    def linha(self):
        """Gráfico de linha com personalização estatística."""
        sns.set(style="whitegrid", palette="muted")
        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)
        sns.lineplot(x=self.df.index, y=self.column, data=self.df, marker=self.marker, color='darkblue', 
                     linewidth=self.linewidth, ax=ax)
        self._personalizar_grafico(ax)
        if self.seta:
            self._adicionar_anotacao(ax)
        plt.tight_layout()
        plt.show()

    def hisplot(self):
        """Gráfico de histograma com estimativa de densidade."""
        sns.set(style="whitegrid", palette="muted")
        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)
        sns.histplot(self.df[self.column], kde=True, bins=self.bins, color='darkblue', 
                     stat='density', linewidth=1.5, ax=ax)
        self._personalizar_grafico(ax)
        plt.tight_layout()
        plt.show()

    def correlacao(self):
        """Gráfico de dispersão entre duas variáveis."""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)
        self.df['variacao_percentual'] = self.df[self.column[0]].pct_change(1).shift(-1)
        sns.scatterplot(data=self.df, x='variacao_percentual', y=self.column[1], color='b', ax=ax)
        correlacao = self.df[self.column[0]].corr(self.df[self.column[1]])
        ax.set_title(f"Dispersão entre '{self.column[0]} (pct_change)' e '{self.column[1]}'\n"
                     f"Correlação de Pearson: {correlacao:.4f}", 
                     fontsize=14, fontweight='bold')
        self._personalizar_grafico(ax)
        plt.tight_layout()
        plt.show()

    def barplot(self):
        """Gráfico de barras para retornos anuais."""
        self.df = self.df.reset_index()
        self.df['Ano'] = self.df['Date'].dt.year
        retornos_anuais = self.df.groupby('Ano')['resultado_predicao'].sum()
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(12, 4), dpi=300)
        sns.barplot(x=retornos_anuais.index, y=retornos_anuais.values, color='skyblue', ax=ax)
        for i, value in enumerate(retornos_anuais.values):
            ax.text(i, value + 0.02, f"{value:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax.set_title("Retornos Anuais", fontsize=14, fontweight='bold')
        self._personalizar_grafico(ax)
        plt.tight_layout()
        plt.show()

    def _personalizar_grafico(self, ax):
        """Configuração de elementos básicos do gráfico."""
        ax.set_title(self.title, fontsize=16, fontweight='bold', family='Georgia')
        ax.set_xlabel(self.xlabel, fontsize=14, family='Arial')
        ax.set_ylabel(self.ylabel, fontsize=14, family='Arial')
        ax.tick_params(axis='x', rotation=45, labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)

    def _adicionar_anotacao(self, ax):
        """Adiciona uma anotação no gráfico."""
        max_price_value = self.df[self.column].iloc[-1]
        max_price_date = self.df.index[-1]
        ax.annotate(f'R$ {max_price_value:.2f}', xy=(max_price_date, max_price_value), 
                    xytext=(max_price_date, max_price_value + 2), 
                    arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->', lw=1), 
                    fontsize=10, color='red', fontweight='bold',
                    bbox=dict(facecolor='white', alpha=0.5, edgecolor='red', boxstyle='round,pad=0.3'))
