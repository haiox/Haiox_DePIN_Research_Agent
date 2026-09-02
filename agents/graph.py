from agents.twitter_agent import twitter_factory_node
from langgraph.graph import StateGraph, END
from agents.persist_agent import persist_research_node
from agents.state import AgentState
from tools.smart_miner_adapter import fetch_raw_data_from_miner
from core.repositories import save_evidence

# Import agents connected to the language model
from agents.tokenomics_agent import tokenomics_node
from agents.risk_agent import risk_node
from agents.verification_agent import verification_node

# ==========================================
# Nodes
# ==========================================

async def extract_and_evidence_node(state: AgentState):
    print(f"🔄 [Graph] Step 1: Extraction & Evidence Persistence for {state['target_url']}")
    
    raw_data = await fetch_raw_data_from_miner(state["target_url"])
    
    if not raw_data:
        errors = state.get("errors", [])
        errors.append("Extraction failed from Smart Miner.")
        return {"errors": errors, "current_step": "failed"}

    p_id = state.get("project_id") or 1 
    ev_id = save_evidence(p_id, state["target_url"], raw_data)

    if not ev_id:
        errors = state.get("errors", [])
        errors.append("Evidence persistence failed in Supabase.")
        return {"errors": errors, "current_step": "failed"}

    print(f"✅ [Graph] Evidence injected into State -> ID: {ev_id}")
    return {
        "evidence_id": ev_id,
        "current_step": "evidence_persisted"
    }

# ==========================================
# Graph Construction
# ==========================================

workflow = StateGraph(AgentState)

workflow.add_node("extract_evidence", extract_and_evidence_node)
workflow.add_node("tokenomics", tokenomics_node)
workflow.add_node("risk", risk_node)
workflow.add_node("verification", verification_node)
workflow.add_node("persist_research", persist_research_node)

workflow.set_entry_point("extract_evidence")
workflow.add_edge("extract_evidence", "tokenomics")
workflow.add_edge("tokenomics", "risk")
workflow.add_edge("risk", "verification")
workflow.add_edge("verification", "persist_research")
workflow.add_edge("persist_research", END)
# Add the Twitter node
workflow.add_node("twitter_factory", twitter_factory_node)

# Update the routing for the final stages:
workflow.add_edge("verification", "persist_research")
workflow.add_edge("persist_research", "twitter_factory") # Proceed to Twitter after the database step
workflow.add_edge("twitter_factory", END) # Then finish

app = workflow.compile()
