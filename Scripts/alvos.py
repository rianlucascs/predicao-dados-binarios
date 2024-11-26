from numpy import where, nan
from pandas import isna, DataFrame


class Alvos:
    """
    Classe para calcular alvos financeiros com base em variações absolutas de preços.

    Esta classe fornece diferentes métodos de geração de alvos, incluindo binários, ternários e outros.
    Os alvos são baseados na diferença entre os preços de abertura e fechamento ajustados com um período
    de deslocamento definido.

    Atributos:
        df (DataFrame): DataFrame contendo os dados de preços, incluindo as colunas 'Close' e 'Open'.
        p (int): Número de períodos para deslocamento dos alvos.
    """

    def __init__(self, df: DataFrame, p: int):
        """
        Inicializa a classe Alvos com o DataFrame de preços e o período de deslocamento.

        Args:
            df (DataFrame): DataFrame contendo os dados de preços.
            p (int): Número de períodos para deslocar os alvos.

        Raises:
            ValueError: Se o DataFrame não contém as colunas 'Close' e 'Open'.
        """
        # Verifica se o DataFrame contém as colunas necessárias
        if not {'Close', 'Open'}.issubset(df.columns):
            raise ValueError("O DataFrame deve conter as colunas 'Close' e 'Open'.")

        # Verifica se 'p' é um número inteiro positivo
        if not isinstance(p, int) or p <= 0:
            raise ValueError("O parâmetro 'p' deve ser um número inteiro positivo.")

        self.df = df.copy() 
        self.p = p

        # Calcula a variação absoluta (Close - Open) e a desloca para o futuro
        self.df['variacao_absoluta'] = self.df['Close'] - self.df['Open']
        self.df['variacao_absoluta'] = self.df['variacao_absoluta'].shift(-p)

    def _correct_last_value(self, name_alvo: str) -> DataFrame:
        """
        Corrige o valor da última linha para a coluna especificada, se necessário.

        Args:
            name_alvo (str): Nome da coluna do alvo a ser corrigido.

        Returns:
            DataFrame: DataFrame com os valores corrigidos.
        """
        # Se a última linha contém 'NaN', corrige os valores dessa linha
        if isna(self.df.iloc[-1, self.df.columns.get_loc('variacao_absoluta')]):
            self.df.iloc[-1, self.df.columns.get_loc('variacao_absoluta')] = nan
            self.df.iloc[-1, self.df.columns.get_loc(name_alvo)] = nan
        return self.df

    @property
    def A_BINARIO(self) -> DataFrame:
        """
        Calcula o alvo binário baseado na variação absoluta.

        Retorna:
            DataFrame: DataFrame com a coluna 'alvo_binario' adicionada.
        """
        # Cria a coluna 'alvo_binario' com base na variação absoluta
        self.df['alvo_binario'] = where(self.df['variacao_absoluta'] > 0, 1, 0)
        return self._correct_last_value('alvo_binario')

    @property
    def B_TERNARIO(self) -> DataFrame:
        """
        Placeholder para o cálculo de um alvo ternário.

        Retorna:
            DataFrame: DataFrame com a lógica do alvo ternário aplicada (não implementado).
        """
        raise NotImplementedError("O método 'B_TERNARIO' ainda não foi implementado.")

    @property
    def C_QUATERNARIO(self) -> DataFrame:
        """
        Placeholder para o cálculo de um alvo quaternário.

        Retorna:
            DataFrame: DataFrame com a lógica do alvo quaternário aplicada (não implementado).
        """
        raise NotImplementedError("O método 'C_QUATERNARIO' ainda não foi implementado.")

    @property
    def D_QUINARIO(self) -> DataFrame:
        """
        Placeholder para o cálculo de um alvo quinário.

        Retorna:
            DataFrame: DataFrame com a lógica do alvo quinário aplicada (não implementado).
        """
        raise NotImplementedError("O método 'D_QUINARIO' ainda não foi implementado.")
