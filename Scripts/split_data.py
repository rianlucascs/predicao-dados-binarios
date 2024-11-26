from datetime import datetime, timedelta
from pandas import DataFrame, DatetimeIndex, Timestamp
from typing import Optional

class SplitData:
    """
    Classe para dividir um DataFrame em conjuntos de treino, teste e pós-teste.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem divididos. 
                           Deve ter um índice do tipo `DatetimeIndex`.
        start (str, opcional): Data inicial do intervalo de análise no formato 'YYYY-MM-DD'. 
                               Se não fornecido, usa a data mínima do índice.
        end (str, opcional): Data final do intervalo de análise no formato 'YYYY-MM-DD'.
                             Se não fornecido, usa a data máxima do índice.
        p (float, opcional): Proporção de dados para o conjunto de treino (0 < p < 1).
                             O padrão é 0.50.
        step_size (int, opcional): Número de dias a ser adicionado às datas `start` e `end`.
                                    Se fornecido, move o intervalo de dados.
    """
    def __init__(self, df: DataFrame, start: Optional[str] = None, end: Optional[str] = None, 
                 p: float = 0.50, step_size: Optional[int] = None):
        # Verifica se o índice é um DatetimeIndex
        if not isinstance(df.index, DatetimeIndex):
            raise ValueError("O índice do DataFrame deve ser do tipo `DatetimeIndex`.")

        self.df = df.copy()

        # Atribui as datas de início e fim com base nos parâmetros ou no índice do DataFrame
        self.start = self._parse_date(start, df.index.min())
        self.end = self._parse_date(end, df.index.max())

        # Aplica o deslocamento de dias, se necessário
        if step_size is not None:
            self._apply_step_size(step_size)

        # Verifica se as datas de 'start' e 'end' estão dentro do índice do DataFrame
        self._validate_dates()

        # Seleciona o intervalo de dados dentro do DataFrame entre 'start' e 'end'
        self.data_range = self.df.loc[self.start : self.end]

        # Calcula o índice para dividir os dados entre treino e teste
        self.split_index = round(len(self.data_range) * p)

    def _parse_date(self, date_str: Optional[str], default_date) -> datetime:
        """
        Converte uma string de data para um objeto `datetime`. 
        Se a data não for fornecida, retorna a data padrão.

        Args:
            date_str (str, opcional): Data no formato 'YYYY-MM-DD'.
            default_date (datetime): Data padrão a ser usada se `date_str` for None.

        Returns:
            datetime: Data convertida.
        """
        if date_str:
            return datetime.strptime(date_str, '%Y-%m-%d')
        return default_date

    def _apply_step_size(self, step_size: int):
        """
        Aplica um deslocamento de dias às datas `start` e `end`.

        Args:
            step_size (int): Número de dias a ser adicionado às datas `start` e `end`.
        """
        if step_size <= 0:
            raise ValueError("O valor de `step_size` deve ser positivo.")

        self.start += timedelta(days=step_size)
        self.end += timedelta(days=step_size)

    def _validate_dates(self):
        """
        Valida se as datas `start` e `end` estão presentes no índice do DataFrame.
        
        Lança um erro se alguma das datas não estiver no índice.
        """
        if Timestamp(self.start) not in self.df.index or Timestamp(self.end) not in self.df.index:
            raise ValueError(f"As datas `start` ({self.start}) e/ou `end` ({self.end}) não estão presentes no índice do DataFrame.")

    def train(self) -> DataFrame:
        """
        Retorna o conjunto de dados de treino com base no índice de divisão.

        Returns:
            pd.DataFrame: Dados de treino.
        """
        return self.data_range.iloc[:self.split_index].dropna() # <-!

    def test(self) -> DataFrame:
        """
        Retorna o conjunto de dados de teste, com base no índice de divisão.

        Returns:
            pd.DataFrame: Dados de teste.
        """
        return self.data_range.iloc[self.split_index:].dropna() # <-!

    def after_test(self) -> DataFrame:
        """
        Retorna os dados após o período de teste, a partir da data `end`.

        Returns:
            pd.DataFrame: Dados pós-teste.
        """
        return self.df.loc[self.end:].iloc[1:].dropna() # <-!
