import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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
                 xlabel='Data', ylabel='', bins=None, seta=False, fontsize_title=16,
                 fontsize_xlabel=14, fontsize_ylabel=14, tick_params_labelsize=12):
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
        self.fontsize_title = fontsize_title
        self.fontsize_xlabel = fontsize_xlabel
        self.fontsize_ylabel = fontsize_ylabel
        self.tick_params_labelsize = tick_params_labelsize

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
        self.title = f"Dispersão entre '{self.column[0]} (pct_change) (shift(-1))' e Feature: '{self.column[1]}' - Correlação de Pearson: {correlacao:.4f}"
        self._personalizar_grafico(ax)
        plt.tight_layout()
        plt.show()

    def barplot(self):
        """Gráfico de barras para retornos anuais."""
        self.df = self.df.reset_index()
        self.df['Ano'] = self.df['Date'].dt.year
        retornos_anuais = self.df.groupby('Ano')['resultado_predicao'].sum()
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)
        sns.barplot(x=retornos_anuais.index, y=retornos_anuais.values, color='skyblue', ax=ax)
        for i, value in enumerate(retornos_anuais.values):
            ax.text(i, value + 0.02, f"{value:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
        self._personalizar_grafico(ax)
        plt.tight_layout()
        plt.show()

    def pio(self):

        dados = self.df.filter(like=self.column).value_counts()
        dados = {'Sell': dados[0.0], 'Buy': dados[1.0]}
        labels = list(dados.keys())
        valores = list(dados.values())

        colors = ['skyblue', 'yellowgreen']  # Cores alinhadas com os gráficos anteriores
        explode = [0.05, 0]  # Destacar um segmento, opcional

        sns.set(style="whitegrid", palette="muted")
        fig, ax = plt.subplots(figsize=self.figsize, dpi=150)
        plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode, 
            wedgeprops={'edgecolor': 'black', 'linewidth': 1})
        self._personalizar_grafico(ax)

        plt.tight_layout()
        plt.show()

    def comparar_retornos(self, retorno_data):
        """
        Gráfico de barras agrupadas para comparação de retornos entre 'train', 'test' e 'after_test'.
        
        Parâmetros:
            retorno_data (dict): Dicionário contendo as métricas de retorno.
        """
        # Preparar os dados
        metrics = list(retorno_data['train'].keys())  # Métricas (ex.: daily, weekly)
        datasets = list(retorno_data.keys())  # Conjuntos de dados (train, test, after_test)
        values = {metric: [retorno_data[dataset][metric] for dataset in datasets] for metric in metrics}
        
        # Configuração do gráfico
        x = np.arange(len(metrics))  # Posições das métricas no eixo X
        width = 0.25  # Largura das barras

        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)

        # Adicionar barras e valores no topo
        for i, dataset in enumerate(datasets):
            bar_positions = x + i * width
            bar_heights = [values[metric][i] for metric in metrics]
            bars = ax.bar(bar_positions, bar_heights, width, label=dataset)
            
            # Adicionar valores no topo de cada barra
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,  # Centralizar o texto
                    height,                            # Posição vertical
                    f"{height:.2f}",                   # Formatação do valor
                    ha='center', va='bottom',          # Centralizar e alinhar na parte de baixo
                    fontsize=10, fontweight='bold'
                )

        # Personalizar o gráfico
        ax.set_title("Comparação da Média dos Retornos por Métrica de t", fontsize=self.fontsize_title, fontweight='bold', family='Georgia')
        ax.set_xlabel("Métricas", fontsize=self.fontsize_xlabel, family='Arial')
        ax.set_ylabel("Valores (%)", fontsize=self.fontsize_ylabel, family='Arial')
        ax.set_xticks(x + width)
        ax.set_xticklabels(metrics, fontsize=self.tick_params_labelsize, rotation=45)
        ax.legend(title="Conjunto de Dados", fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Exibir o gráfico
        plt.tight_layout()
        plt.show()

    def comparar_metricas(self, metric_data):
        """
        Gráfico de barras agrupadas para comparar métricas ('accuracy', 'precision', 'recall', 'f1_score') 
        entre 'train', 'test' e 'after_test'.
        
        Parâmetros:
            metric_data (dict): Dicionário contendo as métricas de cada conjunto de dados.
        """
        # Preparar os dados
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']  # Lista fixa de métricas
        datasets = list(metric_data.keys())  # Conjuntos de dados (train, test, after_test)

        # Criar estrutura de valores para cada métrica por dataset
        values = {metric: [metric_data[dataset][metric] for dataset in datasets] for metric in metrics}
        
        # Configuração do gráfico
        x = np.arange(len(metrics))  # Posições das métricas no eixo X
        width = 0.25  # Largura das barras

        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)

        # Adicionar barras e valores no topo
        for i, dataset in enumerate(datasets):
            bar_positions = x + i * width
            bar_heights = [values[metric][i] for metric in metrics]
            bars = ax.bar(bar_positions, bar_heights, width, label=dataset)
            
            # Adicionar valores no topo de cada barra
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,  # Centralizar o texto
                    height + 0.01,                     # Posição vertical um pouco acima da barra
                    f"{height:.2f}",                   # Formatação do valor
                    ha='center', va='bottom',          # Centralizar e alinhar na parte de baixo
                    fontsize=10, fontweight='bold'
                )

        # Personalizar o gráfico
        ax.set_title("Comparação de Métricas por Conjunto de Dados", fontsize=self.fontsize_title, fontweight='bold')
        ax.set_xlabel("Métricas", fontsize=self.fontsize_xlabel)
        ax.set_ylabel("Valores (%)", fontsize=self.fontsize_ylabel)
        ax.set_xticks(x + width)
        ax.set_xticklabels(metrics, fontsize=self.tick_params_labelsize, rotation=45)
        ax.legend(title="Conjunto de Dados", fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Exibir o gráfico
        plt.tight_layout()
        plt.show()



    def _personalizar_grafico(self, ax):
        
        """Configuração de elementos básicos do gráfico."""
        ax.set_title(self.title, fontsize=self.fontsize_title, fontweight='bold', family='Georgia')
        ax.set_xlabel(self.xlabel, fontsize=self.fontsize_xlabel, family='Arial')
        ax.set_ylabel(self.ylabel, fontsize=self.fontsize_ylabel, family='Arial')
        ax.tick_params(axis='x', rotation=45, labelsize=self.tick_params_labelsize)
        ax.tick_params(axis='y', labelsize=self.tick_params_labelsize)
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
