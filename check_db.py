import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def check_supabase():
    print("🔍 Fetching data straight from Supabase 'evidence' table...\n")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Fetch the latest 3 records
        cursor.execute("SELECT id, project_id, source_url, content, extracted_at FROM evidence ORDER BY id DESC LIMIT 3;")
        rows = cursor.fetchall()
        
        if not rows:
            print("📭 Table is empty! Nothing saved yet.")
        else:
            for row in rows:
                print(f"🔹 ID: {row[0]} | Project: {row[1]} | URL: {row[2]}")
                print(f"   🕒 Time: {row[4]}")
                print(f"   📄 Content Snippet: {row[3][:100]}...\n")
                
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_supabase()
