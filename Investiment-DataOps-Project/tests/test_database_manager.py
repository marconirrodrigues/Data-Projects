import unittest
import sqlite3
from src.database_manager import DatabaseManager

# Classe para extensão do comportamento no teste
class DatabaseManagerForTest(DatabaseManager):
    def __init__(self, conn):
        self.conn = conn
        self.conn.isolation_level = None  # Para ativar o autocommit no SQLite
        self.cursor = self.conn.cursor()

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')  # Criar um banco de dados SQLite na memória
        self.db_manager = DatabaseManagerForTest(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_insert_data(self):
        create_table_query = """CREATE TABLE IF NOT EXISTS stocks
                                (date text, trans text, symbol text,
                                 qty real, price real)"""
        self.db_manager.create_table(create_table_query)
        data = ('2023-10-05', 'BUY', 'RHAT', 100, 35.14)
        insert_query = """INSERT INTO stocks VALUES (?, ?, ?, ?, ?)"""
        self.db_manager.insert_data(insert_query, data)
        self.db_manager.cursor.execute('SELECT * FROM stocks')
        self.assertEqual(self.db_manager.cursor.fetchone(), data)

if __name__ == '__main__':
    unittest.main()
