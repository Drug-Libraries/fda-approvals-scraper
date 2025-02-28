# main.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

def scrape_fda_approvals(output_file="fda_approvals.csv"):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    url = "https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=reportsSearch.process"
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Approval Date", "Drug Name", "Submission", "Active Ingredients", "Company", "Submission Classification", "Submission Status"])

        while True:
            try:
                header = wait.until(EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'All Approvals')]")))
                current_month_year = header.text.split()[-2:]
                month, year = current_month_year[0], int(current_month_year[1])

                print(f"Extracting data for {month} {year}...")
                table_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr")))
                
                for row in table_rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 7:
                        data = [col.text.replace("\n", " ") for col in cols[:7]]
                        csv_writer.writerow(data)
                        print(f"Extracted: {data}")
                
                if month == "January" and year == 1900:
                    print("Reached January 1900. Stopping extraction.")
                    break
                
                prev_month_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Previous Month')]") ))
                prev_month_btn.click()
                time.sleep(7)
            
            except Exception as e:
                print(f"Error: {e}")
                break

    driver.quit()
    print(f"\nData saved to {output_file}")

if __name__ == "__main__":
    scrape_fda_approvals()
