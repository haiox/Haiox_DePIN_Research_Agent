import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")

# Read model settings from the .env file
CHEAP_MODEL = os.getenv("CHEAP_MODEL", "z-ai/glm-5.3-flash")
MAIN_MODEL = os.getenv("TARGET_MODEL", "deepseek/deepseek-v4-flash-0731")

def get_llm(model_choice: str):
    """
    Initializes and returns the LLM instance with the specified model.
    """
    return ChatOpenAI(
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base=LLM_BASE_URL,
        model_name=model_choice,
        temperature=0.2,
        max_tokens=8000
    )

async def call_llm(prompt: str, role: str = "main") -> str:
    """
    Receives a text prompt and selects the appropriate model based on the role.
    role='cheap' -> z-ai/glm-5.3-flash (1.3M Context / Ultra Low Cost)
    role='main'  -> deepseek/deepseek-v4-flash-0731
    """
    selected_model = CHEAP_MODEL if role == "cheap" else MAIN_MODEL
    
    print(f"🧠 [Router] Sending prompt to: {selected_model}")
    
    llm = get_llm(model_choice=selected_model)
    response = await llm.ainvoke(prompt)
    return response.content

if __name__ == "__main__":
    import asyncio
    print("⏳ Testing Smart Dual-Engine Router...")
    try:
        async def test():
            # Test the cost-efficient GLM 5.3 Flash model
            res_cheap = await call_llm("Respond with: 'GLM 5.3 Flash is active and ready!'", role="cheap")
            print(f"✅ Cheap Model Response: {res_cheap}")
            
            # Test the main model
            res_main = await call_llm("Respond with: 'DeepSeek is active and ready!'", role="main")
            print(f"✅ Main Model Response: {res_main}")
            
        asyncio.run(test())
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
