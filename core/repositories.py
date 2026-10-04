import json
import os
from contextlib import closing

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is required")
    return psycopg2.connect(database_url)


def save_evidence(project_id: int | None, source_url: str, raw_content: str) -> int | None:
    """Store page text and associate it with an existing or newly created project."""
    try:
        with closing(get_connection()) as conn, conn:
            with conn.cursor() as cursor:
                if project_id is None:
                    cursor.execute(
                        "SELECT id FROM projects WHERE website_url = %s ORDER BY id LIMIT 1",
                        (source_url,),
                    )
                    row = cursor.fetchone()
                    if row:
                        project_id = row[0]
                    else:
                        cursor.execute(
                            "INSERT INTO projects (project_name, website_url) VALUES (%s, %s) RETURNING id",
                            (source_url, source_url),
                        )
                        project_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO evidence (project_id, source_url, content) VALUES (%s, %s, %s) RETURNING id",
                    (project_id, source_url, raw_content),
                )
                return cursor.fetchone()[0]
    except Exception as exc:
        print(f"❌ [Repository] Failed to save evidence: {exc}")
        return None


def get_evidence_by_id(evidence_id: int) -> dict | None:
    try:
        with closing(get_connection()) as conn, conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, project_id, source_url, content FROM evidence WHERE id = %s",
                    (evidence_id,),
                )
                row = cursor.fetchone()
        if row:
            return dict(zip(("id", "project_id", "source_url", "content"), row))
        return None
    except Exception as exc:
        print(f"❌ [Repository] Error fetching evidence: {exc}")
        return None


def save_research_report(evidence_id: int, tokenomics: dict, risk: dict, verification: dict) -> int | None:
    try:
        with closing(get_connection()) as conn, conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO research_reports
                       (evidence_id, tokenomics, risk_analysis, verification_result)
                       VALUES (%s, %s, %s, %s) RETURNING id""",
                    (evidence_id, json.dumps(tokenomics), json.dumps(risk), json.dumps(verification)),
                )
                return cursor.fetchone()[0]
    except Exception as exc:
        print(f"❌ [Repository] Error saving research report: {exc}")
        return None
