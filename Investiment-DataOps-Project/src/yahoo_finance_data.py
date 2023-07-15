import yfinance as yf

class FinanceDataFetcher:
    """
    Classe para recuperação de dados financeiros.
    """
    def __init__(self, ticker):
        """
        Inicializa uma instância da classe FinanceDataFetcher.

        Args:
            ticker (str): O ticker do ativo financeiro.
        """
        self.ticker = ticker

    def download_data(self, period='7d', interval='1h'):
        """
        Baixa os dados financeiros para o ticker especificado.

        Args:
            period (str, optional): O período dos dados. Default é '7d'.
            interval (str, optional): O intervalo dos dados. Default é '1h'.

        Returns:
            DataFrame: Um DataFrame do pandas com os dados financeiros.
        """
        data = yf.download(self.ticker, period=period, interval=interval)
        return data

if __name__ == "__main__":
    # Cria uma instância da classe FinanceDataFetcher para o ticker 'AAPL'.
    fetcher = FinanceDataFetcher('AAPL')
    # Baixa os dados financeiros e os imprime.
    data = fetcher.download_data()
    print(data)