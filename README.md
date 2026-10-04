# Haiox DePIN Research Agent

A Python/LangGraph workflow that fetches a DePIN project page, stores visible page text in PostgreSQL, analyzes tokenomics and risks, checks selected claims against that stored text, and writes a Markdown report and an X/Twitter thread.

## Current workflow

`URL → fetch page text → save evidence → tokenomics → risk → verification → save report → create files`

The graph stops when any stage reports an error. Verification errors do not produce a supported result. A supported or partially supported evaluation requires a quote that occurs verbatim in the stored evidence. This is a mechanical quote check, not independent confirmation that the website is truthful. The verifier reads the first 4,000 characters of stored evidence and checks selected claims; it does not verify every statement in the generated thread.

The adapter uses `curl_cffi` to fetch the page and BeautifulSoup to extract visible text. JavaScript-rendered pages and anti-bot challenges may still fail. The database retains up to 30,000 characters of extracted text, not the original HTML.

## Run locally

Requires Python 3.10+, PostgreSQL, network access, and an OpenAI-compatible API key.

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` in the project root:

```env
DATABASE_URL=postgresql://user:password@host:5432/database
OPENROUTER_API_KEY=your_key
LLM_BASE_URL=https://openrouter.ai/api/v1
TARGET_MODEL=your_main_model
CHEAP_MODEL=your_cheap_model
```

Create the core tables, then run with a project URL:

```powershell
python database/db_setup.py
python main.py https://teneo.pro/
```

A project record is created for a new URL, or an existing matching record is reused. Output files go to `output_threads/`. If the workflow fails, `main.py` exits with an error.

## Limits

The project requires a reachable database and model endpoint for a full run. The page text, analysis, and generated thread remain subject to source quality and model errors. Quotes are checked against extracted page text; the system does not independently verify the site's claims. Existing `output_threads/` files were generated before these fixes and should be treated as historical examples, not validated results.

The core workflow uses `projects`, `evidence`, and `research_reports`. Vector search and whitepaper claims are not part of the current runnable path.
