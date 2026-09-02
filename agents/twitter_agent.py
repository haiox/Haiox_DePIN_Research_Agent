import json
import os
import re
from core.llm_router import call_llm
from agents.state import AgentState

async def twitter_factory_node(state: AgentState):
    print("✍️ [Graph] Step 6: Generating Content (Twitter & GitHub Reports)")
    
    findings = state.get("structured_findings", {})
    verification = state.get("verification_result", {})
    target_url = state.get("target_url", "Unknown Project")
    
    if not findings:
        return {"errors": state.get("errors", []) + ["No findings available to generate content."]}

    # Optimized system prompt for higher LLM reliability
    prompt = f"""
    Act as a Web3 & DePIN On-Chain Analyst.
    Write a 4-tweet Twitter thread based on the research data below.
    
    Project: {target_url}
    Data: {json.dumps(findings)}
    
    RULES:
    1. Language: STRICTLY ENGLISH.
    2. Tone: Professional, investigative, Alpha Caller style.
    3. Format: Number each tweet clearly (e.g., 🧵 1/4:, 2/4:).
    4. Output raw tweets ONLY. Do not write introductory sentences.
    """
    
    try:
        thread_content = await call_llm(prompt)
        
        # Fallback mechanism in case of an empty response
        if not thread_content or not thread_content.strip():
            print("⚠️ [Warning] Primary LLM returned empty. Retrying with a simplified prompt...")
            fallback_prompt = f"Write a short, professional English Twitter thread summarizing this DePIN project: {target_url}. Data: {json.dumps(findings)}"
            thread_content = await call_llm(fallback_prompt)
            
            # Final safety check
            if not thread_content or not thread_content.strip():
                thread_content = "⚠️ Error: The LLM API failed to generate a response after multiple attempts. Please run the script again."

        # File generation logic
        project_name_match = re.search(r'https?://(?:www\.)?([^/]+)', target_url)
        project_name = project_name_match.group(1).replace('.', '_') if project_name_match else "project"
        
        os.makedirs("output_threads", exist_ok=True)
        
        # 1. Save the Twitter Thread
        thread_filepath = os.path.join("output_threads", f"{project_name}_thread.txt")
        with open(thread_filepath, "w", encoding="utf-8") as f:
            f.write(thread_content.strip())
            
        # 2. Save the GitHub Markdown Report
        report_filepath = os.path.join("output_threads", f"{project_name}_GitHub_Report.md")
        with open(report_filepath, "w", encoding="utf-8") as f:
            f.write(f"# 🕵️‍♂️ DePIN Research Report: {target_url}\n\n")
            f.write("## 📊 Tokenomics\n")
            f.write(f"```json\n{json.dumps(findings.get('tokenomics', {}), indent=2)}\n```\n\n")
            f.write("## ⚠️ Risk Analysis\n")
            f.write(f"```json\n{json.dumps(findings.get('risk', {}), indent=2)}\n```\n\n")
            f.write("## ⚖️ Verification Results\n")
            f.write(f"```json\n{json.dumps(verification, indent=2)}\n```\n")

        print(f"✅ [Content Factory] Twitter thread saved in: {thread_filepath}")
        print(f"✅ [Content Factory] GitHub Report saved in: {report_filepath}")
        
        return {"current_step": "content_generated"}
        
    except Exception as e:
        print(f"❌ [Content Factory] Error: {e}")
        return {"errors": state.get("errors", []) + [str(e)]}