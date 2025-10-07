
# main_agent.py
# 🧠 Master Controller: Seamless Orchestration of All Tools for Your AI Job Agent

import os
from dotenv import load_dotenv

# Import tools
from tools.job_crawler import run_job_crawler
from tools.resume_optimizer import update_resume_and_description
from tools.email_sender import send_cold_emails
from tools.email_tracker import track_followups
from tools.daily_summary import send_daily_summary
from tools.linkedin_auto_apply_tool.auto_apply_bot import LinkedInAutoApplyBot

load_dotenv()

def main_job_agent():
    print("🔁 Starting AI Job Agent...")

    if os.getenv("UPDATE_RESUME_KEYWORDS", "false") == "true":
        update_resume_and_description()

    job_links = run_job_crawler()

    print("🚀 Applying to jobs on LinkedIn...")
    bot = LinkedInAutoApplyBot()
    bot.login()
    for link in job_links:
        bot.apply_to_job(link)
    bot.close()

    send_cold_emails()
    track_followups()
    send_daily_summary(job_links)

    print("✅ AI Job Agent Completed the Cycle")

if __name__ == "__main__":
    main_job_agent()
