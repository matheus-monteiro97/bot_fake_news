import sqlite3


DATABASE = "data/analysis_history.db"


def init_db():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            tipo TEXT,

            score INTEGER,

            categoria TEXT,

            texto TEXT
        )
        """
    )

    conn.commit()

    conn.close()


def save_analysis(
        tipo,
        score,
        categoria,
        texto):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analyses
        (
            tipo,
            score,
            categoria,
            texto
        )

        VALUES (?, ?, ?, ?)
        """,

        (
            tipo,
            score,
            categoria,
            texto
        )
    )

    conn.commit()

    conn.close()

import pandas as pd

def get_all_analyses():

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql_query(

        """
        SELECT *
        FROM analyses
        ORDER BY data DESC
        """,

        conn
    )

    conn.close()

    return df

def get_category_count():

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql_query(

        """
        SELECT
            categoria,
            COUNT(*) quantidade
        FROM analyses
        GROUP BY categoria
        """,

        conn
    )

    conn.close()

    return df

def get_average_score():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT AVG(score)
        FROM analyses
        """

    )

    avg_score = cursor.fetchone()[0]

    conn.close()

    return round(avg_score or 0, 2)