import unittest
from unittest.mock import patch
import pandas as pd
from src.yahoo_finance_data import FinanceDataFetcher

class TestFinanceDataFetcher(unittest.TestCase):
    @patch('yfinance.download')
    def test_download_data(self, mock_download):
        # Configura a resposta fictícia
        mock_df = pd.DataFrame({
            'Open': [1.0, 2.0],
            'High': [1.5, 2.5],
            'Low': [0.5, 1.5],
            'Close': [1.0, 2.0],
            'Volume': [1000, 2000],
        })
        mock_download.return_value = mock_df

        # Cria uma instância da classe FinanceDataFetcher
        data_fetcher = FinanceDataFetcher('AAPL')

        # Chama o método download_data e verifica a resposta
        df = data_fetcher.download_data('7d', '1h')

        # Verifica se o DataFrame tem as colunas corretas
        self.assertListEqual(list(df.columns), ['Open', 'High', 'Low', 'Close', 'Volume'])

        # Verifica se o DataFrame tem a quantidade correta de linhas
        self.assertEqual(len(df), 2)
        
if __name__ == '__main__':
    unittest.main()
