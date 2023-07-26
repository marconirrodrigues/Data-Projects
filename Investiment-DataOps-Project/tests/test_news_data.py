import unittest
import os
from unittest.mock import patch
from src.news_data import NewsAPI
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

newsapi_key = os.environ.get('NEWSAPI_KEY')  # Obtém a chave da API do NewsAPI do ambiente

class TestNewsAPI(unittest.TestCase):

    @patch('requests.get')
    def test_get_news(self, mock_get):
        # Configura a resposta fictícia da API
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "ok",
            "totalResults": 2,
            "articles": [
                # Adicione aqui as informações das notícias que quiser testar
            ]
        }

        # Cria uma instância da classe NewsAPI
        news_api = NewsAPI(newsapi_key)

        # Chama o método get_news e verifica a resposta
        response = news_api.get_news('bitcoin', 30)

        # Verifica se a resposta tem o status 'ok'
        self.assertEqual(response['status'], 'ok')

        # Verifica se a quantidade de resultados é a esperada
        self.assertEqual(response['totalResults'], 2)

        # Adicione mais assertivas de acordo com o que você quer testar


if __name__ == '__main__':
    unittest.main()
