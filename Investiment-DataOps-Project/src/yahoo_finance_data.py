import yfinance as yf
import queries
import os
from database_manager import DatabaseManager
from hashing import calculate_hash
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
        
def main():
    # cria uma instância do NewsAPI
    db = DatabaseManager(dbname, user, password)  # substitua por suas credenciais de banco de dados
    # Cria uma instância da classe FinanceDataFetcher para o ticker 'AAPL'.
    fetcher = FinanceDataFetcher('AAPL')
    # Baixa os dados financeiros e os imprime.
    data = fetcher.download_data()
    
    print("\nVerificando a tabela 'sor_yahoo_finance'\n")

    db.create_table(queries.create_table_yahoo_finance)

    # insere os dados recuperados no banco de dados
    if not data.empty:
        print(f'')
        for datetime, row in data.iterrows():  # Observe a mudança aqui
            open = row['Open']
            high = row['High']
            low = row['Low']
            close = row['Close']
            adj_close = row['Adj Close']
            volume = row['Volume']

            # Calcula o hash das colunas
            id_yahoo_finance = calculate_hash(datetime, close, volume)

            # Verifica se o registro já existe antes de inserir
            if not queries.record_exists_yahoo_finance(db.cursor, id_yahoo_finance):
                data_base = (datetime, open, high, low, close, adj_close, volume)
                db.insert_data(queries.insert_into_yahoo_finance, (id_yahoo_finance,) + data_base)
                print(f"{id_yahoo_finance} adicionados com sucesso!")
            else:
                print("Dados já existentes na tabela.")
    else:
        print("Erro ao buscar notícias")

    db.close()


