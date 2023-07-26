import psycopg2

class DatabaseManager:
    def __init__(self, dbname, user, password, host="localhost"):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def create_table(self, create_table_query):
        self.cursor.execute(create_table_query)

    def insert_data(self, insert_query, data):
        self.cursor.execute(insert_query, data)

    def close(self):
        self.conn.close()

class DatabaseManagerForTest(DatabaseManager):
    def __init__(self, conn):
        self.conn = conn
        self.conn.isolation_level = None  # Para ativar o autocommit no SQLite
        self.cursor = self.conn.cursor()
