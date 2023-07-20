import requests
from datetime import datetime, timedelta


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
