import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def grafico_KDE(df_price, column, title, xlabel):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 3))
    # Plotando o histograma e a densidade (KDE)
    sns.histplot(df_price[column], kde=True, bins=30, color='darkblue', stat='density', linewidth=1.5)
    
    # Calculando estatísticas
    mean_return = np.mean(df_price[column])
    std_return = np.std(df_price[column])

    # Adicionando as estatísticas no gráfico
    plt.axvline(mean_return, color='darkred', linestyle='--', label=f'Média: {mean_return:.4f}')
    plt.axvline(mean_return + std_return, color='darkgreen', linestyle=':', label=f'1 Desvio Padrão: {mean_return + std_return:.4f}')
    plt.axvline(mean_return - std_return, color='darkgreen', linestyle=':')

    # Adicionando título e rótulos
    plt.title(title, fontsize=18, fontweight='bold', color='black')
    plt.xlabel(xlabel, fontsize=14, color='black')
    plt.ylabel('Densidade', fontsize=14, color='black')

    # Adicionando legenda com texto discreto
    plt.legend(facecolor='white', edgecolor='black', frameon=True)

    # Exibindo o gráfico
    plt.show()

def grafico_linha(df_price, column, title, xlabel='Date', ylabel='', label='', figsize=(12, 3)):
    df_price = df_price.reset_index()
    sns.set(style="whitegrid", palette="muted")
    plt.figure(figsize=figsize)

    # Plotando o gráfico de linha
    plt.plot(df_price['Date'], df_price[column], color='darkblue', label=label, linewidth=2)

    # Adicionando título e rótulos
    plt.title(title, fontsize=18, fontweight='bold')
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)

    # Adicionando legenda
    plt.legend()

    # Ajustando o layout do gráfico
    plt.xticks(rotation=45)  # Rotacionando os rótulos da data para facilitar a leitura
    plt.tight_layout()

    # Exibindo o gráfico
    plt.show()

def grafico_retorno(df_price, column, title, xlabel='Date', ylabel='', label='', figsize=(12, 3)):
    df_price = df_price.reset_index()  # Garantir que o índice está no formato correto
    sns.set(style="whitegrid", palette="muted")
    plt.figure(figsize=figsize)

    # Plotando o gráfico de linha
    plt.plot(df_price['Date'], df_price[column], color='darkblue', label=label, linewidth=2)

    # Adicionando título e rótulos
    plt.title(title, fontsize=18, fontweight='bold')
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    
    # Adicionando legenda
    plt.legend()

    # Ajustando o layout do gráfico
    plt.xticks(rotation=45)  # Rotacionando os rótulos da data para facilitar a leitura
    
    # Encontrando o valor final da variável e a data correspondente
    max_price_value = df_price[column].iloc[-1]
    max_price_date = df_price['Date'].iloc[-1]  # Usar 'Date' diretamente para pegar a última data

    # Anotando no gráfico o valor final
    plt.annotate(f'R${max_price_value:.2f}',
                     xy=(max_price_date, max_price_value),  # Posição no gráfico
                     xytext=(max_price_date, max_price_value + 2),  # Deslocando o texto um pouco acima
                     arrowprops=dict(
                         facecolor='red',           
                         edgecolor='red',       
                         arrowstyle='->',           
                         lw=1,                       
                         connectionstyle='arc3,rad=-0.2'  
                     ),
                     fontsize=10,  # Tamanho da fonte
                     color='red',  # Cor do texto
                     fontweight='bold',  # Negrito
                     bbox=dict(facecolor='white', alpha=0.5, edgecolor='red', boxstyle='round,pad=0.3')  # Caixa de fundo
                     )
    
    # Ajuste para a exibição
    plt.tight_layout()

    # Exibindo o gráfico
    plt.show()

def grafico_sinais(dados, title):
    # Dados de exemplo
    dados = dados['predicao'].value_counts()
    dados = {'Sell': dados[0.0], 'Buy': dados[1.0]}
    labels = list(dados.keys())
    valores = list(dados.values())

    # Estilo do gráfico
    sns.set(style="whitegrid", palette="muted")

    # Configurando a figura
    plt.figure(figsize=(4, 4))

    # Criando o gráfico de pizza
    colors = ['skyblue', 'orange']  # Cores alinhadas com os gráficos anteriores
    explode = [0.05, 0]  # Destacar um segmento, opcional
    plt.pie(
        valores, 
        labels=labels, 
        autopct='%1.1f%%',  # Mostrar porcentagem
        startangle=90,  # Começar no topo
        colors=colors, 
        explode=explode, 
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}  # Borda dos segmentos
    )

    # Adicionando título
    plt.title(title, fontsize=18, fontweight='bold')

    # Exibindo o gráfico
    plt.tight_layout()
    plt.show()


def grafico_retorno_anual(dados, coluna_serie_retorno, title, xlabel='Ano', ylabel='Retorno Acumulado',
                          quantidade_de_contratos=100):
    # Garantir que os dados estão no formato correto
    dados = dados.reset_index()
    dados['Ano'] = dados['Date'].dt.year  # Extraindo o ano
    
    # Agrupando por ano
    retornos_anuais = dados.groupby('Ano')[coluna_serie_retorno].sum() * quantidade_de_contratos
    
    # Configurando o estilo do gráfico
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 4))
    
    # Criando o gráfico de barras sem o uso de `palette`
    sns.barplot(
        x=retornos_anuais.index, 
        y=retornos_anuais.values, 
        color='skyblue',  # Usando uma cor fixa
        edgecolor='black'
    )
    
    # Adicionando valores acima de cada barra
    for i, value in enumerate(retornos_anuais.values):
        plt.text(
            i, value + 0.02, f"{value:.2f}", 
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )

    # Adicionando título e rótulos
    plt.title(title, fontsize=18, fontweight='bold', color='black')
    plt.xlabel(xlabel, fontsize=14, color='black')
    plt.ylabel(ylabel, fontsize=14, color='black')
    
    # Ajustando layout e exibindo
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()