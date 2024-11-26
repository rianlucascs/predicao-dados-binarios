

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
    
    def __1__(self) -> DataFrame:
        return self.df['Close'].diff()
    
    def __2__(self) -> DataFrame:
        return self.df['Open'].diff()