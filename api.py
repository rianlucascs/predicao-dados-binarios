
import requests
from typing import Union, List
from pandas import concat


class GitHubClass:

    def __init__(self, file: str, dep_git : bool = False):
        response = requests.get(f'https://raw.githubusercontent.com/rianlucascs/predicao-dados-binarios/master/Scripts/{file}.py')
        exec(response.text, globals())
        github_class = file.lower().title().replace('_', '')
        self.object = globals().get(github_class)

        # Depuração para verificar se a classe foi carregada corretamente
        if dep_git:
            if self.object is None:
                print(f"Erro: A classe '{github_class}' não foi encontrada.")
                raise ValueError(f"A classe '{file}' não foi encontrada no código.")
            else:
                print(f"Classe '{github_class}' carregada com sucesso.")


class MarketBehaviorForecaster:
    
    def __init__(self, ticker : str, p : str=1, type_alvo : str='A_BINARIO', features : Union[int, List[int]] = [],
                 start : str = 'YYYY-MM-DD', end : str = 'YYYY-MM-DD', step_size : Union[int, None] = None, 
                 ml_model : str = 'train_decision_tree', dep_git : bool = False, contratos : int = 100):
        self.ticker = ticker
        self.p = p
        self.type_alvo = type_alvo
        self.features = features
        self.start = start
        self.end = end
        self.step_size = step_size
        self.ml_model = ml_model
        self.dep_git = dep_git
        self.contratos = contratos

    def generate(self):

        df = GitHubClass('prices').object.get(self.ticker)
        df = getattr(GitHubClass('alvos').object(df, p=self.p), self.type_alvo)
        df = GitHubClass('features').object(df).get(self.features)
        sd = GitHubClass('split_data').object(df, self.start, self.end, step_size=self.step_size)
        train = sd.train()
        test = sd.test()
        after_test = sd.after_test()

        ml = GitHubClass('machines').object(train, test, after_test, self.features)
        model = getattr(ml, self.ml_model)()
        train = ml.predict_train(model)
        test = ml.predict_test(model)
        after_test = ml.predict_after_test(model)

        rp = GitHubClass('result_predict').object(train, test, after_test, lotes=self.contratos)
        train = rp.calcula_train_day()
        test = rp.calcula_test_day()
        after_test = rp.calcula_after_test_day()

        df = concat([train, test, after_test], axis=0)
        df['resultado_predicao_acumulado'] = df['resultado_predicao'].cumsum()
        print(df)

        GitHubClass('graphs').object(df, 'resultado_predicao_acumulado', (10, 5), 1, ylabel='Patrimônio Acumulado (Reais)', title='Train, Test and After Test', seta=True).linha()


MarketBehaviorForecaster('BBDC4.SA', features=[1, 2], start='2012-05-11', end='2022-05-11', step_size=None).generate()

