# # apply_tool/auto_apply.py

# """
# Auto-Apply Tool
# ---------------
# This tool simulates job application submissions using:
# - Resume file (latest version)
# - Cover message generated via LLM (Ollama)
# """

# import os
# from utils.llm_client import query_ollama

# def load_latest_resume(resume_dir="data/resumes"):
#     files = sorted(os.listdir(resume_dir), key=lambda x: os.path.getmtime(os.path.join(resume_dir, x)), reverse=True)
#     for file in files:
#         if file.endswith(".pdf") or file.endswith(".docx"):
#             return os.path.join(resume_dir, file)
#     return None

# def apply_to_jobs(jobs, preferences):
#     resume_path = load_latest_resume()
#     user_description = preferences.get("description", "")
    
#     if not resume_path:
#         print("[AutoApply] ❌ No resume found in resume directory.")
#         return
    
#     print(f"[AutoApply] ✅ Using resume: {resume_path}")
#     print(f"[AutoApply] 🔍 Found {len(jobs)} job(s) to apply.")

#     for job in jobs:
#         job_desc_summary = f"Job title: {job['title']}\nCompany: {job['company']}\nLocation: {job['location']}\nPosted: {job['posted']}"
        
#         # Use local LLM to generate cover message
#         prompt = f"""
# Given my background as: "{user_description}"

# Write a short professional cover message I could use to apply for the following job:
# {job_desc_summary}
#         """
#         cover_letter = query_ollama(prompt)

#         print(f"\n🧾 Applying to: {job['title']} at {job['company']}")
#         print(f"🔗 Link: {job['link']}")
#         print(f"📄 Resume: {resume_path}")
#         print("💬 Cover Message:\n", cover_letter)
#         print("-" * 50)


import os
from utils.llm_client import query_ollama

def load_latest_resume(resume_dir="data/resumes"):
    """Load the most recent resume from the resumes directory."""
    print(f"[DEBUG] 📂 Looking for resumes in: {resume_dir}")
    
    # Create directory if it doesn't exist
    if not os.path.exists(resume_dir):
        print(f"[DEBUG] 📁 Creating resume directory: {resume_dir}")
        os.makedirs(resume_dir, exist_ok=True)
        print(f"[DEBUG] ⚠️ No resumes found in {resume_dir}. Please add your resume (PDF or DOCX) to this directory.")
        return None
    
    try:
        files = sorted(os.listdir(resume_dir), key=lambda x: os.path.getmtime(os.path.join(resume_dir, x)), reverse=True)
        print(f"[DEBUG] 📄 Found {len(files)} files in resume directory")
        
        for file in files:
            if file.endswith(".pdf") or file.endswith(".docx"):
                resume_path = os.path.join(resume_dir, file)
                print(f"[DEBUG] ✅ Found resume: {resume_path}")
                return resume_path
                
        print(f"[DEBUG] ⚠️ No PDF or DOCX files found in {resume_dir}")
        return None
        
    except Exception as e:
        print(f"[DEBUG] ❌ Error loading resume: {str(e)}")
        return None

def read_resume_text(resume_path):
    # ✅ Optional enhancement: Add docx/pdf text extraction
    try:
        with open(resume_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return "Resume content not accessible as plain text."

def apply_to_jobs(jobs, preferences):
    resume_path = load_latest_resume()
    user_description = preferences.get("description", "")
    simulate_submission = preferences.get("simulate_submission", True)

    if not resume_path:
        print("[AutoApply] ❌ No resume found in resume directory.")
        return

    print(f"[AutoApply] ✅ Using resume: {resume_path}")
    print(f"[AutoApply] 🔍 Found {len(jobs)} job(s) to apply.")

    os.makedirs("data/applied_jobs", exist_ok=True)

    for index, job in enumerate(jobs, 1):
        job_title = job['title']
        company = job['company']
        location = job['location']
        posted = job['posted']
        link = job['link']

        job_description = job.get('description', 'N/A')

        job_desc_summary = (
            f"🔹 Job Title: {job_title}\n"
            f"🔹 Company: {company}\n"
            f"🔹 Location: {location}\n"
            f"🔹 Posted: {posted}\n"
            f"🔹 Job Description (snippet): {job_description}\n"
            f"🔹 Apply Link: {link}"
        )

        # 🧠 Prompt for local LLM (Ollama) using resume and job info
        prompt = f"""
You are an AI career assistant helping a candidate write a personalized cover letter.

Candidate Profile:
{user_description}

Job Posting:
{job_desc_summary}

Generate a short, professional, confident cover message (80-120 words) that matches the candidate to the job and includes enthusiasm, skill relevance, and a clear intent to apply.
        """

        cover_letter = query_ollama(prompt)

        print(f"\n🧾 Applying to: {job_title} at {company}")
        print(f"🔗 Link: {link}")
        print(f"📄 Resume: {resume_path}")
        print("💬 Cover Message:\n", cover_letter)
        print("-" * 60)

        if simulate_submission:
            safe_filename = f"{company.replace(' ', '_')}_{job_title.replace(' ', '_')[:30]}.txt"
            filepath = os.path.join("data/applied_jobs", safe_filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Resume Path: {resume_path}\n\n")
                f.write(f"{job_desc_summary}\n\n")
                f.write("Generated Cover Message:\n")
                f.write(cover_letter.strip())

            print(f"💾 Simulated application saved to {filepath}")
