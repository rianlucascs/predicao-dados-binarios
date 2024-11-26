import pandas as pd


class ResultPredict:
    """
    Classe para calcular e avaliar o impacto das previsões de lotes sobre os retornos financeiros.
    
    Attributes:
        train (pd.DataFrame): Dados de treino.
        test (pd.DataFrame): Dados de teste.
        after_test (pd.DataFrame): Dados após o teste.
        lotes (int, optional): Quantidade de lotes para calcular o impacto. Padrão é 1.
    """

    def __init__(self, train: pd.DataFrame, test: pd.DataFrame, after_test: pd.DataFrame, lotes: int = 1):
        """
        Inicializa a classe com dados de treino, teste, e pós-teste, além do número de lotes.

        Args:
            train (pd.DataFrame): Dados históricos de treino.
            test (pd.DataFrame): Dados de teste para avaliação.
            after_test (pd.DataFrame): Dados após a fase de teste.
            lotes (int, optional): Número de lotes a ser utilizado no cálculo do impacto. Padrão é 1.
        """
        self.train = train
        self.test = test
        self.after_test = after_test
        self.lotes = lotes
        
        # Validar se os DataFrames possuem índice de data
        self._verificar_indice_datetime()

    def _verificar_indice_datetime(self):
        """
        Verifica se o índice dos DataFrames é do tipo DatetimeIndex e converte, se necessário.
        """
        for dataset in [self.train, self.test, self.after_test]:
            if not pd.api.types.is_datetime64_any_dtype(dataset.index):
                dataset.index = pd.to_datetime(dataset.index)

    def _calcular_impacto_previsao(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula o impacto das previsões baseadas na variação absoluta e no número de lotes.

        Args:
            df (pd.DataFrame): O DataFrame contendo os dados de previsão.

        Returns:
            pd.DataFrame: DataFrame com as colunas de impacto calculadas.
        """
        # Calcular o impacto da previsão (resultado de predicao)
        df['resultado_predicao'] = df['variacao_absoluta'].abs() * (
            2 * (df['predicao'] == df.filter(like='alvo').squeeze()) - 1
        )
        
        # Aplicar o fator de lotes se for diferente de zero
        if self.lotes != 0:
            df['resultado_predicao'] *= self.lotes
        
        # Calcular o acumulado
        df['resultado_predicao_acumulado'] = df['resultado_predicao'].cumsum()
        return df
    
    def calcula_train_day(self) -> pd.DataFrame:
        """
        Calcula os impactos de previsão para o conjunto de treino.

        Returns:
            pd.DataFrame: DataFrame de treino com os cálculos de impacto.
        """
        self.train = self._calcular_impacto_previsao(self.train)
        return self.train
    
    def calcula_test_day(self) -> pd.DataFrame:
        """
        Calcula os impactos de previsão para o conjunto de teste.

        Returns:
            pd.DataFrame: DataFrame de teste com os cálculos de impacto.
        """
        self.test = self._calcular_impacto_previsao(self.test)
        return self.test
    
    def calcula_after_test_day(self) -> pd.DataFrame:
        """
        Calcula os impactos de previsão para o conjunto de dados após o teste.

        Returns:
            pd.DataFrame: DataFrame após o teste com os cálculos de impacto.
        """
        self.after_test = self._calcular_impacto_previsao(self.after_test)
        return self.after_test

    def evaluate(self) -> dict:
        """
        Avalia os resultados para os conjuntos de treino, teste e pós-teste.

        Returns:
            dict: Dicionário contendo as métricas médias para cada conjunto de dados.
        """
        def calcular_metricas(df: pd.DataFrame) -> dict:
            """
            Função auxiliar para calcular as métricas médias de retorno.

            Args:
                df (pd.DataFrame): O DataFrame contendo os resultados de previsão.

            Returns:
                dict: Dicionário com as métricas calculadas.
            """
            return {
                "average_daily_returns": df['resultado_predicao'].mean(),
                "average_weekly_returns": df['resultado_predicao'].resample('W').mean().mean(),
                "average_monthly_returns": df['resultado_predicao'].resample('M').mean().mean(),
                "average_quarterly_return": df['resultado_predicao'].resample('Q').mean().mean()
            }
        
        return {
            "train": calcular_metricas(self.train),
            "test": calcular_metricas(self.test),
            "after_test": calcular_metricas(self.after_test)
        }
