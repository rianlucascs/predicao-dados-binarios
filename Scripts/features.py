

from pandas import DataFrame
from typing import Union, List

class Features:
    """
    Classe para calcular diferentes tipos de features a partir de dados de preços.

    Attributes:
        df (pd.DataFrame): DataFrame contendo os dados de preços, como 'Close' e 'Open'.

    Methods:
        get(F: Union[list[int], int]) -> pd.DataFrame:
            Calcula as features especificadas e as adiciona ao DataFrame.

        __?__() -> pd.Series:
            ...

    """
    def __init__(self, df: DataFrame):
        """
        Inicializa a classe Features com um DataFrame de preços.

        Args:
            df (pd.DataFrame): DataFrame contendo os dados de preços.
        """
        self.df = df.copy()

    def get(self, F: Union[int, List[int]]) -> DataFrame:
        """
        Calcula as features especificadas e as adiciona ao DataFrame.

        Args:
            F (Union[int, list[int]]): Um número inteiro ou uma lista de inteiros representando
            as features a serem calculadas.

        Returns:
            pd.DataFrame: DataFrame com as novas features adicionadas.

        Raises:
            ValueError: Se uma feature especificada não está implementada.
            TypeError: Se o argumento 'F' não for um inteiro ou uma lista de inteiros.
        """
        if isinstance(F, int):
            self.F = [F]
        
        if isinstance(F, list):
            for f in F:
                method_name  = f'__{f}__'
                if hasattr(self, method_name):
                    self.df[f'__{f}__'] = getattr(self, method_name)()
                else:
                    raise ValueError(f"A feature '__{f}__' não está implementada.")
        else:
            raise TypeError("O parâmetro 'F' deve ser um inteiro ou uma lista de inteiros.")

        return self.df
    
    # -----------------------------------------------------------------------------------------

    # Adicione aqui suas features seguindo a ordem númerica

    # Colunas permitidas df[['Adj Close', 'Close', 'High', 'Low', 'Open',  'Volume']]

    def __1__(self) -> DataFrame:
        return self.df['Close'].diff()
    
    def __2__(self) -> DataFrame:
        return self.df['Open'].diff()

    def __3__(self):
        # NOTE: ticker = BBDC4, start = '2012-05-11', end = '2022-05-11', p = 1
        W = lambda x, window_size=5: x.rolling(window_size).sum()
        S = lambda x, window_size=5: x.rolling(window_size).std() / x.rolling(window_size).mean()
        J = lambda x, window_size=5, quantile=0.5: x.rolling(window_size).quantile(quantile)
        U = lambda x: x.diff().diff()
        adj_close = self.df['Adj Close'].pct_change(1)                
        low = self.df['Low'].pct_change(1)        
        high = self.df['High'].pct_change(1)       
        q = W(S(J(low, 6, 0.10) - J(high, 6, 0.10), 6), 6)
        r = W(q, 4) / J(U(adj_close), 5, 0.75) 
        u = r ** 2
        return u