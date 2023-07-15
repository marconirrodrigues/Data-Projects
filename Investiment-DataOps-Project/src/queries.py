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

select_record_by_id = """
SELECT 1 FROM sor_newsapi WHERE id_newsapi = %s;
"""

def record_exists(cursor, id_newsapi):
    cursor.execute(select_record_by_id, (id_newsapi,))
    return bool(cursor.fetchone())


'''# queries yahoo_finance
create_table_yahoo_finance = """
CREATE TABLE sor_yahoo_finance (
    id SERIAL PRIMARY KEY,


)'''