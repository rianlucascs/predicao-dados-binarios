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
        """Gráfico de linha com personalização estatística e anotações opcionais."""
        
        # Configuração de estilo
        sns.set(style="whitegrid", palette="muted")
        
        # Criar a figura e o eixo
        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)
        
        # Criar gráfico de linha
        sns.lineplot(x=self.df.index, y=self.df[self.column], data=self.df, marker=self.marker, 
                    color='#66A3A1', linewidth=self.linewidth, ax=ax)
        
        # Personalização do gráfico
        # Título
        ax.set_title(self.title, fontsize=self.fontsize_title, fontweight='bold')

        # Rótulos dos eixos
        ax.set_xlabel(self.xlabel, fontsize=self.fontsize_xlabel)
        ax.set_ylabel(self.ylabel, fontsize=self.fontsize_ylabel)
        
        # Ajustes adicionais para o gráfico
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(12)  # Ajuste do tamanho da fonte dos rótulos
            label.set_fontweight('bold')  # Ajuste do peso da fonte

        # Adicionar anotações, se solicitado
        if self.seta:
            max_price_value = self.df[self.column].iloc[-1]
            max_price_date = self.df.index[-1]

            # Cor da seta e do texto para um tom de azul suave
            arrow_color = '#66A3A1'  # Azul esverdeado suave, combinando com a paleta existente

            # Ajustar a posição da anotação para um espaçamento mais confortável
            y_offset = 5  # Deslocamento vertical para o texto

            # Criar anotação com melhorias visuais
            ax.annotate(f'R$ {max_price_value:.2f}', 
                        xy=(max_price_date, max_price_value), 
                        xytext=(max_price_date, max_price_value + y_offset),  # Ajustando a posição vertical
                        arrowprops=dict(facecolor=arrow_color, edgecolor=arrow_color, arrowstyle='->', lw=1.5), 
                        fontsize=12,  # Tamanho maior para melhorar a legibilidade
                        color=arrow_color,  # Usar o mesmo tom de azul
                        fontweight='bold',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor=arrow_color, boxstyle='round,pad=0.3'))  # Opacidade do fundo ajustada
        
        # Ajustar o layout para evitar sobreposição de elementos
        plt.tight_layout()
        
        # Exibir o gráfico
        plt.show()


    def hisplot(self):
        """Gráfico de histograma com estimativa de densidade e informações estatísticas."""

        # Configuração do estilo do gráfico
        sns.set(style="whitegrid", palette="muted")
        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)
        
        # Criar o histograma com KDE
        sns.histplot(self.df[self.column], kde=True, bins=self.bins, color='#4F9DC7', 
                    stat='density', linewidth=1.5, ax=ax)
        
        # Calcular a média e o desvio padrão dos dados
        mean_return = np.mean(self.df[self.column])
        std_return = np.std(self.df[self.column])
        
        # Adicionar linhas verticais para a média e o desvio padrão
        ax.axvline(mean_return, color='darkred', linestyle='--', label=f'Média: {mean_return:.4f}')
        ax.axvline(mean_return + std_return, color='darkgreen', linestyle=':', label=f'1 Desvio Padrão: {mean_return + std_return:.4f}')
        ax.axvline(mean_return - std_return, color='darkgreen', linestyle=':')

        # Personalizar título e eixos
        ax.set_title(f"Distribuição de {self.column} com Estimativa de Densidade", fontsize=self.fontsize_title, fontweight='bold')
        ax.set_xlabel(f"{self.column} (Valores)", fontsize=self.fontsize_xlabel)
        ax.set_ylabel("Densidade", fontsize=self.fontsize_ylabel)

        # Ajustes adicionais para o gráfico
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(12)  # Ajuste do tamanho da fonte dos rótulos
            label.set_fontweight('bold')  # Ajuste do peso da fonte

        # Exibir legenda e ajustar layout
        plt.legend(facecolor='white', edgecolor='black', frameon=True)
        plt.tight_layout()
        plt.show()

    def correlacao(self):
        """Gráfico de dispersão entre duas variáveis com informações estatísticas e melhorias visuais."""
        
        # Calcular a variação percentual e armazenar na coluna 'variacao_percentual'
        self.df['variacao_percentual'] = self.df[self.column[0]].pct_change(1).shift(-1)
        
        # Calcular a correlação de Pearson entre as duas variáveis
        correlacao = self.df[self.column[0]].corr(self.df[self.column[1]])
        
        # Título do gráfico com a correlação
        self.title = f"Correlação entre {self.column[0]} (Variação Percentual Deslocada) e {self.column[1]}"
        
        # Configuração do gráfico
        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)
        
        # Criar gráfico de dispersão
        scatter = sns.scatterplot(data=self.df, x='variacao_percentual', y=self.column[1], color='#4F9DC7', ax=ax, s=100, edgecolor='black', linewidth=1.5)
        
        # Adicionar linha de regressão para evidenciar a tendência
        sns.regplot(data=self.df, x='variacao_percentual', y=self.column[1], scatter=False, ax=ax, color='darkblue', line_kws={'linewidth': 2, 'linestyle': '--'})
        
        # Adicionar texto com correlação no gráfico
        ax.text(0.05, 0.95, f"Correlação de Pearson: {correlacao:.4f}", transform=ax.transAxes, fontsize=12, verticalalignment='top', color='darkblue', fontweight='bold')
        
        # Informações adicionais sobre a distribuição dos dados
        mean_x = self.df['variacao_percentual'].mean()
        mean_y = self.df[self.column[1]].mean()
        ax.text(0.05, 0.90, f"Média (X): {mean_x:.4f}", transform=ax.transAxes, fontsize=10, verticalalignment='top', color='black')
        ax.text(0.05, 0.85, f"Média (Y): {mean_y:.4f}", transform=ax.transAxes, fontsize=10, verticalalignment='top', color='black')

        # Personalizar o gráfico com título e eixos
        ax.set_title(self.title, fontsize=self.fontsize_title, fontweight='bold')
        ax.set_xlabel(f"Variação Percentual de {self.column[0]}", fontsize=self.fontsize_xlabel)
        ax.set_ylabel(f"Feature: {self.column[1]}", fontsize=self.fontsize_ylabel)

        # Ajustes adicionais para o gráfico
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(12)  # Ajuste do tamanho da fonte dos rótulos
            label.set_fontweight('bold')  # Ajuste do peso da fonte

        # Layout do gráfico
        plt.tight_layout()
        plt.show()

    def barplot(self):
        """Gráfico de barras para retornos anuais com barras mais finas."""
        self.df = self.df.reset_index()
        self.df['Ano'] = self.df['Date'].dt.year
        retornos_anuais = self.df.groupby('Ano')['resultado_predicao'].sum()

        # Definir a cor das barras (azul claro)
        azul = '#4F9DC7'  # O tom de azul escolhido

        # Configuração do gráfico
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)

        # Criar gráfico de barras com a cor azul definida e largura ajustada
        sns.barplot(x=retornos_anuais.index, y=retornos_anuais.values, color=azul, ax=ax, width=0.5)  # Ajustar a largura das barras

        # Adicionar bordas finas nas barras
        for bar in ax.patches:
            bar.set_edgecolor('white')  # Borda branca para as barras
            bar.set_linewidth(1.5)

        # Adicionar os valores no topo das barras
        for i, value in enumerate(retornos_anuais.values):
            ax.text(i, value + 0.02, f"{value:.2f}", ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

        # Personalização do gráfico
        # Título
        ax.set_title(self.title, fontsize=self.fontsize_title, fontweight='bold')

        # Ajustar os rótulos dos eixos
        ax.set_xlabel(self.xlabel, fontsize=self.fontsize_xlabel)
        ax.set_ylabel(self.ylabel, fontsize=self.fontsize_ylabel)

        # Ajustes adicionais para o gráfico
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(12)  # Ajuste do tamanho da fonte dos rótulos
            label.set_fontweight('bold')  # Ajuste do peso da fonte

        # Ajustes do layout
        plt.tight_layout()
        plt.show()

    def pio(self):
        dados = self.df.filter(like=self.column).value_counts()
        dados = {'Sell': dados[0.0], 'Buy': dados[1.0]}
        labels = list(dados.keys())
        valores = list(dados.values())

        # Cores em tons de azul
        colors = ['#A3C4DC', '#4F9DC7']  # Azul claro e azul médio
        explode = [0.1, 0]  # Destacar o primeiro segmento de forma mais pronunciada

        # Definir o estilo do gráfico
        sns.set(style="whitegrid", palette="muted")
        fig, ax = plt.subplots(figsize=self.figsize, dpi=100)
        
        # Criar gráfico de pizza com efeitos de borda e sombra
        wedges, texts, autotexts = plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90, 
                                            colors=colors, explode=explode, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}, 
                                            shadow=True)
        
        # Personalização do gráfico
        # Título
        ax.set_title(self.title, fontsize=self.fontsize_title, fontweight='bold')
        
        # Ajustar o rótulo do eixo (mesmo que para gráficos de pizza, este não é tão relevante)
        ax.set_xlabel(self.xlabel, fontsize=self.fontsize_xlabel)
        ax.set_ylabel(self.ylabel, fontsize=self.fontsize_ylabel)

        # Ajustes de fontes e tamanho dos textos
        for autotext in autotexts:
            autotext.set(fontsize=12, fontweight='bold', color='white')
        for text in texts:
            text.set(fontsize=14, fontweight='bold', color='black')

        # Ajuste para o layout mais limpo e bonito
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

        # Definir cores em tons de azul
        blues = ['#003366', '#4682b4', '#5f9ea0']  # Azul escuro, médio e claro

        # Adicionar barras e valores no topo
        for i, dataset in enumerate(datasets):
            bar_positions = x + i * width
            bar_heights = [values[metric][i] for metric in metrics]
            bars = ax.bar(bar_positions, bar_heights, width, label=dataset, color=blues[i])
            
            # Adicionar valores no topo de cada barra com formato melhorado
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,  # Centralizar o texto
                    height + 0.02,                     # Ajustar a posição vertical
                    f"{height:.2f}",                   # Formatação do valor
                    ha='center', va='bottom',          # Centralizar e alinhar na parte de baixo
                    fontsize=12, fontweight='bold',
                    color='black'
                )

        # Personalizar o gráfico
        ax.set_title("Avaliação dos Retornos Médios ao Longo de Diferentes Períodos de Tempo", fontsize=self.fontsize_title, fontweight='bold')
        ax.set_xlabel("Métricas", fontsize=self.fontsize_xlabel, family='Arial')
        ax.set_ylabel("Valores (%)", fontsize=self.fontsize_ylabel, family='Arial')
        ax.set_xticks(x + width)
        ax.set_xticklabels(metrics, fontsize=self.tick_params_labelsize, rotation=45)
        ax.legend(title="Conjunto de Dados", fontsize=5)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Melhorar layout para maior clareza
        plt.tight_layout(pad=3.0)  # Aumentar o espaçamento entre os elementos

        # Exibir o gráfico
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
        width = 0.2  # Largura das barras ajustada para evitar sobreposição

        fig, ax = plt.subplots(figsize=self.figsize, dpi=300)

        # Definir cores para cada conjunto de dados
        colors = ['#003366', '#4682b4', '#5f9ea0'] # Azul escuro, médio e claro

        # Adicionar barras e valores no topo
        for i, dataset in enumerate(datasets):
            bar_positions = x + i * width
            bar_heights = [values[metric][i] for metric in metrics]
            bars = ax.bar(bar_positions, bar_heights, width, label=dataset, color=colors[i])
            
            # Adicionar valores no topo de cada barra com formato melhorado
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,  # Centralizar o texto
                    height + 0.01,                     # Ajustar um pouco mais a posição vertical
                    f"{height:.2f}",                   # Formatação do valor
                    ha='center', va='bottom',          # Centralizar e alinhar na parte de baixo
                    fontsize=10, fontweight='bold',
                    color='black'
                )

        # Personalizar o gráfico
        ax.set_title("Comparação de Métricas por Conjunto de Dados", fontsize=self.fontsize_title, fontweight='bold')
        ax.set_xlabel("Métricas", fontsize=self.fontsize_xlabel)
        ax.set_ylabel("Valores (%)", fontsize=self.fontsize_ylabel)
        ax.set_xticks(x + width)
        ax.set_xticklabels(metrics, fontsize=self.tick_params_labelsize, rotation=45)
        ax.legend(title="Conjunto de Dados", fontsize=5)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Melhorar layout para maior clareza
        plt.tight_layout(pad=3.0)  # Aumentar o espaçamento entre os elementos

        # Exibir o gráfico
        plt.show()
