import json
import requests
from pathlib import Path

OUT = Path("outputs")
findings = json.loads((OUT / "findings.json").read_text())

prompt = f"""
You are a careful data analyst.

Summarize ONLY the computed findings below.
Do not invent numbers.
Do not add external facts.
If something is missing, say so.
Write:
- 5 bullet points of key findings
- 3 limitations of the data
- 2 suggestions for further analysis

Computed findings:
{json.dumps(findings, indent=2)}
"""

# Save the prompt so you have proof of what was sent
(OUT / "summary_prompt.txt").write_text(prompt)

# Send to local LLM (Ollama). 
try:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
        },
    )
    summary = r.json()["response"]
    (OUT / "llm_summary_raw.md").write_text(summary)
    print("Summary generated! Check outputs/llm_summary_raw.md")
    print("-" * 40)
    print(summary)
except Exception as e:
    print(f"Could not connect to local LLM. Error: {e}")
    print("You can manually copy the prompt from outputs/summary_prompt.txt and paste it into ChatGPT/Claude.")