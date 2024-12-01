import requests

# URL do script do GitHub
url = 'https://raw.githubusercontent.com/rianlucascs/simulacao-de-monte-carlo/master/Scripts/monte_carlo.py'

# Baixando o conteúdo do script
response = requests.get(url)

# Executando o conteúdo do script
exec(response.text)

# Agora a classe MonteCarlo está disponível, podemos instanciá-la
monaco = MonteCarlo('VALE3.SA', '1y')

# Chamar a simulação com 100 simulações e custo operacional de 0.001
result = monaco.simulacao(n_simulacao=100, custo_operacional=0.001)

# Exibir o resultado
print(result)