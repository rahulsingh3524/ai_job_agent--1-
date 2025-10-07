# # # import os
# # # import requests
# # # from bs4 import BeautifulSoup
# # # from dotenv import load_dotenv
# # # import datetime

# # # load_dotenv()

# # # # Constants for LinkedIn job search URL construction
# # # BASE_URL = "https://www.linkedin.com/jobs/search/"

# # # def build_search_url(role, location, days_posted=7):
# # #     """
# # #     Build LinkedIn job search URL with filters:
# # #     - role (job title)
# # #     - location
# # #     - days_posted: filter recent jobs (e.g., last 7 days)
# # #     """
# # #     params = {
# # #         'keywords': role,
# # #         'location': location,
# # #         'f_TPR': f'r{days_posted}',  # time posted range filter (r7 means last 7 days)
# # #         'f_E': '2',  # Full-time jobs (example filter)
# # #         'trk': 'public_jobs_jobs-search-bar_search-submit',
# # #     }
# # #     # Construct query string
# # #     query = '&'.join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
# # #     return f"{BASE_URL}?{query}"

# # # def crawl_jobs(preferences):
# # #     """
# # #     Crawl LinkedIn jobs for all roles in preferences and return a list of jobs
# # #     preferences = {
# # #         'roles': [...],
# # #         'location': 'India',
# # #         'days_posted': 7
# # #     }
# # #     """
# # #     roles = preferences.get('roles', [])
# # #     location = preferences.get('location', 'India')
# # #     days_posted = preferences.get('days_posted', 7)

# # #     all_jobs = []

# # #     headers = {
# # #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
# # #                       ' Chrome/91.0.4472.124 Safari/537.36'
# # #     }

# # #     for role in roles:
# # #         url = build_search_url(role, location, days_posted)
# # #         print(f"Crawling jobs for role '{role}' at '{location}' - URL: {url}")
# # #         response = requests.get(url, headers=headers)
# # #         if response.status_code != 200:
# # #             print(f"Failed to fetch jobs for {role}. Status Code: {response.status_code}")
# # #             continue

# # #         soup = BeautifulSoup(response.text, 'html.parser')

# # #         # LinkedIn dynamically loads jobs via JS, so static scraping may be limited
# # #         # Here, we attempt to scrape job cards from the static content (may need Selenium for full support)
# # #         job_cards = soup.find_all('li', {'class': 'jobs-search-results__list-item'})

# # #         for card in job_cards:
# # #             title = card.find('h3')
# # #             company = card.find('h4')
# # #             location_elem = card.find('span', {'class': 'job-result-card__location'})
# # #             date_posted = card.find('time')

# # #             job = {
# # #                 'title': title.get_text(strip=True) if title else None,
# # #                 'company': company.get_text(strip=True) if company else None,
# # #                 'location': location_elem.get_text(strip=True) if location_elem else None,
# # #                 'date_posted': date_posted.get_text(strip=True) if date_posted else None,
# # #                 'url': card.find('a', href=True)['href'] if card.find('a', href=True) else None
# # #             }
# # #             all_jobs.append(job)

# # #     print(f"Total jobs found: {len(all_jobs)}")
# # #     return all_jobs


# # # crawler/job_crawler.py

# # """
# # LinkedIn Job Crawler
# # --------------------
# # Crawls LinkedIn for job postings based on saved preferences (roles, location).
# # Filters by 'Posted in past 24 hours'.
# # Returns a list of job postings (title, company, link, location, time).
# # """

# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.chrome.service import Service
# # import time
# # import os
# # from dotenv import load_dotenv
# # load_dotenv()

# # def crawl_jobs(preferences):
# #     roles = preferences.get("roles", [])
# #     location = preferences.get("location", "India")
# #     email = os.getenv("LINKEDIN_EMAIL")
# #     password = os.getenv("LINKEDIN_PASSWORD")
# #     print("LinkedIn Email:", email)
# #     print("LinkedIn Password:", password)

# #     # Headless Chrome setup
# #     options = Options()
# #     options.add_argument("--headless")
# #     options.add_argument("--disable-gpu")
# #     driver = webdriver.Chrome(options=options)

# #     # Log in to LinkedIn
# #     driver.get("https://www.linkedin.com/login")
# #     time.sleep(2)
# #     driver.find_element(By.ID, "username").send_keys(email)
# #     driver.find_element(By.ID, "password").send_keys(password)
# #     driver.find_element(By.XPATH, "//button[@type='submit']").click()
# #     time.sleep(3)

# #     all_jobs = []

# #     for role in roles:
# #         query = role.replace(" ", "%20")
# #         search_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={location}&f_TPR=r86400"
# #         driver.get(search_url)
# #         time.sleep(3)

# #         job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")
# #         for job in job_cards:
# #             try:
# #                 title = job.find_element(By.CLASS_NAME, "job-card-list__title").text
# #                 company = job.find_element(By.CLASS_NAME, "job-card-container__company-name").text
# #                 location = job.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
# #                 link = job.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")
# #                 time_posted = job.find_element(By.CLASS_NAME, "job-card-container__listed-time").text
# #                 all_jobs.append({
# #                     "title": title,
# #                     "company": company,
# #                     "location": location,
# #                     "link": link,
# #                     "posted": time_posted
# #                 })
# #             except Exception as e:
# #                 print("Error reading job card:", e)

# #     driver.quit()
# #     return all_jobs


# import os
# import time
# import csv
# from dotenv import load_dotenv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

# load_dotenv()

# def crawl_jobs(preferences):
#     roles = preferences.get("roles", [])
#     location = preferences.get("location", "India")
#     email = os.getenv("LINKEDIN_EMAIL")
#     password = os.getenv("LINKEDIN_PASSWORD")

#     # Setup headless Chrome
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     driver = webdriver.Chrome(options=options)

#     # Log in to LinkedIn
#     driver.get("https://www.linkedin.com/login")
#     time.sleep(2)
#     driver.find_element(By.ID, "username").send_keys(email)
#     driver.find_element(By.ID, "password").send_keys(password)
#     driver.find_element(By.XPATH, "//button[@type='submit']").click()
#     time.sleep(3)

#     all_jobs = []

#     for role in roles:
#         query = role.replace(" ", "%20")
#         search_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={location}&f_TPR=r86400"
#         driver.get(search_url)
#         time.sleep(3)

#         job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")
#         for job in job_cards:
#             try:
#                 title = job.find_element(By.CLASS_NAME, "job-card-list__title").text
#                 company = job.find_element(By.CLASS_NAME, "job-card-container__company-name").text
#                 location = job.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
#                 link = job.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")
#                 time_posted = job.find_element(By.CLASS_NAME, "job-card-container__listed-time").text
#                 all_jobs.append({
#                     "title": title,
#                     "company": company,
#                     "location": location,
#                     "link": link,
#                     "posted": time_posted
#                 })
#             except Exception as e:
#                 print("Error reading job card:", e)

#     driver.quit()

#     # ✅ Save to CSV
#     save_path = os.path.join("data", "linkedin_jobs.csv")
#     os.makedirs("data", exist_ok=True)

#     with open(save_path, mode="w", newline="", encoding="utf-8") as csvfile:
#         fieldnames = ["title", "company", "location", "link", "posted"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for job in all_jobs:
#             writer.writerow(job)

#     print(f"✅ Total jobs saved: {len(all_jobs)} to '{save_path}'")
#     return all_jobs


# # crawler/job_crawler.py

# import os
# import time
# import csv
# from dotenv import load_dotenv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# load_dotenv()

# def crawl_jobs(preferences):
#     roles = preferences.get("roles", [])
#     locations = preferences.get("locations", ["India"])
#     email = os.getenv("LINKEDIN_EMAIL")
#     password = os.getenv("LINKEDIN_PASSWORD")

#     if not email or not password:
#         raise Exception("⚠️ LinkedIn credentials not found in .env file!")

#     # Setup headless Chrome
#     options = Options()
#     # options.add_argument("--headless=new")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--window-size=1920,1080")

#     driver = webdriver.Chrome(options=options)

#     # Login to LinkedIn
#     try:
#         driver.get("https://www.linkedin.com/login")
#         time.sleep(2)
#         driver.find_element(By.ID, "username").send_keys(email)
#         driver.find_element(By.ID, "password").send_keys(password)
#         driver.find_element(By.XPATH, "//button[@type='submit']").click()
#         time.sleep(3)
#     except Exception as e:
#         driver.quit()
#         raise Exception("❌ LinkedIn login failed:", e)

#     all_jobs = []
#     seen_links = set()

#     for role in roles:
#         for location in locations:
#             query = role.replace(" ", "%20")
#             loc = location.replace(" ", "%20")
#             search_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}&f_TPR=r86400"
#             driver.get(search_url)
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)  # let additional jobs load

#             # Wait for job listings to load
#             try:
#                 wait = WebDriverWait(driver, 10)
#                 job_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.jobs-search__results-list li")))
#             except TimeoutException:
#                 print(f"❌ No jobs found for role '{role}' in location '{location}'.")
#                 continue

#             job_cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")

#             for job in job_cards:
#                 try:
#                     title_el = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title")
#                     title = title_el.text
#                     link = title_el.get_attribute("href")

#                     if link in seen_links:
#                         continue
#                     seen_links.add(link)

#                     company = job.find_element(By.CLASS_NAME, "job-card-container__company-name").text
#                     location_text = job.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
#                     posted = job.find_element(By.CLASS_NAME, "job-card-container__listed-time").text

#                     all_jobs.append({
#                         "title": title,
#                         "company": company,
#                         "location": location_text,
#                         "link": link,
#                         "posted": posted
#                     })

#                 except NoSuchElementException:
#                     continue
#                 except Exception as e:
#                     print("⚠️ Error reading job card:", e)

#     driver.quit()

#     # Save to CSV
#     os.makedirs("data", exist_ok=True)
#     save_path = os.path.join("data", "latest_jobs.csv")

#     with open(save_path, mode="w", newline="", encoding="utf-8") as csvfile:
#         fieldnames = ["title", "company", "location", "link", "posted"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for job in all_jobs:
#             writer.writerow(job)

#     print(f"✅ {len(all_jobs)} jobs saved to {save_path}")
#     return all_jobs



# import os
# import time
# import csv
# from dotenv import load_dotenv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# load_dotenv()

# def crawl_jobs(preferences):
#     roles = preferences.get("roles", [])
#     locations = preferences.get("locations", ["India"])
#     email = os.getenv("LINKEDIN_EMAIL")
#     password = os.getenv("LINKEDIN_PASSWORD")

#     if not email or not password:
#         raise Exception("⚠️ LinkedIn credentials not found in .env file!")

#     # Setup Chrome
#     options = Options()
#     # options.add_argument("--headless=new")  # Uncomment to run headless
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--window-size=1920,1080")

#     driver = webdriver.Chrome(options=options)

#     # Login to LinkedIn
#     try:
#         driver.get("https://www.linkedin.com/login")
#         time.sleep(2)
#         driver.find_element(By.ID, "username").send_keys(email)
#         driver.find_element(By.ID, "password").send_keys(password)
#         driver.find_element(By.XPATH, "//button[@type='submit']").click()
#         time.sleep(3)
#     except Exception as e:
#         driver.quit()
#         raise Exception("❌ LinkedIn login failed:", e)

#     all_jobs = []
#     seen_links = set()

#     for role in roles:
#         for location in locations:
#             query = role.replace(" ", "%20")
#             loc = location.replace(" ", "%20")
#             search_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}&f_TPR=r86400"
#             driver.get(search_url)
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)  # let jobs load

#             try:
#                 wait = WebDriverWait(driver, 10)
#                 wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.jobs-search__results-list li")))
#             except TimeoutException:
#                 print(f"❌ No jobs found for '{role}' in '{location}'.")
#                 continue

#             job_cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")

#             for job in job_cards:
#                 try:
#                     title_el = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title")
#                     title = title_el.text.strip()
#                     link = title_el.get_attribute("href")

#                     if link in seen_links:
#                         continue
#                     seen_links.add(link)

#                     # Robust selectors
#                     company_el = job.find_element(By.CSS_SELECTOR, ".job-card-container__company-name")
#                     company = company_el.text.strip() if company_el else "N/A"

#                     metadata_items = job.find_elements(By.CSS_SELECTOR, ".job-card-container__metadata-item")
#                     location_text = metadata_items[0].text.strip() if len(metadata_items) > 0 else "N/A"

#                     posted_el = job.find_element(By.CSS_SELECTOR, ".job-card-container__listed-time")
#                     posted = posted_el.text.strip() if posted_el else "N/A"

#                     all_jobs.append({
#                         "title": title,
#                         "company": company,
#                         "location": location_text,
#                         "link": link,
#                         "posted": posted
#                     })

#                     print(f"📄 Job scraped: {title} at {company} [{location_text}] – {posted}")

#                 except NoSuchElementException as e:
#                     print(f"⚠️ Missing element in job card: {e}")
#                     continue
#                 except Exception as e:
#                     print(f"⚠️ Unexpected error reading job card: {e}")

#     driver.quit()

#     # Save to CSV
#     os.makedirs("data", exist_ok=True)
#     save_path = os.path.join("data", "latest_jobs.csv")

#     with open(save_path, mode="w", newline="", encoding="utf-8") as csvfile:
#         fieldnames = ["title", "company", "location", "link", "posted"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for job in all_jobs:
#             writer.writerow(job)

#     print(f"✅ {len(all_jobs)} jobs saved to {save_path}")
#     return all_jobs




# -------------------------------------------------------------------

# # crawler/job_crawler.py

# import os
# import csv
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import quote
# from dotenv import load_dotenv

# load_dotenv()


# def fetch_jobs_via_api(query, location, max_pages=3, results_per_page=25):
#     all_jobs = []
#     seen_links = set()

#     for page in range(max_pages):
#         offset = page * results_per_page
#         url = (
#             "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
#             f"?keywords={quote(query)}&location={quote(location)}&start={offset}&f_TPR=r86400"
#         )

#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                           '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
#         }

#         try:
#             response = requests.get(url, headers=headers)
#             if response.status_code != 200:
#                 print(f"⚠️ Failed to fetch jobs from LinkedIn API. Status code: {response.status_code}")
#                 break

#             soup = BeautifulSoup(response.text, 'html.parser')
#             job_cards = soup.find_all('li')

#             if not job_cards:
#                 print(f"ℹ️ No more jobs found for '{query}' in '{location}'.")
#                 break

#             for card in job_cards:
#                 try:
#                     title_el = card.find('a', class_='job-card-list__title')
#                     company_el = card.find('a', class_='job-card-container__company-name')
#                     location_el = card.find('li', class_='job-card-container__metadata-item')
#                     time_el = card.find('time')

#                     title = title_el.get_text(strip=True) if title_el else "N/A"
#                     company = company_el.get_text(strip=True) if company_el else "N/A"
#                     job_location = location_el.get_text(strip=True) if location_el else "N/A"
#                     posted = time_el.get_text(strip=True) if time_el else "N/A"
#                     link = "https://www.linkedin.com" + title_el['href'] if title_el and 'href' in title_el.attrs else "N/A"

#                     if link in seen_links:
#                         continue
#                     seen_links.add(link)

#                     all_jobs.append({
#                         "title": title,
#                         "company": company,
#                         "location": job_location,
#                         "posted": posted,
#                         "link": link
#                     })
#                 except Exception as e:
#                     print("⚠️ Error parsing a job card:", e)
#                     continue

#         except requests.RequestException as e:
#             print(f"❌ Network error while fetching jobs: {e}")
#             break

#     return all_jobs


# def crawl_jobs(preferences):
#     roles = preferences.get("roles", [])
#     locations = preferences.get("locations", ["India"])

#     all_crawled_jobs = []

#     for role in roles:
#         for location in locations:
#             print(f"🔍 Searching for '{role}' jobs in '{location}'...")
#             jobs = fetch_jobs_via_api(role, location)
#             print(f"✅ Found {len(jobs)} jobs for '{role}' in '{location}'.")
#             all_crawled_jobs.extend(jobs)

#     # Save to CSV
#     os.makedirs("data", exist_ok=True)
#     save_path = os.path.join("data", "latest_jobs.csv")

#     with open(save_path, mode="w", newline="", encoding="utf-8") as csvfile:
#         fieldnames = ["title", "company", "location", "posted", "link"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for job in all_crawled_jobs:
#             writer.writerow(job)

#     print(f"\n📝 {len(all_crawled_jobs)} total jobs saved to {save_path}")
#     return all_crawled_jobs



# -----------------------------------------------


# import os
# import csv
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import quote
# from dotenv import load_dotenv

# load_dotenv()

# def fetch_jobs_via_api(query, location, max_pages=3, results_per_page=25):
#     all_jobs = []
#     seen_links = set()

#     headers = {
#         'User-Agent': (
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#             '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
#         )
#     }

#     for page in range(max_pages):
#         offset = page * results_per_page
#         url = (
#             "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
#             f"?keywords={quote(query)}&location={quote(location)}"
#             f"&start={offset}&f_TPR=r86400"
#         )
#         resp = requests.get(url, headers=headers)
#         if resp.status_code != 200:
#             print(f"⚠️ Status {resp.status_code} fetching {url}")
#             break

#         soup = BeautifulSoup(resp.text, 'html.parser')
#         cards = soup.find_all('li')

#         if not cards:
#             break

#         for c in cards:
#             title_el = c.find('h3', class_='base-search-card__title')
#             company_el = c.find('h4', class_='base-search-card__subtitle')
#             location_el = c.find('span', class_='job-search-card__location')
#             link_el = c.find('a', class_='base-card__full-link')
#             time_el = c.find('time')

#             title = title_el.get_text(strip=True) if title_el else None
#             company = company_el.get_text(strip=True) if company_el else None
#             job_loc = location_el.get_text(strip=True) if location_el else None
#             posted = time_el.get_text(strip=True) if time_el else None
#             link = link_el['href'] if link_el and link_el.has_attr('href') else None

#             if not link or link in seen_links:
#                 continue
#             seen_links.add(link)

#             all_jobs.append({
#                 'title': title,
#                 'company': company,
#                 'location': job_loc,
#                 'posted': posted,
#                 'link': link
#             })
#             print(f"📄 Scraped: {title} at {company} [{job_loc}]")

#     return all_jobs

# def crawl_jobs(preferences):
#     roles = preferences.get('roles', [])
#     locations = preferences.get('locations', ['India'])
#     all_jobs = []

#     for role in roles:
#         for loc in locations:
#             print(f"🔍 Searching '{role}' in '{loc}'...")
#             jobs = fetch_jobs_via_api(role, loc)
#             print(f"✅ Found {len(jobs)} jobs for '{role}' in '{loc}'.")
#             all_jobs.extend(jobs)

#     os.makedirs('data', exist_ok=True)
#     path = os.path.join('data', 'latest_jobs.csv')
#     with open(path, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=['title','company','location','posted','link'])
#         writer.writeheader()
#         writer.writerows(all_jobs)

#     print(f"💾 Saved {len(all_jobs)} jobs to {path}")
#     return all_jobs


# -------------------------------------------------------------


# import os
# import csv
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import quote
# from dotenv import load_dotenv

# load_dotenv()

# # Constants
# DESIRED_COUNT = 100  # ← you asked to fix this in code
# RESULTS_PER_PAGE = 25

# def fetch_jobs_via_api(query, location):
#     all_jobs = []
#     seen_links = set()

#     headers = {
#         'User-Agent': (
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#             '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
#         )
#     }

#     page = 0
#     while len(all_jobs) < DESIRED_COUNT:
#         offset = page * RESULTS_PER_PAGE
#         url = (
#             "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
#             f"?keywords={quote(query)}&location={quote(location)}"
#             f"&start={offset}&f_TPR=r86400"
#         )
#         resp = requests.get(url, headers=headers)
#         if resp.status_code != 200:
#             print(f"⚠️ Status {resp.status_code} fetching page {page}")
#             break

#         soup = BeautifulSoup(resp.text, 'html.parser')
#         cards = soup.find_all('li')

#         if not cards:
#             print("ℹ️ No more job cards found. Stopping.")
#             break

#         for c in cards:
#             title_el = c.find('h3', class_='base-search-card__title')
#             company_el = c.find('h4', class_='base-search-card__subtitle')
#             location_el = c.find('span', class_='job-search-card__location')
#             link_el = c.find('a', class_='base-card__full-link')
#             time_el = c.find('time')

#             title = title_el.get_text(strip=True) if title_el else None
#             company = company_el.get_text(strip=True) if company_el else None
#             job_loc = location_el.get_text(strip=True) if location_el else None
#             posted = time_el.get_text(strip=True) if time_el else None
#             link = link_el['href'] if link_el and link_el.has_attr('href') else None

#             if not link or link in seen_links:
#                 continue
#             seen_links.add(link)

#             all_jobs.append({
#                 'title': title,
#                 'company': company,
#                 'location': job_loc,
#                 'posted': posted,
#                 'link': link
#             })
#             print(f"📄 [{len(all_jobs)}] {title} at {company} [{job_loc}]")

#             if len(all_jobs) >= DESIRED_COUNT:
#                 break

#         page += 1

#     return all_jobs

# def crawl_jobs():
#     roles = ["Java Developer", "Software Engineer"]  # you can change these
#     locations = ["India"]                            # and these
#     all_jobs = []

#     for role in roles:
#         for loc in locations:
#             print(f"🔍 Searching '{role}' in '{loc}'...")
#             jobs = fetch_jobs_via_api(role, loc)
#             print(f"✅ Found {len(jobs)} jobs for '{role}' in '{loc}'.")
#             all_jobs.extend(jobs)

#     os.makedirs('data', exist_ok=True)
#     path = os.path.join('data', 'latest_jobs.csv')
#     with open(path, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=['title','company','location','posted','link'])
#         writer.writeheader()
#         writer.writerows(all_jobs)

#     print(f"💾 Saved {len(all_jobs)} jobs to {path}")
#     return all_jobs

# # Optional run trigger
# if __name__ == "__main__":
#     crawl_jobs()


# -------------------------------------------------------


# crawler/job_crawler.py

import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

RESULTS_PER_PAGE = 25  # LinkedIn API paginates this way

# # def fetch_jobs_via_api(query, location, desired_count):
#     all_jobs = []
#     seen_links = set()
#     headers = {
#         'User-Agent': (
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#             '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
#         )
#     }

#     page = 0
#     while len(all_jobs) < desired_count:
#         offset = page * RESULTS_PER_PAGE
#         url = (
#             "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
#             f"?keywords={quote(query)}&location={quote(location)}"
#             f"&start={offset}&f_TPR=r86400"
#         )

#         resp = requests.get(url, headers=headers)
#         if resp.status_code != 200:
#             print(f"⚠️ Status {resp.status_code} fetching page {page} for {query} in {location}")
#             break

#         soup = BeautifulSoup(resp.text, 'html.parser')
#         cards = soup.find_all('li')

#         if not cards:
#             print("ℹ️ No more job cards found. Stopping.")
#             break

#         for c in cards:
#             title_el = c.find('h3', class_='base-search-card__title')
#             company_el = c.find('h4', class_='base-search-card__subtitle')
#             location_el = c.find('span', class_='job-search-card__location')
#             link_el = c.find('a', class_='base-card__full-link')
#             time_el = c.find('time')

#             title = title_el.get_text(strip=True) if title_el else "N/A"
#             company = company_el.get_text(strip=True) if company_el else "N/A"
#             job_loc = location_el.get_text(strip=True) if location_el else "N/A"
#             posted = time_el.get_text(strip=True) if time_el else "N/A"
#             link = link_el['href'] if link_el and link_el.has_attr('href') else "N/A"

#             if link == "N/A" or link in seen_links:
#                 continue
#             seen_links.add(link)

#             all_jobs.append({
#                 'title': title,
#                 'company': company,
#                 'location': job_loc,
#                 'posted': posted,
#                 'link': link
#             })
#             print(f"📄 [{len(all_jobs)}] {title} at {company} [{job_loc}]")

#             if len(all_jobs) >= desired_count:
#                 break

#         page += 1

#     return all_jobs

# def fetch_jobs_via_api(query, location, desired_count=100, easy_apply_only=True):
#     all_jobs = []
#     seen_links = set()
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
#           '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
#     }

#     page = 0
#     RESULTS_PER_PAGE = 25

#     while len(all_jobs) < desired_count:
#         offset = page * RESULTS_PER_PAGE
#         url = (
#             "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
#             f"?keywords={quote(query)}&location={quote(location)}&start={offset}&f_TPR=r86400"
#         )

#         resp = requests.get(url, headers=headers)
#         if resp.status_code != 200:
#             print(f"⚠️ Error {resp.status_code} on page {page}")
#             break

#         soup = BeautifulSoup(resp.text, 'html.parser')
#         cards = soup.find_all('li')
#         if not cards:
#             break

#         for card in cards:
#             # Check if "Easy Apply" is present
#             if easy_apply_only:
#                 easy_apply_badge = card.find('span', class_='apply-method')
#                 if not easy_apply_badge or 'Easy Apply' not in easy_apply_badge.get_text():
#                     continue

#             title = card.find('h3', class_='base-search-card__title')
#             company = card.find('h4', class_='base-search-card__subtitle')
#             location_el = card.find('span', class_='job-search-card__location')
#             link_el = card.find('a', class_='base-card__full-link')
#             posted = card.find('time')

#             job = {
#                 'title': title.get_text(strip=True) if title else 'N/A',
#                 'company': company.get_text(strip=True) if company else 'N/A',
#                 'location': location_el.get_text(strip=True) if location_el else 'N/A',
#                 'posted': posted.get_text(strip=True) if posted else 'N/A',
#                 'link': link_el['href'] if link_el and link_el.has_attr('href') else 'N/A'
#             }

#             if job['link'] in seen_links:
#                 continue

#             seen_links.add(job['link'])
#             all_jobs.append(job)
#             print(f"📄 [{len(all_jobs)}] {job['title']} at {job['company']}")

#             if len(all_jobs) >= desired_count:
#                 break

#         page += 1

#     return all_jobs

def fetch_jobs_via_api(query, location, desired_count=100, easy_apply_only=True):
    all_jobs = []
    seen_links = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    page = 0
    RESULTS_PER_PAGE = 25

    while len(all_jobs) < desired_count:
        offset = page * RESULTS_PER_PAGE

        # 🔀 Add correct filters based on Easy Apply toggle
        extra_filters = "&f_AL=true&f_E=2" if easy_apply_only else ""

        url = (
            "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
            f"?keywords={quote(query)}&location={quote(location)}&start={offset}&f_TPR=r86400"
            f"{extra_filters}"
        )

        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"⚠️ Error {resp.status_code} on page {page}")
            break

        soup = BeautifulSoup(resp.text, 'html.parser')
        cards = soup.find_all('li')
        if not cards:
            print("ℹ️ No more jobs found.")
            break

        for card in cards:
            title = card.find('h3', class_='base-search-card__title')
            company = card.find('h4', class_='base-search-card__subtitle')
            location_el = card.find('span', class_='job-search-card__location')
            link_el = card.find('a', class_='base-card__full-link')
            posted = card.find('time')

            job = {
                'title': title.get_text(strip=True) if title else 'N/A',
                'company': company.get_text(strip=True) if company else 'N/A',
                'location': location_el.get_text(strip=True) if location_el else 'N/A',
                'posted': posted.get_text(strip=True) if posted else 'N/A',
                'link': link_el['href'] if link_el and link_el.has_attr('href') else 'N/A'
            }

            if job['link'] in seen_links:
                continue

            seen_links.add(job['link'])
            all_jobs.append(job)
            print(f"📄 [{len(all_jobs)}] {job['title']} at {job['company']}")

            if len(all_jobs) >= desired_count:
                break

        page += 1

    return all_jobs



def crawl_jobs(preferences):
    """
    Crawl LinkedIn jobs based on preferences.
    preferences = {
        'roles': ['Software Engineer', 'UI/UX Designer'],  # List of roles to search for
        'locations': ['India'],  # List of locations
        'desired_count': 100,  # Number of jobs to fetch per role
        'easy_apply_only': True  # Whether to only show Easy Apply jobs
    }
    """
    # Extract parameters from preferences
    roles = preferences.get('roles', [])
    locations = preferences.get('locations', ['India'])
    desired_count = preferences.get('desired_count', 100)
    easy_apply_only = preferences.get('easy_apply_only', True)

    # If roles is a string (from LLM), convert to list
    if isinstance(roles, str):
        roles = [roles]

    all_jobs = []
    seen_links = set()

    for role in roles:
        for location in locations:
            print(f"\n🔍 Searching '{role}' in '{location}' for {desired_count} jobs (Easy Apply: {easy_apply_only})...")
            jobs = fetch_jobs_via_api(role, location, desired_count, easy_apply_only)
            print(f"✅ Found {len(jobs)} jobs for '{role}' in '{location}'")
            
            # Filter out duplicates
            for job in jobs:
                if job['link'] not in seen_links:
                    seen_links.add(job['link'])
                    all_jobs.append(job)

    # Save to CSV
    os.makedirs('data', exist_ok=True)
    path = os.path.join('data', 'latest_jobs.csv')
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'company', 'location', 'posted', 'link'])
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"💾 Saved {len(all_jobs)} total jobs to {path}")
    return all_jobs


def crawl_jobs(preferences):
    roles = preferences.get("roles", ["Software Engineer", "Java Developer"])
    locations = preferences.get("locations", ["India"])
    desired_count = preferences.get("desired_count", 100)
    easy_apply_only = preferences.get("easy_apply_only", True)  # ✅ Extract this from prefs

    all_jobs = []

    for role in roles:
        for loc in locations:
            print(f"\n🔍 Searching '{role}' in '{loc}' for {desired_count} jobs (Easy Apply: {easy_apply_only})...")
            jobs = fetch_jobs_via_api(role, loc, desired_count, easy_apply_only)  # ✅ Pass easy_apply_only
            print(f"✅ Fetched {len(jobs)} jobs for '{role}' in '{loc}'")
            all_jobs.extend(jobs)

    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", "latest_jobs.csv")
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'company', 'location', 'posted', 'link'])
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"💾 Saved {len(all_jobs)} total jobs to {path}")
    return all_jobs
