
# auto_apply_bot.py
# 🚀 Automatically applies to LinkedIn jobs using Selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv

load_dotenv()

class LinkedInAutoApplyBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")

    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        self.driver.find_element(By.ID, "username").send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

    def apply_to_job(self, job_url):
        self.driver.get(job_url)
        time.sleep(3)
        try:
            easy_apply = self.driver.find_element(By.XPATH, "//button[contains(text(),'Easy Apply')]")
            easy_apply.click()
            time.sleep(2)
            submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit.click()
            print(f"✅ Applied to {job_url}")
        except Exception as e:
            print(f"❌ Could not apply to {job_url}: {e}")

    def close(self):
        self.driver.quit()
