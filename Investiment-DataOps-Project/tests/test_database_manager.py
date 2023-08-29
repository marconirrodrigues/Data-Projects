import sqlite3
import pytest
from src.database_manager import DatabaseManagerForTest

@pytest.fixture
def db_manager():
    conn = sqlite3.connect(':memory:')  # Criar um banco de dados SQLite na memória
    db_manager = DatabaseManagerForTest(conn)
    yield db_manager  # yield funciona como return, mas garante que o código após seja executado ao final
    conn.close()

def test_insert_data(db_manager):
    create_table_query = """CREATE TABLE IF NOT EXISTS stocks
                            (date text, trans text, symbol text,
                             qty real, price real)"""
    db_manager.create_table(create_table_query)
    data = ('2023-10-05', 'BUY', 'RHAT', 100, 35.14)
    insert_query = """INSERT INTO stocks VALUES (?, ?, ?, ?, ?)"""
    db_manager.insert_data(insert_query, data)
    db_manager.cursor.execute('SELECT * FROM stocks')
    assert db_manager.cursor.fetchone() == data
