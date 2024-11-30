
import requests
from typing import Union, List
from pandas import concat
import os
from requests.exceptions import RequestException

class GitHubScriptLoader:
    """
    Classe para carregar e executar scripts Python do GitHub.

    Esta classe permite fazer o download de scripts Python armazenados em um repositório público do GitHub,
    e carregar as classes definidas nesses scripts. Também fornece funcionalidades para salvar esses scripts localmente.

    Attributes:
        BASE_URL (str): URL base do repositório GitHub onde os scripts estão hospedados.
        FILES (list): Lista de scripts a serem baixados e carregados.
        script_name (str): Nome do script a ser carregado.
        enable_debug (bool): Habilita ou desabilita mensagens de depuração.
        object (object): Instância da classe carregada a partir do script Python.

    Methods:
        ``_response(script_name: str) -> requests.Response``:
            Realiza uma requisição HTTP para obter o conteúdo de um script Python.

        ``_download_and_save_class()``:
            Baixa os scripts Python listados em `FILES` e os salva localmente.

        ``_download_and_load_class() -> object``:
            Faz o download do script e instância a classe correspondente.
    """
    BASE_URL = 'https://raw.githubusercontent.com/rianlucascs/predicao-dados-binarios/master/Scripts/'

    FILES = ['alvos', 'features', 'graphs', 'machines', 'prices', 'result_predict', 'split_data'] 

    def __init__(self, script_name: Union[str, None] = None, enable_debug: bool = False,
                 import_local: bool = False, path: str = ''):
        """
        Inicializa a classe GitHubScriptLoader.

        Este método configura as opções para carregar os scripts e faz a inicialização dependendo
        da escolha de carregar scripts locais ou baixar do GitHub.

        :param script_name: Nome do script a ser carregado do GitHub. Se `import_local` for True, 
                             esse parâmetro é ignorado.
        :param enable_debug: Se True, habilita a depuração com prints detalhados.
        :param import_local: Se True, tenta carregar scripts locais em vez de baixar do GitHub.
        :param path: Caminho onde os scripts locais devem ser salvos. Necessário se `import_local` for True.
        """
        self.script_name = script_name
        self.enable_debug = enable_debug
        self.path = path
        self.object = self._download_and_load_class() if not import_local else self._download_and_save_class()
    
    def _response(self, script_name: str) -> requests.Response:
        """
        Realiza uma requisição HTTP para obter o conteúdo de um script Python a partir de um repositório GitHub.

        Este método constrói a URL do script a ser baixado e faz uma requisição HTTP GET. Caso a resposta tenha
        um status diferente de 200 (OK), uma exceção será levantada. O método também trata exceções de rede e
        fornece mensagens de erro mais detalhadas.

        :param script_name: Nome do script Python a ser baixado, sem a extensão '.py'.
        :return: Resposta HTTP com o conteúdo do script.
        :raises FileNotFoundError: Se o script não for encontrado no repositório (status 404).
        :raises RequestException: Para qualquer outro erro relacionado à requisição HTTP (e.g., erros de rede).
        :raises ValueError: Se o nome do script fornecido for inválido ou não tiver o formato esperado.
        """
        if not script_name or not isinstance(script_name, str):
            raise ValueError("O nome do script deve ser uma string não vazia.")

        url = f"{self.BASE_URL}{script_name}.py"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Levanta exceção para status 4xx/5xx
        except RequestException as e:
            # Captura erros relacionados à requisição HTTP (e.g., problemas de rede, timeout)
            raise RequestException(f"Erro ao acessar o arquivo '{script_name}.py' no repositório: {str(e)}")
        
        if response.status_code != 200:
            raise FileNotFoundError(f"O script '{script_name}.py' não foi encontrado no repositório: {url}")
        
        return response

    def _download_and_save_class(self):
        """
        Baixa os scripts Python listados em `FILES` a partir do repositório GitHub e os salva no diretório local
        especificado em `self.path`. Após o download, importa os módulos Python salvos localmente, permitindo
        seu uso na execução do código.

        Este método verifica se o diretório local existe, criando-o caso necessário. Em seguida, para cada script
        listado, o método tenta baixar o arquivo correspondente, salvá-lo no diretório indicado e, caso o arquivo
        não exista localmente, escreve seu conteúdo.

        Após o salvamento, os módulos Python são importados dinamicamente para o projeto.

        :raises FileNotFoundError: Se algum dos scripts listados não puder ser baixado do GitHub (erro 404 ou outro erro de rede).
        :raises OSError: Se ocorrer um erro ao tentar salvar o arquivo no diretório local.
        :raises ImportError: Se ocorrer um erro ao tentar importar os módulos localmente após o download.
        """
        # Cria o diretório se ele não existir
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except OSError as e:
                raise OSError(f"Erro ao tentar cirar o diretório '{self.path}': {e}")

        # Cria o diretório se ele não existir
        for file in self.FILES:
            try:
                response = self._response(file)
                path_file = os.path.join(self.path, f'{file}.py')

                if not os.path.exists(path_file):
                    with open(path_file, 'x', encoding='utf-8') as f:
                        f.write(response.text)
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Erro ao tentar baixar o script '{file}' do GitHub: {e}")
            except OSError as e:
                raise OSError(f"Erro ao salvar o script '{file}' no caminho '{self.path}': {e}")


    def _download_and_load_class(self) -> object:
        """
        Faz o download de um script Python, executa-o dinamicamente e instancia a classe correspondente.

        O código do script é executado no escopo global e a classe definida no script é carregada dinamicamente.

        :return: Instância da classe carregada do script Python.
        :rtype: object
        :raises FileNotFoundError: Se o script não for encontrado no repositório.
        :raises ValueError: Se a classe esperada não for encontrada no script.
        :raises RuntimeError: Se ocorrer um erro ao executar o script ou ao instanciar a classe.
        """
        try:
            # Obter o conteúdo do script
            response = self._response(self.script_name)
            
            # Construir o nome da classe com base no nome do script
            class_name = self.script_name.title().replace('_', '')
            
            # Executa o código do script no escopo local
            exec(response.text, globals())
            
            # Tenta obter a classe carregada
            loaded_class = globals().get(class_name)
            
            if not loaded_class:
                raise ValueError(f"Classe '{class_name}' não encontrada no script '{self.script_name}'.")
            
            if self.enable_debug:
                print(f"Classe '{class_name}' carregada com sucesso.")
            
            return loaded_class

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Script '{self.script_name}' não encontrado no repositório: {e}")
        
        except ValueError as e:
            raise ValueError(f"Erro ao carregar a classe '{class_name}' do script '{self.script_name}': {e}")
        
        except Exception as e:
            raise RuntimeError(f"Erro inesperado ao carregar a classe '{class_name}' do script '{self.script_name}': {e}")

class MarketForecastConfig:
    """
    Configurações para a previsão de comportamento de mercado.

    Esta classe define os parâmetros necessários para configurar o pipeline de previsão de mercado, 
    incluindo o ativo a ser analisado, período de análise, variáveis-alvo, características a serem 
    extraídas, janelas de dados, modelo de aprendizado de máquina, e outras opções adicionais.

    Parameters:
        ticker (str): Símbolo do ativo a ser analisado (e.g., '^BVSP'). Representa o identificador único do ativo.
        p (int): Período para a criação das variáveis-alvo. Default: 1.
        target_type (str): Tipo de variável-alvo a ser gerada. Valores comuns podem incluir 'A_BINARIO', 'A_CONTINUO', etc. 
            Default: 'A_BINARIO'.
        features (Union[int, List[int]]): Índices das características (features) a serem utilizadas no modelo. Pode ser 
            um único índice ou uma lista de índices.
        start (str): Data de início da análise no formato 'YYYY-MM-DD'. Define o início da janela de dados.
        end (str): Data de término da análise no formato 'YYYY-MM-DD'. Define o final da janela de dados.
        step_size (Union[int, None]): Tamanho do passo para janelas deslizantes. Se None, usa o tamanho padrão.
        ml_model (str): Nome do modelo de aprendizado de máquina a ser utilizado. Exemplos incluem 
            'train_decision_tree', 'train_random_forest', etc. Default: 'train_decision_tree'.
        enable_debug (bool): Indica se mensagens de depuração devem ser exibidas. Default: False.
        contracts (int): Quantidade de contratos financeiros utilizados para cálculos de resultados. Default: 100.
        import_local (bool): Se True, importa scripts de um diretório local definido em `path`. Default: False.
        path (str): Caminho para os scripts locais, usado apenas se `import_local` for True.
    """
    def __init__(self, ticker: str, p: int = 1, target_type: str = 'A_BINARIO',
                 features: Union[int, List[int]] = [], start: str = 'YYYY-MM-DD',
                 end: str = 'YYYY-MM-DD', step_size: Union[int, None] = None,
                 ml_model: str = 'train_decision_tree', enable_debug: bool = False,
                 contracts: int = 100, import_local: bool = False, path : str = ''):
        self.ticker = ticker
        self.p = p
        self.target_type = target_type
        self.features = features
        self.start = start
        self.end = end
        self.step_size = step_size
        self.ml_model = ml_model
        self.enable_debug = enable_debug
        self.contracts = contracts
        self.import_local = import_local
        self.path = path

class MarketBehaviorForecaster(MarketForecastConfig):
    """
    Classe para realizar a previsão do comportamento de mercado.

    Esta classe herda as configurações definidas em `MarketForecastConfig` e implementa as etapas
    necessárias para realizar previsões de mercado, como carregamento de dados, criação de alvos,
    engenharia de atributos e treinamento de modelos de aprendizado de máquina.

    Methods:
        ``run_forecast()``:
            Executa o pipeline completo de previsão, desde o carregamento de dados até a consolidação dos resultados.
    """
    def run_forecast(self):
        """
        Executa o pipeline completo de previsão de mercado.

        Etapas:
        1. Carrega os dados históricos de preços a partir de um script externo.
        2. Cria variáveis-alvo utilizando diferentes estratégias definidas no script.
        3. Adiciona atributos ao conjunto de dados para enriquecer a análise.
        4. Divide os dados em conjuntos de treino, teste e pós-teste.
        5. Treina o modelo de aprendizado de máquina especificado.
        6. Gera previsões e consolida os resultados em um único DataFrame.

        :raises Exception: Caso ocorra algum erro durante o processo.
        """
        try:
            # Carregamento dos dados de preços
            df = GitHubScriptLoader('prices').object.get(self.ticker)

            # Criação dos alvos
            df = getattr(GitHubScriptLoader('alvos').object(df, p=self.p), self.target_type)

            # Adicionando features
            df = GitHubScriptLoader('features').object(df).get(self.features)

            # Divisão dos dados
            sd = GitHubScriptLoader('split_data').object(df, self.start, self.end, step_size=self.step_size)
            train = sd.train()
            test = sd.test()
            after_test = sd.after_test()

            # Treinamento do modelo
            ml = GitHubScriptLoader('machines').object(train, test, after_test, self.features)
            model = getattr(ml, self.ml_model)()
            train = ml.predict_train(model)
            test = ml.predict_test(model)
            after_test = ml.predict_after_test(model)

            # Resultados
            rp = GitHubScriptLoader('result_predict').object(train, test, after_test, lotes=self.contracts)
            train = rp.calcula_train_day()
            test = rp.calcula_test_day()
            after_test = rp.calcula_after_test_day()

            # Consolidação dos resultados
            df = concat([train, test, after_test], axis=0)
            df['resultado_predicao_acumulado'] = df['resultado_predicao'].cumsum()
            
            
            return {
                "metrics": {
                    "model": ml.evaluate(),
                    "returns": rp.evaluate()
                },
                "df": {
                    "train": train,
                    "test": test,
                    "after_test": after_test,
                    "df": df
                }
                
            }

        except Exception as e:
            print(f"Erro na execução: {e}")
            raise

# mb = MarketBehaviorForecaster('^BVSP', features=[1, 2], start='2012-05-11', end='2022-05-11', step_size=None).run_forecast()


class MarketBehaviorForecasterLocal(MarketForecastConfig):
    """
    Classe para previsão de comportamento de mercado utilizando scripts locais.

    Esta classe herda de `MarketForecastConfig` e executa um pipeline de previsão
    de mercado utilizando scripts Python armazenados localmente. É útil em cenários
    onde os scripts já foram baixados previamente e estão disponíveis no sistema de arquivos.

    Methods:
        ``run_forecast_local()``:
            Executa o pipeline completo de previsão utilizando scripts locais.
    """
    def run_forecast_local(self):
        """
        Executa o pipeline de previsão de mercado utilizando scripts locais.

        Este método realiza as seguintes etapas:
        1. Carrega os scripts locais (se ainda não estiverem carregados).
        2. Realiza o carregamento dos dados históricos de preços.
        3. Cria variáveis-alvo para modelagem.
        4. Adiciona atributos (features) ao conjunto de dados.
        5. Divide os dados em conjuntos de treino, teste e pós-teste.
        6. Treina o modelo especificado e gera previsões.
        7. Consolida os resultados e calcula o patrimônio acumulado.

        :raises ImportError: Se houver falha ao importar os módulos locais.
        :raises Exception: Para outros erros durante o pipeline de previsão.
        """
        try:
            # Baixar e salvar scripts locais, se necessário
            GitHubScriptLoader(
                script_name=None, 
                import_local=True, 
                path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MarketForecast')
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao preparar os scripts locais: {e}")
        
        # Importa os módulos salvos localmente após o download
        try:
            global alvos, features, graphs, machines, prices, result_predict, split_data
            from MarketForecast import (
                alvos, features, graphs, machines, prices, result_predict, split_data
            )
        except ImportError as e:
            raise ImportError(f"Erro ao importar os módulos locais após o download: {e}")
        
        try:
            # Carregamento dos dados de preços
            df = prices.Prices.get(self.ticker)
            
            # Criação dos alvos
            df = getattr(alvos.Alvos(df, p=self.p), self.target_type)

            # Adicionando features
            df = features.Features(df).get(self.features)

            # Divisão dos dados
            sd = split_data.SplitData(df, self.start, self.end, step_size=self.step_size)
            train = sd.train()
            test = sd.test()
            after_test = sd.after_test()

            # Treinamento do modelo
            ml = machines.Machines(train, test, after_test, self.features)
            model = getattr(ml, self.ml_model)()
            train = ml.predict_train(model)
            test = ml.predict_test(model)
            after_test = ml.predict_after_test(model)

            # Resultados
            rp = result_predict.ResultPredict(train, test, after_test, lotes=self.contracts)
            train = rp.calcula_train_day()
            test = rp.calcula_test_day()
            after_test = rp.calcula_after_test_day()

            # Consolidação dos resultados
            df = concat([train, test, after_test], axis=0)
            df['resultado_predicao_acumulado'] = df['resultado_predicao'].cumsum()
            
            return {
                "metrics": {
                    "model": ml.evaluate(),
                    "returns": rp.evaluate()
                },
                "df": {
                    "train": train,
                    "test": test,
                    "after_test": after_test,
                    "df": df
                }
                
            }

        
        except Exception as e:
            print(f"Erro na execução: {e}")
            raise  

# mb = MarketBehaviorForecasterLocal('^BVSP', features=[1, 2], start='2012-05-11', end='2022-05-11', step_size=None).run_forecast_local()
# print(mb)