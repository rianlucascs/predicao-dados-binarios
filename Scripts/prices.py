from yfinance import download
import requests
from pandas import read_csv
from io import StringIO
import sys

INDICES = {
    'IDIV': 'Índice Dividendos BM&FBOVESPA (IDIV B3)',
    'MLCX': 'Índice MidLarge Cap (MLCX B3)',
    'SMLL': 'Índice Small Cap (SMLL B3)',
    'IVBX': 'Índice Valor (IVBX 2 B3)',
    'AGFS': 'Índice Agronegócio B3 (IAGRO B3)',
    'IFNC': 'Índice BM&FBOVESPA Financeiro (IFNC B3)',
    'IBEP': 'Índice Bovespa B3 Empresas Privadas (Ibov B3 Empresas Privadas)',
    'IBEE': 'Índice Bovespa B3 Estatais (Ibov B3 Estatais)',
    'IBHB': 'Índice Bovespa Smart High Beta B3 (Ibov Smart High Beta B3)',
    'IBLV': 'Índice Bovespa Smart Low Volatility B3 (Ibov Smart Low B3)',
    'IMOB': 'Índice Imobiliário (IMOB B3)',
    'UTIL': 'Índice Utilidade Pública BM&FBOVESPA (UTIL B3)',
    'ICON': 'Índice de Consumo (ICON B3)',
    'IEEX': 'Índice de Energia Elétrica (IEE B3)',
    'IFIL': 'Índice de Fundos de Investimentos Imobiliários de Alta Liquidez (IFIX L B3)',
    'IMAT': 'Índice de Materiais Básicos BM&FBOVESPA (IMAT B3)',
    'INDX': 'Índice do Setor Industrial (INDX B3)',
    'IBSD': 'Índice Bovespa Smart Dividendos B3 (Ibov Smart Dividendos B3)',
    'BDRX': 'Índice de BDRs Não Patrocinados-GLOBAL (BDRX B3)',
    'IFIX': 'Índice de Fundos de Investimentos Imobiliários (IFIX B3)'
}

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
        df_price = download(ticker, period='max', progress=False)
        df_price.columns = df_price.columns.droplevel(1)
        df_price.columns = list(df_price.columns)
        return df_price
    
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
            response = requests.get(url_setor(setor))
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro ao acessar a página: {e}')
        tickers_setor = read_csv(StringIO(response.text), delimiter=',')['Código'].values

        dict_series_setor = {}
        for i, ticker in enumerate(tickers_setor):
            sys.stdout.write(f'\r [*********************100%***********************]  {i + 1} of {len(tickers_setor)} completed')
            dict_series_setor[f'{ticker}.SA'] = Prices.get(f'{ticker}.SA')

        return dict_series_setor

    


    
        
        