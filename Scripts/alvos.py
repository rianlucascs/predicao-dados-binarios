


class Alvos:

    def __init__(self, df_price):
        self.df_price = df_price

        self.alvo_numerico = df_price['Close'] - df_price['Open']

    @property
    def BINARIO(self):
        pass
    
    @property
    def TERNARIO(self):
        pass

    @property
    def REGRA_1(self):
        pass

    @property
    def REGRA_2(self):
        pass