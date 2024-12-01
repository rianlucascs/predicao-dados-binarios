
import requests

class Synthetic:

    def monte_carlo(self, ticker, period, numero_simulacoes, loc_simulacao):
        url = 'https://raw.githubusercontent.com/rianlucascs/simulacao-de-monte-carlo/master/Scripts/monte_carlo.py'
        response = requests.get(url)
        exec(response.text)
        monaco = MonteCarlo(ticker, period)
        result = monaco.simulacao(numero_simulacao=numero_simulacoes, custo_operacional=0)
        return monaco.loc_sim(result, loc_simulacao)

