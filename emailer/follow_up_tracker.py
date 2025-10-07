"""
Follow-Up Tracker
-----------------
- Logs sent cold emails
- Sends follow-ups after X days using LLM-generated messages
"""

import os
import pandas as pd
import datetime
from email.message import EmailMessage
import smtplib
from utils.llm_client import query_ollama
from apply_tool.auto_apply import load_latest_resume
from memory.preference_manager import load_preferences
from datetime import timedelta

TRACKER_FILE = "data/email_tracker.csv"

def ensure_tracker_exists():
    """Ensure the email tracker file exists."""
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(TRACKER_FILE):
        df = pd.DataFrame(columns=["email", "date_sent", "follow_up_date"])
        df.to_csv(TRACKER_FILE, index=False)
        print(f"[DEBUG] ✅ Created new email tracker file at {TRACKER_FILE}")

def log_email_sent(email):
    """Log a sent email for follow-up tracking."""
    ensure_tracker_exists()
    try:
        df = pd.read_csv(TRACKER_FILE)
        new_row = {
            "email": email,
            "date_sent": datetime.now().strftime("%Y-%m-%d"),
            "follow_up_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(TRACKER_FILE, index=False)
        print(f"[DEBUG] ✅ Logged email to {email} for follow-up")
    except Exception as e:
        print(f"[DEBUG] ❌ Failed to log email: {e}")

def get_emails_due_for_followup(days=5):
    """Get list of emails that are due for follow-up."""
    print(f"[DEBUG] 🔍 Checking for emails due for follow-up after {days} days...")
    if not os.path.exists(TRACKER_FILE):
        print("[DEBUG] ❌ No tracker file found")
        return []
    
    df = pd.read_csv(TRACKER_FILE)
    print(f"[DEBUG] 📊 Loaded {len(df)} entries from tracker")
    
    df["sent_date"] = pd.to_datetime(df["sent_date"])
    due_date = datetime.datetime.now() - datetime.timedelta(days=days)
    print(f"[DEBUG] 📅 Checking for emails sent before {due_date.strftime('%Y-%m-%d')}")
    
    due_df = df[df["sent_date"] < due_date]
    due_emails = due_df["email"].tolist()
    print(f"[DEBUG] ✅ Found {len(due_emails)} emails due for follow-up")
    return due_emails

def send_followups():
    """Send follow-up emails to recruiters who haven't responded."""
    print("[DEBUG] 🚀 Starting follow-up email process...")
    
    print("[DEBUG] 📋 Loading preferences...")
    prefs = load_preferences()
    print(f"[DEBUG] ✅ Loaded preferences: {prefs}")
    
    print("[DEBUG] 📄 Loading latest resume...")
    resume_path = load_latest_resume()
    print(f"[DEBUG] ✅ Resume path: {resume_path}")

    emails_to_followup = get_emails_due_for_followup(days=5)
    if not emails_to_followup:
        print("[DEBUG] 💤 No emails due for follow-up today")
        return

    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    
    print(f"[DEBUG] 📧 Email configuration:")
    print(f"[DEBUG] - From: {from_email}")
    print(f"[DEBUG] - SMTP Server: {smtp_server}")
    print(f"[DEBUG] - SMTP Port: {smtp_port}")

    print(f"[DEBUG] 🔁 Preparing to send {len(emails_to_followup)} follow-up emails...")

    for to_email in emails_to_followup:
        print(f"\n[DEBUG] 📧 Processing follow-up for: {to_email}")
        
        # Create a prompt for the LLM to generate a follow-up email
        prompt = f"""
Write a professional follow-up email with the following details:

CANDIDATE INFORMATION:
{prefs.get('description', '')}

TARGET ROLES:
{', '.join(prefs.get('roles', []))}

REQUIREMENTS:
- Keep the email professional and concise (under 150 words)
- Reference the previous email sent 5+ days ago
- Reiterate interest and relevant experience
- Maintain a polite and persistent tone
- Include a clear call to action
- Reattach resume for convenience

FORMAT:
- Professional greeting
- Brief reminder of previous email
- Reiterate key qualifications
- Express continued interest
- Request for update
- Professional closing
"""
        print("[DEBUG] 🤖 Generating follow-up email content...")
        # Get the follow-up email body from the LLM
        body = query_ollama([{"role": "user", "content": prompt}])
        print("[DEBUG] ✅ Email content generated")
        
        subject = f"Following Up: Application for {', '.join(prefs.get('roles', ['Full-Stack Developer']))}"
        print(f"[DEBUG] 📝 Generated subject: {subject}")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        msg.set_content(body)

        print("[DEBUG] 📎 Attaching resume...")
        try:
            with open(resume_path, "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=os.path.basename(resume_path))
            print("[DEBUG] ✅ Resume attached successfully")
        except Exception as e:
            print(f"[DEBUG] ❌ Failed to attach resume: {e}")

        try:
            print("[DEBUG] 📤 Sending follow-up email...")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(from_email, password)
                server.send_message(msg)
            print(f"[DEBUG] ✅ Follow-up email sent successfully to {to_email}")
        except Exception as e:
            print(f"[DEBUG] ❌ Failed to send follow-up email to {to_email}: {e}")

if __name__ == "__main__":
    print("[DEBUG] 🚀 Starting follow-up tracker...")
    send_followups()
