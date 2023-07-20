import os
import queries
from database_manager import DatabaseManager
from hashing import calculate_hash
from news_data import NewsAPI
from yahoo_finance_data import FinanceDataFetcher
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

newsapi_key = os.environ.get('NEWSAPI_KEY')  # Obtém a chave da API do NewsAPI do ambiente
dbname = os.environ.get('DB_NAME') # obtém o nome do banco de dados do ambiente
user = os.environ.get('DB_USER') # obtém o usuário do banco de dados do ambiente
password = os.environ.get('DB_PASSWORD') # obtém a senha do banco de dados do ambiente

def main_news():

 # cria uma instância do NewsAPI
    newsapi = NewsAPI(newsapi_key)
    db = DatabaseManager(dbname, user, password)  # substitua por suas credenciais de banco de dados

    keyword = 'Apple'  # define a palavra-chave para a busca
    data = newsapi.get_news(keyword, 7)  # busca notícias dos últimos 7 dias com a palavra-chave

    print("\nVerificando a tabela 'sor_newsapi'\n")

    db.create_table(queries.create_table_newsapi)

    # insere os dados recuperados no banco de dados
    if data:
        articles = data['articles']
        for article in articles:
            source = article["source"].get("name")  # Obtém "source_name"
            author = article['author']
            title = article['title']
            description = article['description']
            url = article['url']
            published_at = article['publishedAt']

            # Calcula o hash das colunas
            id_newsapi = calculate_hash(source, title, author, published_at)

            # Verifica se o registro já existe antes de inserir
            if not queries.record_exists_news(db.cursor, id_newsapi):
                data_base = (source, author, title, description, url, published_at)
                db.insert_data(queries.insert_into_table_newsapi, (id_newsapi,) + data_base)
                print(f"{id_newsapi} adicionados com sucesso!")
            else:
                print("Dados já existentes na tabela.")
    else:
        print("Erro ao buscar notícias")

    db.close()

def main_yahoo_finance():
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

if __name__ == "__main__":
    main_news()
    main_yahoo_finance()