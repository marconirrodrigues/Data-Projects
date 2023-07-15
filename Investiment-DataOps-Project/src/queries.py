# queries.py

# queries newsapi
create_table_newsapi = """
CREATE TABLE IF NOT EXISTS sor_newsapi (
    id_newsapi TEXT PRIMARY KEY,
    source_name TEXT,
    author TEXT,
    title TEXT,
    description TEXT,
    url TEXT,
    published_at TIMESTAMP
)
"""

insert_into_table_newsapi = """
INSERT INTO sor_newsapi (id_newsapi, source_name, author, title, description, url, published_at)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

select_record_by_id_newsapi = """
SELECT 1 FROM sor_newsapi WHERE id_newsapi = %s;
"""

def record_exists_news(cursor, id_newsapi):
    cursor.execute(select_record_by_id_newsapi, (id_newsapi,))
    return bool(cursor.fetchone())


# queries yahoo_finance
create_table_yahoo_finance = """
CREATE TABLE IF NOT EXISTS sor_yahoo_finance (
    id_yahoo_finance TEXT PRIMARY KEY,
    Datetime TIMESTAMP,
    Open NUMERIC(15,6),
    High NUMERIC(15,6),
    Low NUMERIC(15,6),
    Close NUMERIC(15,6),
    Adj_Close NUMERIC(15,6),
    Volume NUMERIC(15)
)
"""

insert_into_yahoo_finance = """
INSERT INTO sor_yahoo_finance (id_yahoo_finance, Datetime, Open, High, Low, Close, Adj_Close, Volume)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

select_record_by_id_yahoo_finance = """
SELECT 1 FROM sor_yahoo_finance WHERE id_yahoo_finance = %s;
"""

def record_exists_yahoo_finance(cursor, id_yahoo_finance):
    cursor.execute(select_record_by_id_yahoo_finance, (id_yahoo_finance,))
    return bool(cursor.fetchone())