import logging
import asyncio
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Import the graph
from agents.graph import app as depin_agent

# Configure logging to show only our own messages
logging.getLogger("httpx").setLevel(logging.WARNING)

async def async_main():
    print("🚀 Starting AGINAZ DePIN Research Agent (Evidence-Based Architecture)...\n")
    print("⚙️ Running LangGraph Workflow...")
    
    # Test URL for the DePIN project
    target_url = "https://teneo.pro/"
    
    # Lightweight State structure based on the new architecture
    initial_state = {
        "target_url": target_url,
        "project_id": 1,
        "evidence_id": None,
        "structured_findings": None,
        "verification_result": None,
        "current_step": "init",
        "errors": []
    }

    # Run the graph asynchronously (ainvoke)
    result = await depin_agent.ainvoke(initial_state)

    # Review the final result
    print("\n==================================================")
    print("🎯 FINAL EXECUTION REPORT:")
    print("==================================================")
    
    if result.get("errors"):
        print("❌ Errors occurred during execution:")
        for err in result["errors"]:
            print(f"  - {err}")
    else:
        print(f"✅ Workflow completed successfully! Step: {result.get('current_step')}")
        print(f"📌 Generated Evidence ID: {result.get('evidence_id')}")
        
        # --- Display the graph's internal state ---
        print("\n📊 FINAL RESEARCH FINDINGS (Tokenomics & Risk):")
        print(json.dumps(result.get("structured_findings", {}), indent=2, ensure_ascii=False))
        
        print("\n⚖️ VERIFICATION RESULT:")
        print(json.dumps(result.get("verification_result", {}), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    # Run the main async loop
    asyncio.run(async_main())
