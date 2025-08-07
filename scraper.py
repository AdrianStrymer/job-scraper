from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import urllib.parse

def scrape_page(driver, writer):
    job_cards = driver.find_elements(By.TAG_NAME, 'article')
    for job in job_cards:
        try:
            title = job.find_element(By.CSS_SELECTOR, '[data-testid="job-item-title"]').text
            company = job.find_element(By.CSS_SELECTOR, '[data-at="job-item-company-name"]').text
            location = job.find_element(By.CSS_SELECTOR, '[data-at="job-item-location"]').text

            link_elem = job.find_element(By.CSS_SELECTOR, '[data-testid="job-item-title"]')
            job_url = link_elem.get_attribute('href')

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(job_url)
            time.sleep(2)

            try:
                full_desc_elem = driver.find_element(By.CSS_SELECTOR, '[data-at="section-text-jobDescription-content"]')
                full_description = full_desc_elem.text
            except:
                full_description = "N/A"

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            writer.writerow([title, company, location, full_description])
        except Exception as e:
            continue

search_term = input("Enter a job keyword to search for (e.g. Software Engineer, DevOps etc.): ")
encoded_term = urllib.parse.quote(search_term)

page1_url = f"https://www.irishjobs.ie/jobs/{encoded_term}?page=1&searchOrigin=Resultlist_top-search&action=facet_selected%3bage%3b7&postedWithin=7"
page2_url = f"https://www.irishjobs.ie/jobs/{encoded_term}?page=2&searchOrigin=Resultlist_top-search&action=facet_selected%3bage%3b7&postedWithin=7"


options = Options()
options.add_argument('--headless')  
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

time.sleep(3)

filename = f"{search_term.lower().replace(' ', '_')}_jobs.csv"
with open(filename, "w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Job Title", "Company", "Location", "Full Description"])

    driver.get(page1_url)
    time.sleep(3)
    scrape_page(driver, writer)

    driver.get(page2_url)
    time.sleep(3)
    scrape_page(driver, writer)

driver.quit()
print(f"\n Saved data to '{filename}'")