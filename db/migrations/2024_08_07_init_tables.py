import os

import psycopg2


conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    database=os.getenv("POSTGRES_DB_NAME", "vocabulary"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
)

cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );
    """
)

cursor.execute("CREATE TYPE card_status AS ENUM ('in_progress', 'learned');")
conn.commit()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS cards (
        id SERIAL PRIMARY KEY,
        telegram_id INTEGER,
        word TEXT NOT NULL,
        phase INTEGER NOT NULL DEFAULT 1,
        next_repetition_on DATE DEFAULT CURRENT_DATE,,
        status card_status NOT NULL DEFAULT 'in_progress',
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
    );
    """
)
conn.commit()
cursor.close()
conn.close()
