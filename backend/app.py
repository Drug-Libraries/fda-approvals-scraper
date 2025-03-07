from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")  # Path to frontend folder
OUTPUT_FOLDER = os.path.join(FRONTEND_DIR, "files")  # Folder for CSV storage

app = Flask(__name__)

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def scrape_fda_approvals(output_file, selected_year):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
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

                if year < int(selected_year):
                    print(f"Reached selected year {selected_year}. Stopping extraction.")
                    break

                table_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr")))

                for row in table_rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 7:
                        data = [col.text.replace("\n", " ") for col in cols[:7]]
                        csv_writer.writerow(data)

                prev_month_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'Previous Month')]")
                if prev_month_btns:
                    prev_month_btns[0].click()
                    time.sleep(7)
                else:
                    print("No Previous Month button found. Stopping.")
                    break

            except Exception as e:
                print(f"Error: {e}")
                break

    driver.quit()
    print(f"\nData saved to {output_file}")

@app.route("/")
def index():
    """Serve the frontend (index.html)"""
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    year = data.get("year", 2024)  # Default year if not provided
    output_file = os.path.join(OUTPUT_FOLDER, f"fda_approvals_{year}.csv")

    scrape_fda_approvals(output_file, year)

    return jsonify({"message": "Scraping complete", "download_url": f"/download/{year}"})

@app.route("/download/<year>")
def download(year):
    """Serve the generated CSV file for download"""
    file_path = os.path.join(OUTPUT_FOLDER, f"fda_approvals_{year}.csv")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

@app.route("/<path:filename>")
def serve_static(filename):
    """Serve any additional frontend files (JS, CSS, images)"""
    return send_from_directory(FRONTEND_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
