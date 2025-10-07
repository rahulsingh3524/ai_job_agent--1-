import os
import csv
import time
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_google(company_name):
    """Use SerpAPI to get recruiter-related pages."""
    params = {
        "engine": "google",
        "q": f"{company_name} recruiter email site:linkedin.com OR site:{company_name.lower()}.com",
        "api_key": SERPAPI_KEY,
        "num": 10
    }

    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        results = response.json()
        links = [r['link'] for r in results.get("organic_results", [])]
        return links
    else:
        print(f"Failed to fetch search results for {company_name}")
        return []

def extract_emails_from_url(url):
    """Scrape a URL for email addresses."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.text))
            return list(emails)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return []

def find_recruiter_emails(companies, output_file="data/recruiter_emails.csv"):
    """
    Find recruiter emails for specified companies and save to CSV.
    Returns True if successful, False otherwise.
    """
    try:
        os.makedirs("data", exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Company", "Source URL", "Email"])

            for company in companies:
                print(f"🔍 Searching for recruiter emails at: {company}")
                urls = search_google(company)

                for url in urls:
                    emails = extract_emails_from_url(url)
                    for email in emails:
                        writer.writerow([company, url, email])
                        print(f"📧 Found: {email} at {url}")
                    time.sleep(1)  # Be nice to websites

        print(f"\n✅ Finished. Results saved to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error in find_recruiter_emails: {str(e)}")
        return False

# if __name__ == "__main__":
#     companies = [
#         "Google",
#         "Microsoft",
#         "Infosys",
#         "TCS",
#         "Wipro"
#     ]
#     find_recruiter_emails(companies)
