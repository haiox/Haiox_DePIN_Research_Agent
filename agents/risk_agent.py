import json
from agents.state import AgentState
from core.repositories import get_evidence_by_id
from core.llm_router import call_llm

async def risk_node(state: AgentState):
    print(f"⚠️ [Risk Agent] Analyzing Evidence ID: {state.get('evidence_id')}")
    
    ev_id = state.get("evidence_id")
    if not ev_id:
        return {"errors": state.get("errors", []) + ["No evidence_id found for risk analysis."]}

    evidence_record = get_evidence_by_id(ev_id)
    if not evidence_record:
        return {"errors": state.get("errors", []) + ["Evidence not found in DB."]}

    raw_content = evidence_record.get("content", "")

    prompt = f"""
    You are an expert Web3 Risk Analyst. Analyze the following DePIN project data.
    Extract any technical, economic, centralization risks, or red flags.
    Respond ONLY with a valid JSON object. Do not use markdown blocks like ```json.
    
    Data Source Content:
    {raw_content[:5000]}
    """

    try:
        response_text = await call_llm(prompt)
        cleaned_response = response_text.replace("```json", "").replace("```", "").strip()
        findings = json.loads(cleaned_response)
        if not isinstance(findings, dict) or not findings:
            raise ValueError("Risk response must be a nonempty JSON object")
    except Exception as e:
        return {"errors": state.get("errors", []) + [f"Risk analysis failed: {e}"], "current_step": "failed"}

    current_findings = state.get("structured_findings") or {}
    current_findings["risk"] = findings

    print("✅ [Risk Agent] Analysis complete.")
    return {
        "structured_findings": current_findings,
        "current_step": "risk_done"
    }
