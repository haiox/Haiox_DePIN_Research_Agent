from core.repositories import save_research_report
from agents.state import AgentState

async def persist_research_node(state: AgentState):
    print("🔄 [Graph] Step 5: Persisting Final Verified Research Object")
    
    ev_id = state.get("evidence_id")
    findings = state.get("structured_findings")
    if findings is None:
        findings = {}
        
    tokenomics = findings.get("tokenomics", {})
    # The rest of the code remains unchanged...
    risk = findings.get("risk", {})
    verification = state.get("verification_result", {})
    
    if ev_id:
        report_id = save_research_report(ev_id, tokenomics, risk, verification)
        if report_id:
             return {"current_step": "persisted"}
             
    return {"errors": state.get("errors", []) + ["Failed to persist research report."]}
