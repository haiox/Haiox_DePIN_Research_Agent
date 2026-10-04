import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def init_db():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is required")
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    project_name VARCHAR(255) NOT NULL,
                    website_url TEXT,
                    description TEXT,
                    risk_score INTEGER,
                    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evidence (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id),
                    source_url TEXT,
                    content TEXT NOT NULL,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS research_reports (
                    id SERIAL PRIMARY KEY,
                    evidence_id INTEGER NOT NULL REFERENCES evidence(id),
                    tokenomics JSONB NOT NULL,
                    risk_analysis JSONB NOT NULL,
                    verification_result JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    print("✅ Core database tables are ready.")


if __name__ == "__main__":
    init_db()
