import requests
import os
import queries
from hashing import calculate_hash
from database_manager import DatabaseManager
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

newsapi_key = os.environ.get('NEWSAPI_KEY')  # Obtém a chave da API do NewsAPI do ambiente
dbname = os.environ.get('DB_NAME') # obtém o nome do banco de dados do ambiente
user = os.environ.get('DB_USER') # obtém o usuário do banco de dados do ambiente
password = os.environ.get('DB_PASSWORD') # obtém a senha do banco de dados do ambiente

class NewsAPI:
    """
    Classe para interagir com o NewsAPI.
    """
    def __init__(self, api_key):
        """
        Inicializa a instância do NewsAPI.

        Args:
            api_key (str): A chave da API para autenticar com o NewsAPI.
        """
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything?"

    def get_news(self, keyword, days):
        """
        Obtém notícias de um determinado período passado baseado em uma palavra-chave.

        Args:
            keyword (str): A palavra-chave para procurar nas notícias.
            days (int): O número de dias a partir de hoje para recuperar notícias.

        Returns:
            dict: Um dicionário com a resposta da API, ou None se a requisição falhou.
        """
        # Data de hoje
        to_date = datetime.now()

        # Data do período inicial
        from_date = to_date - timedelta(days=days)

        # Formata as datas para o formato apropriado para a API
        to_date_str = to_date.strftime("%Y-%m-%d")
        from_date_str = from_date.strftime("%Y-%m-%d")
        
        # Constrói a URL completa
        complete_url = self.base_url + "apiKey=" + self.api_key + "&q=" + keyword + "&from=" + from_date_str + "&to=" + to_date_str + "&language=pt"

        # Envia a requisição e recebe a resposta
        response = requests.get(complete_url)

        # Checa o status da requisição
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
        

def main():
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
