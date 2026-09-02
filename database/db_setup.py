import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    print("⏳ Connecting to PostgreSQL database...")
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Enable pgvector extension for AI embeddings
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        # Create table for DePIN projects
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                project_name VARCHAR(255) NOT NULL,
                website_url VARCHAR(255),
                description TEXT,
                risk_score INTEGER,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # New table for the Evidence Layer
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                source_url VARCHAR(255),
                content TEXT NOT NULL,
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create table for whitepaper claims and vector embeddings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS whitepaper_claims (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                claim_text TEXT NOT NULL,
                source_document VARCHAR(255),
                confidence_score FLOAT,
                embedding vector(1536),
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Connection successful! Tables 'projects', 'evidence', and 'whitepaper_claims' are ready.")

    except Exception as e:
        print(f"❌ Database connection or setup failed: {e}")

if __name__ == "__main__":
    init_db()
