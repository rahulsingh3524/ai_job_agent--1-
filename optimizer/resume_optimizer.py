# optimizer/resume_optimizer.py

"""
Resume Optimizer
----------------
Uses offline LLM (Ollama) to:
- Analyze resume text
- Suggest keyword improvements
- Rewrite summary section for job alignment
"""

import os
from utils.llm_client import query_ollama

def load_resume_text(resume_path):
    # You can replace this with PDF/DOCX parsing if needed
    try:
        with open(resume_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[Resume Optimizer] ❌ Could not read resume: {e}")
        return ""

def optimize_resume(preferences, resume_dir="data/resumes"):
    resume_path = sorted(
        [os.path.join(resume_dir, f) for f in os.listdir(resume_dir)],
        key=os.path.getmtime,
        reverse=True
    )[0]

    resume_text = load_resume_text(resume_path)
    user_description = preferences.get("description", "")

    if not resume_text:
        return

    prompt = f"""
I am targeting job roles like: "{', '.join(preferences.get('roles', []))}".
My current resume content is below:

{resume_text}

Please suggest:
1. Keywords to improve visibility for these roles
2. Rewrite of the summary section to better align with "{user_description}"
    """
    
    result = query_ollama(prompt)
    
    print("📈 Resume Optimization Suggestions:")
    print(result)
