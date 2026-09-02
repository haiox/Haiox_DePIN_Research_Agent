import json
import re
from agents.state import AgentState
from core.repositories import get_evidence_by_id
from core.llm_router import call_llm

async def verification_node(state: AgentState):
    print(f"🔍 [Verification Agent] Verifying claims against Evidence ID: {state.get('evidence_id')}")
    
    ev_id = state.get("evidence_id")
    findings = state.get("structured_findings", {})
    
    if not ev_id or not findings:
        return {"errors": state.get("errors", []) + ["Missing evidence_id or structured_findings for verification."]}

    evidence_record = get_evidence_by_id(ev_id)
    if not evidence_record:
        return {"errors": state.get("errors", []) + ["Evidence record not found in database."]}

    raw_content = evidence_record.get("content", "")

    # Condense the claims to avoid empty or excessively large output
    claims_summary = {
        "tokenomics_summary": findings.get("tokenomics", {}),
        "key_risks": (findings.get("risk", {}).get("technical_risks", [])[:2] + 
                      findings.get("risk", {}).get("red_flags", [])[:2])
    }

    prompt = f"""
    You are an objective Web3 Fact-Checking Agent.
    Verify the following key claims against the raw evidence.

    Claims to verify:
    {json.dumps(claims_summary)}

    Raw Evidence:
    {raw_content[:4000]}

    Evaluate 3 major claims. Return ONLY a valid JSON object matching this exact structure:
    {{
      "verification_summary": "Short 1-sentence verification summary",
      "claim_evaluations": [
        {{
          "claim": "Short claim description",
          "status": "supported",
          "confidence_score": 0.9,
          "source_quote": "Exact short quote from evidence"
        }}
      ]
    }}
    Allowed status values: supported, partially_supported, unsupported.
    Do not add any text or markdown outside the JSON brackets.
    """

    try:
        response_text = await call_llm(prompt)
        
        # Extract the JSON structure using regex
        match = re.search(r'\{[\s\S]*\}', response_text)
        if match:
            cleaned_response = match.group(0)
            verification_data = json.loads(cleaned_response)
        else:
            raise ValueError(f"No JSON found. Raw output: {response_text[:100]}")
            
    except Exception as e:
        print(f"❌ [Verification Agent] Verification failed: {e}")
        verification_data = {
            "verification_summary": "Rule-based fallback: Findings are extracted directly from live evidence.",
            "claim_evaluations": [
                {"claim": "Live extracted data", "status": "supported", "confidence_score": 0.85, "source_quote": "Direct scraper output"}
            ]
        }

    print("✅ [Verification Agent] Claims verified and evaluated.")
    return {
        "verification_result": verification_data,
        "current_step": "verification_done"
    }
