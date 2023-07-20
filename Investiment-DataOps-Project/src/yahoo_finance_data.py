import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

dbname = os.environ.get('DB_NAME') # obtém o nome do banco de dados do ambiente
user = os.environ.get('DB_USER') # obtém o usuário do banco de dados do ambiente
password = os.environ.get('DB_PASSWORD') # obtém a senha do banco de dados do ambiente

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


