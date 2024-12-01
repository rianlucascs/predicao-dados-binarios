from yfinance import download
import requests
from pandas import read_csv, to_datetime
from io import StringIO
import sys

# Função para gerar a URL de um setor específico, acessando o repositório do GitHub
url_setor = lambda setor: f'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/1.%20%C3%8Dndices%20de%20Segmentos%20e%20Setoriais/Setores/{setor}/Tabela_{setor}.csv'

class Prices:
    """
    Classe para obtenção de preços históricos e dados de ativos setoriais.

    Métodos:
        get(ticker: str) -> pandas.DataFrame:
            Retorna os preços históricos de um ativo financeiro.

        get_setor(setor: str) -> dict:
            Retorna séries históricas dos ativos de um setor específico.
    """

    @staticmethod
    def get(ticker: str):
        """
        Obtém os preços históricos de um ativo.

        Args:
            ticker (str): Ticker do ativo (exemplo: 'PETR4.SA').

        Returns:
            pandas.DataFrame: Dados históricos do ativo.
        """
        # Baixa os dados históricos do ativo usando a API do Yahoo Finance
        df = download(ticker, period='max', progress=False)

        # Remove o nível extra das colunas, deixando apenas o nome da coluna
        df.columns = df.columns.droplevel(1)
        df.columns = list(df.columns)

        return df
    
    @staticmethod
    def get_setor_B3(setor: str):
        """
        Obtém séries históricas de ativos de um setor.

        Args:
            setor (str): Nome do setor (exemplo: 'UTIL').

        Returns:
            dict: Dicionário contendo os ativos como chaves e os preços históricos como valores.
        """
        try:
            # Acessa a URL para obter a lista de tickers do setor
            response = requests.get(url_setor(setor))
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro ao acessar a página: {e}')
        
        # Lê os tickers de um arquivo CSV no formato de texto e extrai a coluna 'Código'
        tickers_setor = read_csv(StringIO(response.text), delimiter=',')['Código'].values

        # Cria um dicionário para armazenar as séries históricas dos ativos
        dict_series_setor = {}
        for i, ticker in enumerate(tickers_setor):
            sys.stdout.write(f'\r [*********************100%***********************]  {i + 1} of {len(tickers_setor)} completed')
            
            # Para cada ticker, obtém os dados históricos e adiciona ao dicionário
            dict_series_setor[f'{ticker}.SA'] = Prices.get(f'{ticker}.SA')

        return dict_series_setor

# from datetime import datetime
# df = Prices.get('BBDC4.SA')
# # df.index = df.index.tz_localize(None)
# date = datetime.strptime('2012-05-11', '%Y-%m-%d')
# print(df.loc[date:])

    

    
        
        