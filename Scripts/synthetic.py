
import requests
import pandas as pd
from pandas import to_datetime

class Synthetic:

    def monte_carlo(ticker):
        url = 'https://raw.githubusercontent.com/rianlucascs/simulacao-de-monte-carlo/master/Scripts/monte_carlo.py'
        response = requests.get(url)
        exec(response.text, globals())
        monaco = MonteCarlo(ticker, 'max')
        result = monaco.simulacao(n_simulacao=1, custo_operacional=0)
        result.index = to_datetime(result.index)
        return monaco.loc_sim(result, 0)


# print(Synthetic.monte_carlo('VALE3.SA', '5y', 1, 0))

