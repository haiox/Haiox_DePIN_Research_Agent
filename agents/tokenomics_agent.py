import json
from agents.state import AgentState
from core.repositories import get_evidence_by_id
from core.llm_router import call_llm

async def tokenomics_node(state: AgentState):
    print(f"🪙 [Tokenomics Agent] Analyzing Evidence ID: {state.get('evidence_id')}")
    
    ev_id = state.get("evidence_id")
    if not ev_id:
        return {"errors": state.get("errors", []) + ["No evidence_id found."]}

    evidence_record = get_evidence_by_id(ev_id)
    if not evidence_record:
        return {"errors": state.get("errors", []) + ["Evidence not found in DB."]}

    raw_content = evidence_record.get("content", "")

    prompt = f"""
    You are an expert Web3 Tokenomics Analyst. Analyze the following DePIN project data.
    Extract the tokenomics details (e.g., Token Name, Total Supply, Utility, Distribution).
    Respond ONLY with a valid JSON object. Do not use markdown blocks like ```json.
    
    Data Source Content:
    {raw_content[:5000]}
    """

    try:
        response_text = await call_llm(prompt)
        # Remove any Markdown formatting from the model output
        cleaned_response = response_text.replace("```json", "").replace("```", "").strip()
        findings = json.loads(cleaned_response)
    except Exception as e:
        print(f"❌ [Tokenomics Agent] LLM parsing failed: {e}")
        findings = {"error": f"Failed to parse tokenomics data: {str(e)}"}

    current_findings = state.get("structured_findings") or {}
    current_findings["tokenomics"] = findings

    print("✅ [Tokenomics Agent] Analysis complete.")
    return {
        "structured_findings": current_findings,
        "current_step": "tokenomics_done"
    }
