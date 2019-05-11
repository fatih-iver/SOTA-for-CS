import sqlite3

conn = sqlite3.connect('sota.db')
print("The database is opened successfully");

conn.execute("""
            CREATE TABLE IF NOT EXISTS authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            author_name TEXT NOT NULL,
            author_surname TEXT NOT NULL,
            UNIQUE(author_name, author_surname) );
            """)

conn.execute("""
            CREATE TABLE IF NOT EXISTS topics (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_name TEXT UNIQUE,
            sota_result INTEGER UNIQUE );
            """)

conn.execute("""
            CREATE TABLE IF NOT EXISTS papers (
            paper_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            abstract TEXT,
            result INTEGER );
            """)

conn.execute("""
            CREATE TABLE IF NOT EXISTS paper_authors (
            paper_id INTEGER,
            author_id INTEGER,
            PRIMARY KEY (paper_id, author_id),
            FOREIGN KEY (paper_id) REFERENCES papers (paper_id)
            ON DELETE CASCADE ON UPDATE NO ACTION,
            FOREIGN KEY (author_id) REFERENCES authors (author_id) 
            ON DELETE CASCADE ON UPDATE NO ACTION );
            """)

conn.execute("""
            CREATE TABLE IF NOT EXISTS paper_topics (
            paper_id INTEGER,
            topic_id INTEGER,
            PRIMARY KEY (paper_id, topic_id),
            FOREIGN KEY (paper_id) REFERENCES papers (paper_id)
            ON DELETE CASCADE ON UPDATE NO ACTION,
            FOREIGN KEY (topic_id) REFERENCES topics (topic_id) 
            ON DELETE CASCADE ON UPDATE NO ACTION );
            """)

print("Tables are created successfully");

conn.close()