from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """
    Lightweight State for LangGraph.
    This carries ONLY references and structured data, NEVER raw HTML/text.
    """
    target_url: str
    project_id: Optional[int]           # Project ID in the database
    evidence_id: Optional[int]          # ID of the evidence stored in the Evidence Layer
    
    # Structured outputs from specialized agents (tokenomics, risk, etc.)
    structured_findings: Optional[Dict[str, Any]]
    
    # Final verification result
    verification_result: Optional[Dict[str, Any]]
    
    # Current status and error management
    current_step: str
    errors: List[str]
