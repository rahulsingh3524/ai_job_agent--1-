"""
Cold Email Sender
----------------
Handles sending personalized cold emails to recruiters with resume attachments.
"""

import json
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from utils.llm_client import query_ollama

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

def load_recruiter_emails(csv_path: str = "data/recruiter_emails.csv") -> pd.DataFrame:
    """
    Load recruiter emails from CSV file.
    Expected columns: company, email, name, role, location
    """
    try:
        if not os.path.exists(csv_path):
            logging.error(f"Recruiter emails file not found: {csv_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(csv_path)
        required_columns = ['Company', 'Email']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logging.error(f"Missing required columns in {csv_path}: {missing_columns}")
            return pd.DataFrame()
        
        logging.info(f"Successfully loaded {len(df)} recruiter records from {csv_path}")
        return df
    except Exception as e:
        logging.error(f"Error loading recruiter emails: {str(e)}")
        return pd.DataFrame()

def create_email_message(
    to_email: str,
    subject: str,
    body: str,
    resume_path: str = None
) -> MIMEMultipart:
    """
    Create an email message with optional resume attachment.
    """
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add body
    msg.attach(MIMEText(body, 'plain'))
    
    # Add resume attachment if provided
    if resume_path and os.path.exists(resume_path):
        try:
            with open(resume_path, 'rb') as f:
                resume = MIMEApplication(f.read(), _subtype='pdf')
                resume.add_header('Content-Disposition', 'attachment', filename=os.path.basename(resume_path))
                msg.attach(resume)
                logging.info(f"Successfully attached resume: {resume_path}")
        except Exception as e:
            logging.error(f"Error attaching resume: {str(e)}")
    else:
        logging.warning(f"Resume not found at path: {resume_path}")
    
    return msg

def clean_email_body(body: str) -> str:
    """
    Clean the email body by removing invalid control characters and formatting.
    
    Args:
        body (str): The raw email body text
        
    Returns:
        str: Cleaned email body text
    """
    if not body:
        return ""
        
    # Remove any thinking process
    if "<think>" in body:
        body = body.split("</think>")[-1].strip()
    
    # Remove markdown code blocks
    if body.startswith("```json"):
        body = body[7:]
    elif body.startswith("```"):
        body = body[3:]
    if body.endswith("```"):
        body = body[:-3]
    
    # Remove any JSON formatting
    body = body.strip()
    if body.startswith("{"):
        try:
            import json
            parsed = json.loads(body)
            if isinstance(parsed, dict) and "email_body" in parsed:
                body = parsed["email_body"]
        except:
            pass
    
    # Replace escaped newlines with actual newlines
    body = body.replace("\\n", "\n")
    
    # Remove any remaining control characters
    import re
    body = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', body)
    
    return body.strip()

def validate_email_parameters(email_body: str, roles: list) -> tuple[bool, str]:
    """
    Validate email parameters before sending.
    
    Args:
        email_body (str): The email body to validate
        roles (list): List of roles to validate
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not email_body:
        return False, "Email body cannot be empty"
    
    if not roles:
        return False, "At least one role must be specified"
    
    # Validate roles
    forbidden_roles = ["recruiter", "candidate", "applicant"]
    for role in roles:
        if role.lower() in forbidden_roles:
            return False, f"Invalid role: {role}. Roles must be job titles only."
    
    # # Validate email body
    # forbidden_placeholders = [
    #     "[Your Name]", "[Recruiter's Name]", "[Company Name]", 
    #     "[Position]", "[Role]", "[Skills]", "[Experience]"
    # ]
    
    # for placeholder in forbidden_placeholders:
    #     if placeholder in email_body:
    #         return False, f"Email body contains forbidden placeholder: {placeholder}"
    
    return True, ""

# def send_cold_emails(email_body: str = None, roles: list = None):
#     """
#     Main function to send cold emails to recruiters.
#     Uses provided email_body and roles, or generates personalized content if not provided.
    
#     Args:
#         email_body (str): The email body to send. If None, will generate one.
#         roles (list): List of job roles to target. If None, will use from recruiter data.
#     """
#     try:
#         # Load environment variables
#         email_user = os.getenv('EMAIL_USER')
#         email_password = os.getenv('EMAIL_PASSWORD')
#         smtp_server = os.getenv('SMTP_SERVER')
#         smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
#         if not all([email_user, email_password, smtp_server]):
#             logging.error("Missing required environment variables")
#             return
        
#         # Load recruiter emails
#         recruiters_df = load_recruiter_emails()
#         if recruiters_df.empty:
#             logging.error("No recruiter records found")
#             return
        
#         # Connect to SMTP server
#         try:
#             server = smtplib.SMTP(smtp_server, smtp_port)
#             server.starttls()
#             server.login(email_user, email_password)
#             logging.info("Successfully connected to SMTP server")
#         except Exception as e:
#             logging.error(f"Failed to connect to SMTP server: {str(e)}")
#             return
        
#         # Process each recruiter
#         for _, recruiter in recruiters_df.iterrows():
#             try:
#                 # Use provided email_body or generate one
#                 if email_body is None:
#                     # Generate personalized email content using LLM
#                     prompt = f"""Generate a personalized cold email for a recruiter at {recruiter['company']}.
#                     The email should be professional and include:
#                     1. A brief introduction
#                     2. Relevant experience and skills
#                     3. Why interested in the company
#                     4. A call to action
                    
#                     Recruiter details:
#                     - Name: {recruiter['name']}
#                     - Role: {recruiter['role']}
#                     - Location: {recruiter['location']}
                    
#                     The email should be ready to send, with no placeholders or thinking process."""
                    
#                     response = query_ollama([{"role": "user", "content": prompt}])
#                     current_email_body = response.get("message", {}).get("content", "").strip()
#                 else:
#                     current_email_body = email_body
                
#                 # Clean the email body
#                 current_email_body = clean_email_body(current_email_body)
                
#                 # Use provided roles or recruiter's role
#                 target_role = roles[0] if roles else recruiter['role']
                
#                 # Create and send email
#                 subject = f"Application for {target_role} at {recruiter['company']} | Resume Attached"
#                 msg = create_email_message(
#                     to_email=recruiter['email'],
#                     subject=subject,
#                     body=current_email_body,
#                     resume_path="data/resumes/Rahul Singh-Resume.pdf"
#                 )
                
#                 server.send_message(msg)
#                 logging.info(f"Successfully sent email to {recruiter['email']}")
                
#                 # Log the sent email for follow-up tracking
#                 log_email(recruiter['email'], recruiter['company'], target_role)
                
#             except Exception as e:
#                 logging.error(f"Error processing recruiter {recruiter['email']}: {str(e)}")
#                 continue
        
#         server.quit()
#         logging.info("Finished sending cold emails")
        
#     except Exception as e:
#         logging.error(f"Error in send_cold_emails: {str(e)}")


# def send_cold_emails(prefs: dict):
#     """
#     Main function to send cold emails to recruiters.
#     Uses provided prefs to extract description and roles, and generate a personalized email body.
    
#     Args:
#         prefs (dict): User preferences containing description and roles.
#     """
#     try:
#         # Load environment variables
#         email_user = os.getenv('EMAIL_USER')
#         email_password = os.getenv('EMAIL_PASSWORD')
#         smtp_server = os.getenv('SMTP_SERVER')
#         smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
#         if not all([email_user, email_password, smtp_server]):
#             logging.error("Missing required environment variables")
#             return
        
#         # Load recruiter emails
#         recruiters_df = load_recruiter_emails()
#         if recruiters_df.empty:
#             logging.error("No recruiter records found")
#             return
        
#         # Extract description and roles from prefs
#         description = prefs.get("description", "")
#         roles = prefs.get("roles", [])
        
#         if not description or not roles:
#             logging.error("Missing required parameters: description or roles")
#             return
        
#         # Generate email body using LLM
#         prompt = f"""Generate a personalized cold email for a recruiter.
#         The email should include:
#         1. A professional greeting
#         2. A brief introduction
#         3. Relevant experience and skills based on the description: {description}
#         4. Why interested in the company
#         5. A call to action
#         6. A professional closing

#         The email should be ready to send, with no placeholders or thinking process. Use the user's actual name and details instead of placeholders."""

#         print(f"[DEBUG] Prompt: {prompt}")
#         response = query_ollama([{"role": "user", "content": prompt}])
#         print(f"[DEBUG] Response: {response}")
#         email_body = response.get("message", {}).get("content", "").strip()
#         print(f"[DEBUG] Email body: {email_body}")
#         # Clean the email body
#         email_body = clean_email_body(email_body)
#         print(f"[DEBUG] Cleaned email body: {email_body}")
#         # Connect to SMTP server
#         try:
#             server = smtplib.SMTP(smtp_server, smtp_port)
#             server.starttls()
#             server.login(email_user, email_password)
#             logging.info("Successfully connected to SMTP server")
#         except Exception as e:
#             logging.error(f"Failed to connect to SMTP server: {str(e)}")
#             return
        
#         # Process each recruiter
#         for _, recruiter in recruiters_df.iterrows():
#             try:
#                 # Use the first role as the target role
#                 target_role = roles[0]
                
#                 # Create and send email
#                 subject = f"Application for {target_role} at {recruiter['company']} | Resume Attached"
#                 msg = create_email_message(
#                     to_email=recruiter['email'],
#                     subject=subject,
#                     body=email_body,
#                     resume_path="data/resumes/Rahul Singh-Resume.pdf"
#                 )
                
#                 server.send_message(msg)
#                 logging.info(f"Successfully sent email to {recruiter['email']}")
                
#                 # Log the sent email for follow-up tracking
#                 log_email(recruiter['email'], recruiter['company'], target_role)
                
#             except Exception as e:
#                 logging.error(f"Error processing recruiter {recruiter['email']}: {str(e)}")
#                 continue
        
#         server.quit()
#         logging.info("Finished sending cold emails")
        
#     except Exception as e:
#         logging.error(f"Error in send_cold_emails: {str(e)}")

def send_cold_emails(prefs: dict):
    """
    Main function to send cold emails to recruiters.
    Uses provided prefs to extract description and roles, and generate a personalized email body.
    
    Args:
        prefs (dict): User preferences containing description and roles.
    """
    try:
        # Load environment variables
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
        if not all([email_user, email_password, smtp_server]):
            logging.error("Missing required environment variables")
            return
        
        # Load recruiter emails
        recruiters_df = load_recruiter_emails()
        if recruiters_df.empty:
            logging.error("No recruiter records found")
            return
        
        # Extract description and roles from prefs
        description = prefs.get("description", "")
        roles = prefs.get("roles", [])
        
        if not description or not roles:
            logging.error("Missing required parameters: description or roles")
            return
        
        # Generate email body using LLM
        prompt = f"""Generate a personalized cold email for a recruiter.
        The email should include:
        1. A professional greeting
        2. A brief introduction
        3. Relevant experience and skills based on the description: {description}
        4. Why interested in the company
        5. A call to action
        6. A professional closing
        
        The email should be ready to send, with no placeholders or thinking process. Use the user's actual name and details instead of placeholders."""
        
        response = query_ollama([{"role": "user", "content": prompt}])
        print(f"[DEBUG] Response for email body generation: {response}")
        # Clean the response to ensure it's valid JSON
        content = response.get("message", {}).get("content", "").strip()
        
        # Remove any <think> tags and other unwanted text
        # if "<think>" in content:
        #     content = content.split("</think>")[-1].strip()
        # print(f"[DEBUG] Content after removing <think> tags: {content}")
        # # Extract the JSON part using regex
        # import re
        # json_match = re.search(r'\{.*\}', content)
        import re
        # Safely remove <think> block
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

        # Match JSON across multiple lines
        json_match = re.search(r'\{.*\}', content, re.DOTALL)

        print(f"[DEBUG] JSON match: {json_match}")
        if json_match:
            json_content = json_match.group(0)
        else:
            logging.error("No valid JSON found in the response")
            return
        
        # Try to parse the JSON
        try:
            parsed_response = json.loads(json_content)
            email_body = parsed_response.get("parameters", {}).get("email_body", "")

            email_body = parsed_response.get("parameters", {}).get("prefs", {}).get("description", "").strip()

            if not email_body:
                logging.warning("Email body not provided by LLM. Using default cold email body.")
                email_body = (
                    "Dear Recruiter,\n\n"
                    "I hope this message finds you well. I am writing to express my interest in suitable opportunities "
                    "within your esteemed organization. With hands-on experience in full-stack development and a strong "
                    "foundation in Python, React.js, and Node.js, I am confident in my ability to contribute effectively.\n\n"
                    "I would appreciate the opportunity to discuss how my background aligns with your team's needs.\n\n"
                    "Thank you for your time and consideration.\n\n"
                    "Best regards,\n"
                    "Rahul Singh Dhaakad\n"
                    "rahulsinghdhaakad@gmail.com"
                )


            roles = parsed_response.get("parameters", {}).get("prefs", {}).get("roles", [])
            # Fallback to a default role if roles list is empty
            if not roles:
                logging.warning("No roles provided by LLM. Using default role.")
                roles = ["Software Engineer"]  # or fetch from preferences

            print(f"[DEBUG] Email body: {email_body}")
            print(f"[DEBUG] Roles: {roles}")    
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {str(e)}")
            return
        
        # # Clean the email body to ensure no placeholders are present
        # if any(placeholder in email_body for placeholder in ["[Your Name]", "[Recruiter's Name]", "[Company Name]"]):
        #     logging.error("Email body contains placeholders")
        #     return
        
        # Connect to SMTP server
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_user, email_password)
            logging.info("Successfully connected to SMTP server")
        except Exception as e:
            logging.error(f"Failed to connect to SMTP server: {str(e)}")
            return
        
        # Process each recruiter
        for _, recruiter in recruiters_df.iterrows():
            try:
                print(f"[DEBUG] Recruiter: {recruiter}")
                print(f"[DEBUG] Email body: {email_body}")
                print(f"[DEBUG] Roles: {roles}")
                print(f"[DEBUG] Recruiter email: {recruiter['Email']}")
                print(f"[DEBUG] Recruiter company: {recruiter['Company']}")
                # Use the first role as the target role
                target_role = roles[0]
                
                # Create and send email
                subject = f"Application for {target_role} at {recruiter['Company']} | Resume Attached"
                msg = create_email_message(
                    to_email=recruiter['Email'],
                    subject=subject,
                    body=email_body,
                    resume_path="data/resumes/Rahul Singh-Resume.pdf"
                )
                
                server.send_message(msg)
                logging.info(f"Successfully sent email to {recruiter['Email']}")
                
                # Log the sent email for follow-up tracking
                log_email(recruiter['Email'], recruiter['Company'], target_role)
                
            except Exception as e:
                logging.error(f"Error processing recruiter {recruiter['Email']}: {str(e)}")
                continue
        
        server.quit()
        logging.info("Finished sending cold emails")
        
    except Exception as e:
        logging.error(f"Error in send_cold_emails: {str(e)}")



def log_email(email: str, company: str, role: str):
    """
    Log sent emails to a CSV file for follow-up tracking.
    """
    log_file = "data/sent_emails.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Create log file if it doesn't exist
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.write("timestamp,email,company,role\n")
        
        # Append new entry
        with open(log_file, 'a') as f:
            f.write(f"{timestamp},{email},{company},{role}\n")
        
        logging.info(f"Logged email to {log_file}")
    except Exception as e:
        logging.error(f"Error logging email: {str(e)}")

if __name__ == "__main__":
    send_cold_emails()
