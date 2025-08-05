from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

search_term = input("Enter a job keyword to search for (e.g. Software Engineer, DevOps etc.): ")
url = f"https://www.irishjobs.ie/ShowResults.aspx?Keywords={search_term}"

options = Options()
options.add_argument('--headless')  
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)

time.sleep(3)

job_cards = driver.find_elements(By.TAG_NAME, 'article')

print(f"\nTop {min(10, len(job_cards))} jobs for '{search_term}':\n")

for job in job_cards[:10]:
    try:
        title = job.find_element(By.CSS_SELECTOR, '[data-testid="job-item-title"]').text
        company = job.find_element(By.CSS_SELECTOR, '[data-at="job-item-company-name"]').text
        print(f"{title} @ {company}")
    except Exception:
        continue  

driver.quit()