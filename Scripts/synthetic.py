
import requests
import pandas as pd
from pandas import to_datetime

class Synthetic:

    def monte_carlo(ticker):
        url = 'https://raw.githubusercontent.com/rianlucascs/simulacao-de-monte-carlo/master/Scripts/monte_carlo.py'
        response = requests.get(url)
        exec(response.text, globals())
        monaco = MonteCarlo(ticker, 'max')
        df = monaco.simulacao(n_simulacao=1, custo_operacional=0)
        df.index = to_datetime(df.index).normalize()
        monaco = monaco.loc_sim(df, 0)
        return monaco


# print(Synthetic.monte_carlo('VALE3.SA'))

