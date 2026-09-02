import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def save_evidence(project_id: int, source_url: str, raw_content: str) -> int:
    """
    Stores raw data in the evidence table and returns its ID.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        insert_query = """
            INSERT INTO evidence (project_id, source_url, content)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        # Temporarily set project_id to 1 to avoid foreign-key issues during testing
        cursor.execute(insert_query, (1, source_url, raw_content))
        evidence_id = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ [Repository] Evidence saved successfully! Evidence ID: {evidence_id}")
        return evidence_id
    except Exception as e:
        print(f"❌ [Repository] Failed to save evidence: {e}")
        return None

def get_evidence_by_id(evidence_id: int) -> dict:
    """
    Retrieves evidence by ID for the agents.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, project_id, source_url, content FROM evidence WHERE id = %s;", (evidence_id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "project_id": row[1],
                "source_url": row[2],
                "content": row[3]
            }
        return None
    except Exception as e:
        print(f"❌ [Repository] Error fetching evidence: {e}")
        return None
    import json

def save_research_report(evidence_id: int, tokenomics: dict, risk: dict, verification: dict) -> int:
    """
    Stores the final verified report in the research_reports table.
    """
    conn = get_connection()
    if not conn:
        print("❌ [Repository] Database connection failed.")
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO research_reports (evidence_id, tokenomics, risk_analysis, verification_result)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (
                evidence_id, 
                json.dumps(tokenomics), 
                json.dumps(risk), 
                json.dumps(verification)
            ))
            report_id = cur.fetchone()[0]
            conn.commit()
            print(f"💾 [Repository] Research Report saved successfully! Report ID: {report_id}")
            return report_id
    except Exception as e:
        print(f"❌ [Repository] Error saving research report: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()
