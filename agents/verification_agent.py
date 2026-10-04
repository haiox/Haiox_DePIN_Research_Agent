import json

from agents.state import AgentState
from core.repositories import get_evidence_by_id
from core.llm_router import call_llm


def validate_verification(data: object, evidence: str) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get("verification_summary"), str):
        raise ValueError("Verification response has no summary")
    evaluations = data.get("claim_evaluations")
    if not isinstance(evaluations, list) or not evaluations:
        raise ValueError("Verification response has no claim evaluations")
    allowed = {"supported", "partially_supported", "unsupported"}
    for item in evaluations:
        if not isinstance(item, dict) or not isinstance(item.get("claim"), str) or not item["claim"].strip():
            raise ValueError("Invalid claim evaluation")
        if item.get("status") not in allowed:
            raise ValueError("Invalid claim status")
        score = item.get("confidence_score")
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 1:
            raise ValueError("Invalid confidence score")
        quote = item.get("source_quote")
        if item["status"] in {"supported", "partially_supported"}:
            if not isinstance(quote, str) or not quote.strip() or quote not in evidence:
                raise ValueError("Supporting quote is absent from stored evidence")
        elif quote and (not isinstance(quote, str) or quote not in evidence):
            raise ValueError("Source quote is absent from stored evidence")
    return data


async def verification_node(state: AgentState):
    ev_id = state.get("evidence_id")
    findings = state.get("structured_findings") or {}
    if not ev_id or not findings.get("tokenomics") or not findings.get("risk"):
        return {"errors": state.get("errors", []) + ["Missing evidence or analysis for verification."], "current_step": "failed"}

    evidence_record = get_evidence_by_id(ev_id)
    if not evidence_record or not evidence_record.get("content"):
        return {"errors": state.get("errors", []) + ["Evidence record not found or empty."], "current_step": "failed"}

    evidence = evidence_record["content"][:4000]
    risk = findings["risk"].get("risk_assessment", findings["risk"])
    if not isinstance(risk, dict):
        return {"errors": state.get("errors", []) + ["Invalid risk findings."], "current_step": "failed"}
    claims_summary = {
        "tokenomics_summary": findings["tokenomics"],
        "key_risks": risk.get("technical_risks", [])[:2] + risk.get("red_flags", [])[:2],
    }
    prompt = f"""Check up to three claims against the evidence below. Return only a JSON object with
verification_summary and a nonempty claim_evaluations list. Each evaluation must contain
claim, status (supported, partially_supported, or unsupported), confidence_score (0 to 1),
and source_quote. For supported claims, source_quote must be an exact substring of the evidence.
If evidence is insufficient, use unsupported and an empty source_quote. Never invent quotes.

Claims: {json.dumps(claims_summary, ensure_ascii=False)}
Evidence: {evidence}
"""
    try:
        response = await call_llm(prompt)
        data = validate_verification(json.loads(response), evidence)
    except Exception as exc:
        return {"errors": state.get("errors", []) + [f"Verification failed: {exc}"], "current_step": "failed"}

    return {"verification_result": data, "current_step": "verification_done"}
