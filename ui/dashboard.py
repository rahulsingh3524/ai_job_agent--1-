# # import streamlit as st
# # from memory.preference_manager import load_preferences, save_preferences
# # from crawler.job_crawler import crawl_jobs
# # from apply_tool.auto_apply import apply_to_jobs
# # from optimizer.resume_optimizer import optimize_resume
# # from emailer.cold_email_sender import send_cold_emails

# # st.title("AI Job Agent Dashboard")

# # prefs = load_preferences()

# # with st.form("preferences_form"):
# #     roles = st.text_area("Roles to search (comma separated)", value=", ".join(prefs['roles']))
# #     location = st.text_input("Job Location", value=prefs['location'])
# #     days_posted = st.slider("Recent job postings within days", 1, 30, prefs['days_posted'])
# #     resume_path = st.text_input("Resume Path", value=prefs['resume_path'])
# #     description = st.text_area("Your job application description", value=prefs['description'])
# #     recruiter_emails = st.text_area("Recruiter Emails (comma separated)", value=", ".join(prefs.get('recruiter_emails', [])))

# #     submitted = st.form_submit_button("Save Preferences")
# #     if submitted:
# #         prefs['roles'] = [r.strip() for r in roles.split(",") if r.strip()]
# #         prefs['location'] = location
# #         prefs['days_posted'] = days_posted
# #         prefs['resume_path'] = resume_path
# #         prefs['description'] = description
# #         prefs['recruiter_emails'] = [e.strip() for e in recruiter_emails.split(",") if e.strip()]
# #         save_preferences(prefs)
# #         st.success("Preferences saved!")

# # if st.button("Run Job Crawler"):
# #     jobs = crawl_jobs(prefs)
# #     st.write(f"Found {len(jobs)} jobs")
# #     for job in jobs:
# #         st.write(job)

# # if st.button("Optimize Resume"):
# #     optimized = optimize_resume(prefs)
# #     st.write("Optimized Resume Summary:")
# #     st.write(optimized)

# # if st.button("Auto Apply to Jobs"):
# #     jobs = crawl_jobs(prefs)
# #     applied = apply_to_jobs(jobs, prefs)
# #     st.write(f"Applied to {len(applied)} jobs.")

# # if st.button("Send Cold Emails"):
# #     send_cold_emails(prefs)
# #     st.success("Cold emails sent (or attempted).")


# # ui/dashboard.py

# import sys
# import os

# # ✅ Force Python to treat the parent directory as the root
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# import streamlit as st
# from crawler.job_crawler import crawl_jobs
# from apply_tool.auto_apply import apply_to_jobs
# from emailer.cold_email_sender import send_cold_emails
# from emailer.follow_up_tracker import send_followups
# from optimizer.resume_optimizer import optimize_resume
# from memory.preference_manager import load_preferences, save_preferences
# import pandas as pd
# import os

# st.set_page_config(page_title="AI Job Agent Dashboard", layout="wide")

# st.title("🤖 AI Job Agent Dashboard")

# # Load or initialize user preferences
# prefs = load_preferences()

# with st.sidebar:
#     st.header("Your Preferences")
#     roles = st.text_area("Job Roles (comma-separated)", value=",".join(prefs.get("roles", ["Software Engineer", "Developer"])))
#     locations = st.text_input("Locations (comma-separated)", value=",".join(prefs.get("locations", ["India"])))
#     companies = st.text_area("Companies for Email Scraping (comma-separated)", value=",".join(prefs.get("companies", ["Google", "Microsoft", "TCS", "Infosys", "Wipro"])))
#     followup_days = st.number_input("Follow-up Delay (days)", min_value=1, max_value=30, value=prefs.get("followup_days", 5))

#     if st.button("💾 Save Preferences"):
#         prefs["roles"] = [r.strip() for r in roles.split(",")]
#         prefs["locations"] = [l.strip() for l in locations.split(",")]
#         prefs["companies"] = [c.strip() for c in companies.split(",")]
#         prefs["followup_days"] = followup_days
#         save_preferences(prefs)
#         st.success("✅ Preferences saved!")

# st.header("Actions")

# col1, col2 = st.columns(2)

# with col1:
#     if st.button("🕷️ Crawl LinkedIn Jobs"):
#         with st.spinner("Crawling jobs..."):
#             jobs = crawl_jobs(prefs)
#             st.success(f"Found {len(jobs)} jobs.")
#             # Save jobs for display
#             jobs_df = pd.DataFrame(jobs)
#             jobs_df.to_csv("data/latest_jobs.csv", index=False)

# with col2:
#     if st.button("📝 Optimize Resume"):
#         with st.spinner("Optimizing resume..."):
#             optimize_resume(prefs)
#             st.success("Resume optimized!")

# st.markdown("---")

# if os.path.exists("data/latest_jobs.csv"):
#     jobs_df = pd.read_csv("data/latest_jobs.csv")
#     st.subheader("Latest Crawled Jobs")
#     st.dataframe(jobs_df)

# col3, col4 = st.columns(2)
# with col3:
#     if st.button("✉️ Send Cold Emails"):
#         with st.spinner("Sending cold emails..."):
#             send_cold_emails(prefs)
#             st.success("Cold emails sent!")

# with col4:
#     if st.button("🔁 Send Follow-ups"):
#         with st.spinner("Sending follow-up emails..."):
#             send_followups()
#             st.success("Follow-up emails sent!")

# st.markdown("---")

# st.subheader("Email Tracker Overview")
# if os.path.exists("data/email_tracker.csv"):
#     df = pd.read_csv("data/email_tracker.csv")
#     st.dataframe(df)
# else:
#     st.info("No emails sent yet.")

# st.markdown("---")

# st.info("💡 Tip: Run `ollama run llama3` before starting the dashboard to enable LLM-powered features.")


# # ui/dashboard.py

# import sys
# import os

# # ✅ Ensure correct path to import from parent directories
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import streamlit as st
# import pandas as pd
# from crawler.job_crawler import crawl_jobs
# from apply_tool.auto_apply import apply_to_jobs
# from emailer.cold_email_sender import send_cold_emails
# from emailer.follow_up_tracker import send_followups
# from optimizer.resume_optimizer import optimize_resume
# from memory.preference_manager import load_preferences, save_preferences

# st.set_page_config(page_title="AI Job Agent Dashboard", layout="wide")

# st.title("🤖 AI Job Agent Dashboard")

# # Load or initialize user preferences
# prefs = load_preferences()



# with st.sidebar:
#     st.header("Your Preferences")

#     roles = st.text_area("Job Roles (comma-separated)", value=",".join(prefs.get("roles", ["Software Engineer", "Developer"])))
#     locations = st.text_input("Locations (comma-separated)", value=",".join(prefs.get("locations", ["India"])))
#     companies = st.text_area("Companies for Email Scraping (comma-separated)", value=",".join(prefs.get("companies", ["Google", "Microsoft", "TCS", "Infosys", "Wipro"])))
#     followup_days = st.number_input("Follow-up Delay (days)", min_value=1, max_value=30, value=prefs.get("followup_days", 5))

#     desired_count = st.number_input(
#         "Number of Jobs to Fetch",
#         min_value=10,
#         max_value=500,
#         value=prefs.get("desired_count", 100),
#         step=10
#     )

#     easy_apply_only = st.checkbox(
#         "Only show Easy Apply jobs",
#         value=prefs.get("easy_apply_only", True)
#     )

#     if st.button("💾 Save Preferences"):
#         prefs["roles"] = [r.strip() for r in roles.split(",")]
#         prefs["locations"] = [l.strip() for l in locations.split(",")]
#         prefs["companies"] = [c.strip() for c in companies.split(",")]
#         prefs["followup_days"] = followup_days
#         prefs["desired_count"] = desired_count
#         prefs["easy_apply_only"] = easy_apply_only
#         save_preferences(prefs)
#         st.success("✅ Preferences saved!")



# # Action Buttons
# st.header("Actions")

# col1, col2 = st.columns(2)

# with col1:
#     if st.button("🕷️ Crawl LinkedIn Jobs"):
#         with st.spinner("Crawling jobs..."):
#             jobs = crawl_jobs(prefs)
#             if jobs:
#                 os.makedirs("data", exist_ok=True)
#                 jobs_df = pd.DataFrame(jobs)
#                 jobs_df.to_csv("data/latest_jobs.csv", index=False)
#                 st.success(f"✅ Found and saved {len(jobs)} jobs.")
#             else:
#                 st.warning("⚠️ No jobs found or error during crawl.")

# with col2:
#     if st.button("📝 Optimize Resume"):
#         with st.spinner("Optimizing resume..."):
#             optimize_resume(prefs)
#             st.success("✅ Resume optimized!")


# # Action Buttons
# st.header("Actions")

# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.button("🕷️ Crawl LinkedIn Jobs"):
#         with st.spinner("Crawling jobs..."):
#             jobs = crawl_jobs(prefs)
#             if jobs:
#                 os.makedirs("data", exist_ok=True)
#                 jobs_df = pd.DataFrame(jobs)
#                 jobs_df.to_csv("data/latest_jobs.csv", index=False)
#                 st.success(f"✅ Found and saved {len(jobs)} jobs.")
#             else:
#                 st.warning("⚠️ No jobs found or error during crawl.")

# with col2:
#     if st.button("📝 Optimize Resume"):
#         with st.spinner("Optimizing resume..."):
#             optimize_resume(prefs)
#             st.success("✅ Resume optimized!")

# with col3:
#     if st.button("🤖 Auto-Apply to Jobs"):
#         with st.spinner("Applying to jobs..."):
#             csv_path = "data/latest_jobs.csv"
#             if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
#                 try:
#                     jobs_df = pd.read_csv(csv_path)
#                     if not jobs_df.empty:
#                         jobs = jobs_df.to_dict(orient="records")
#                         apply_to_jobs(jobs, prefs)
#                         st.success("✅ Auto-apply completed. Check terminal or logs.")
#                     else:
#                         st.warning("⚠️ CSV file is empty. Try crawling jobs first.")
#                 except Exception as e:
#                     st.error(f"❌ Error reading job file: {e}")
#             else:
#                 st.warning("⚠️ No job data found. Please crawl jobs first.")


# # Job Listings Display
# st.markdown("---")
# st.subheader("📊 Latest Crawled Jobs")

# csv_path = "data/latest_jobs.csv"

# if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
#     try:
#         jobs_df = pd.read_csv(csv_path)
#         if not jobs_df.empty:
#             st.dataframe(jobs_df, use_container_width=True)
#         else:
#             st.info("CSV file is empty. Try crawling jobs again.")
#     except Exception as e:
#         st.error(f"Error reading jobs data: {e}")
# else:
#     st.info("No job data found. Please run a crawl to fetch jobs.")

# # Cold Emails & Follow-up Section
# st.markdown("---")
# col3, col4 = st.columns(2)

# with col3:
#     if st.button("✉️ Send Cold Emails"):
#         with st.spinner("Sending cold emails..."):
#             send_cold_emails(prefs)
#             st.success("✅ Cold emails sent!")

# with col4:
#     if st.button("🔁 Send Follow-ups"):
#         with st.spinner("Sending follow-up emails..."):
#             send_followups()
#             st.success("✅ Follow-up emails sent!")

# # Email Tracker
# st.markdown("---")
# st.subheader("📬 Email Tracker Overview")

# email_tracker_path = "data/email_tracker.csv"
# if os.path.exists(email_tracker_path) and os.path.getsize(email_tracker_path) > 0:
#     try:
#         df = pd.read_csv(email_tracker_path)
#         st.dataframe(df, use_container_width=True)
#     except Exception as e:
#         st.error(f"Error reading email tracker: {e}")
# else:
#     st.info("No emails sent yet.")

# # Footer Tip
# st.markdown("---")
# st.info("💡 Tip: Run `ollama run llama3` before starting the dashboard to enable LLM-powered features.")

# dashboard.py

import sys
import os
import time

# ✅ Ensure correct path to import from parent directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from crawler.job_crawler import crawl_jobs
from apply_tool.auto_apply import apply_to_jobs
from emailer.cold_email_sender import send_cold_emails
from emailer.follow_up_tracker import send_followups
from optimizer.resume_optimizer import optimize_resume
from memory.preference_manager import load_preferences, save_preferences
from utils.llm_client import query_ollama, parse_llm_response
from email_finder.recruiter_email_scraper import find_recruiter_emails

st.set_page_config(page_title="Hypercortex Dashboard", layout="wide")

st.title("🤖 Hypercortex Dashboard")

# Load or initialize user preferences
prefs = load_preferences()

# Model context protocol for using tools
def get_llm_response(messages):
    """
    Sends a list of chat messages to the LLM and returns the response.
    :param messages: List of message dicts, e.g. [{"role": "user", "content": "Hello!"}]
    :return: LLM response string
    """
    return query_ollama(messages)

with st.sidebar:
    st.header("Your Preferences")

    roles = st.text_area("Job Roles (comma-separated)", value=",".join(prefs.get("roles", ["Software Engineer", "Developer"])))
    locations = st.text_input("Locations (comma-separated)", value=",".join(prefs.get("locations", ["India"])))
    companies = st.text_area("Companies for Email Scraping (comma-separated)", value=",".join(prefs.get("companies", ["Google", "Microsoft", "TCS", "Infosys", "Wipro"])))
    followup_days = st.number_input("Follow-up Delay (days)", min_value=1, max_value=30, value=prefs.get("followup_days", 5))

    desired_count = st.number_input(
        "Number of Jobs to Fetch",
        min_value=10,
        max_value=500,
        value=prefs.get("desired_count", 100),
        step=10
    )

    easy_apply_only = st.checkbox(
        "Only show Easy Apply jobs",
        value=prefs.get("easy_apply_only", True)
    )

    if st.button("💾 Save Preferences"):
        prefs["roles"] = [r.strip() for r in roles.split(",")]
        prefs["locations"] = [l.strip() for l in locations.split(",")]
        prefs["companies"] = [c.strip() for c in companies.split(",")]
        prefs["followup_days"] = followup_days
        prefs["desired_count"] = desired_count
        prefs["easy_apply_only"] = easy_apply_only
        save_preferences(prefs)
        st.success("✅ Preferences saved!")


st.subheader("Ask Hypercortex for Specific Work")
user_query = st.text_input("What would you like me to do?", key="llm_query")
if st.button("Submit Query"):
    if user_query:
        print(f"[DEBUG] Received user query: {user_query}")
        
        # # Send query to LLM
        # messages = [{"role": "user", "content": user_query}]
        # llm_response = query_ollama(messages)
        # print(f"[DEBUG] Raw LLM response: {llm_response}")
        
        # # Parse the response
        # parsed_response = parse_llm_response(llm_response)
        # print(f"[DEBUG] Parsed response: {parsed_response}")

        messages = [{"role": "user", "content": user_query}]
        llm_response = query_ollama(messages)

        # ✅ Extract the <think> part from raw LLM output
        raw_content = llm_response.get("message", {}).get("content", "")
        thinking = ""
        if "<think>" in raw_content and "</think>" in raw_content:
            thinking = raw_content.split("<think>")[1].split("</think>")[0].strip()

        # Now parse the tool output (you already have this)
        parsed_response = parse_llm_response(llm_response)

        # ✅ Show response and optionally show "thinking"
        # st.write(parsed_response.get("content", "No response"))

        if thinking:
            with st.expander("🧠 Show Hypercortex's Thinking Process"):
                placeholder = st.empty()
                full_text = ""
                for char in thinking:
                    full_text += char
                    placeholder.markdown(f"```\n{full_text.strip()}\n```")
                    time.sleep(0.01)

        
        if "error" in llm_response:
            st.error(f"Error: {llm_response['error']}")
        elif parsed_response.get("type") == "error":
            st.error(f"Error parsing LLM response: {parsed_response['content']}")
        elif "tool" in parsed_response:
            tool_name = parsed_response["tool"]
            parameters = parsed_response["parameters"]
            print(f"[DEBUG] Tool call detected: {tool_name} with parameters: {parameters}")
            
            if tool_name == "crawl_jobs":
                roles = parameters.get("roles", [])
                if roles:
                    print(f"[DEBUG] Updating preferences with roles: {roles}")
                    prefs["roles"] = roles
                    st.write(f"Searching for jobs with roles: {', '.join(roles)}")
                    jobs = crawl_jobs(prefs)
                    if jobs:
                        st.success(f"Found {len(jobs)} jobs")
                        jobs_df = pd.DataFrame(jobs)
                        jobs_df.to_csv("data/latest_jobs.csv", index=False)
                        st.dataframe(jobs_df)
                    else:
                        st.warning(f"No jobs found for the specified roles")
                else:
                    st.error("No job roles specified in the query")
            
            elif tool_name == "find_recruiter_emails":
                companies = parameters.get("companies", [])
                if not companies:  # If no companies specified in query, use from preferences
                    companies = prefs.get("companies", [])
                
                if companies:
                    print(f"[DEBUG] Starting email scraping for companies: {companies}")
                    try:
                        find_recruiter_emails(companies)
                        st.success(f"Successfully scraped emails for: {', '.join(companies)}")
                        # Display the results from the CSV file
                        try:
                            df = pd.read_csv("data/recruiter_emails.csv")
                            st.dataframe(df)
                        except Exception as e:
                            print(f"[ERROR] Failed to read CSV file: {str(e)}")
                            st.warning("Emails were scraped but couldn't display results")
                    except Exception as e:
                        print(f"[ERROR] Email scraping failed: {str(e)}")
                        st.error(f"Failed to scrape emails: {str(e)}")
                else:
                    st.error("No companies specified in preferences or query")
            
            # elif tool_name == "send_cold_emails":
            #     description = parameters.get("description", "")
            #     roles = parameters.get("roles", [])
                
            #     if description and roles:
            #         print(f"[DEBUG] Starting cold email sending with description: {description}")
            #         print(f"[DEBUG] Target roles: {roles}")
                    
            #         # Update preferences with the new description and roles
            #         prefs["description"] = description
            #         prefs["roles"] = roles
            #         save_preferences(prefs)
                    
            #         try:
            #             send_cold_emails(prefs)
            #             st.success("✅ Cold emails sent successfully!")
                        
            #             # Display the email tracker
            #             try:
            #                 df = pd.read_csv("data/email_tracker.csv")
            #                 st.dataframe(df)
            #             except Exception as e:
            #                 print(f"[ERROR] Failed to read email tracker: {str(e)}")
            #                 st.warning("Emails were sent but couldn't display tracker")
            #         except Exception as e:
            #             print(f"[ERROR] Cold email sending failed: {str(e)}")
            #             st.error(f"Failed to send cold emails: {str(e)}")
            #     else:
            #         st.error("Missing required parameters: description or roles")
            elif tool_name == "send_cold_emails":
                prefs_data = parameters.get("prefs", {})
                description = prefs_data.get("description", "")
                roles = prefs_data.get("roles", [])
                
                if description and roles:
                    print(f"[DEBUG] Starting cold email sending with description: {description}")
                    print(f"[DEBUG] Target roles: {roles}")
                    
                    # Update preferences with the new description and roles
                    prefs["description"] = description
                    prefs["roles"] = roles
                    save_preferences(prefs)
                    
                    try:
                        send_cold_emails(prefs)
                        st.success("✅ Cold emails sent successfully!")
                        
                        # Display the email tracker
                        try:
                            df = pd.read_csv("data/email_tracker.csv")
                            st.dataframe(df)
                        except Exception as e:
                            print(f"[ERROR] Failed to read email tracker: {str(e)}")
                            st.warning("Emails were sent but couldn't display tracker")
                    except Exception as e:
                        print(f"[ERROR] Cold email sending failed: {str(e)}")
                        st.error(f"Failed to send cold emails: {str(e)}")
                else:
                    st.error("Missing required parameters: prefs.description and prefs.roles")

            
            else:
                st.error(f"Unknown tool: {tool_name}")
        else:
            st.write(parsed_response.get("content", "No response from LLM"))
    else:
        st.warning("Please enter a query.")

st.markdown("---")

# Top Action Buttons
st.header("🔧 Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🕷️ Crawl LinkedIn Jobs"):
        with st.spinner("Crawling jobs..."):
            jobs = crawl_jobs(prefs)
            if jobs:
                os.makedirs("data", exist_ok=True)
                jobs_df = pd.DataFrame(jobs)
                jobs_df.to_csv("data/latest_jobs.csv", index=False)
                st.success(f"✅ Found and saved {len(jobs)} jobs.")
            else:
                st.warning("⚠️ No jobs found or crawl failed.")

# with col2:
#     if st.button("📝 Optimize Resume"):
#         with st.spinner("Optimizing resume..."):
#             optimize_resume(prefs)
#             st.success("✅ Resume optimized!")



# Job Listings
st.markdown("---")
st.subheader("📊 Latest Crawled Jobs")

csv_path = "data/latest_jobs.csv"
if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    try:
        jobs_df = pd.read_csv(csv_path)
        if not jobs_df.empty:
            st.dataframe(jobs_df, use_container_width=True)
        else:
            st.info("CSV is empty. Crawl again.")
    except Exception as e:
        st.error(f"❌ Failed to load jobs: {e}")
else:
    st.info("No job data found. Run a crawl.")

# Email Tools
st.markdown("---")
st.subheader("📨 Cold Email Tools")

col4, col5 = st.columns(2)

with col4:
    if st.button("✉️ Send Cold Emails"):
        with st.spinner("Sending..."):
            send_cold_emails(prefs)
            st.success("✅ Cold emails sent!")



# Email Tracker
st.markdown("---")
st.subheader("📬 Email Tracker Overview")

tracker_path = "data/email_tracker.csv"
if os.path.exists(tracker_path) and os.path.getsize(tracker_path) > 0:
    try:
        df = pd.read_csv(tracker_path)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error reading tracker: {e}")
else:
    st.info("No emails tracked yet.")

# Footer Tip
st.markdown("---")
st.info("💡 Tip: Make sure `ollama run llama3` is running before using LLM features like Auto-Apply.")

st.markdown("---")


