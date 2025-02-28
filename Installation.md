Installation Manual
Prerequisites
Ensure you have the following installed on your system:
•	Python 3.7 or later
•	Google Chrome
•	ChromeDriver (compatible with your Chrome version)
Step 1: Clone the Repository
Open a terminal and run:
git clone https://github.com/yourusername/fda-approvals-scraper.git
cd fda-approvals-scraper
Step 2: Create a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Verify ChromeDriver Installation
Ensure that ChromeDriver is properly installed:
chromedriver --version
If not installed, use:
pip install chromedriver-autoinstaller
Step 5: Run the Scraper
python main.py
Troubleshooting
•	If ChromeDriver is not detected, manually download it from: https://chromedriver.chromium.org/downloads
•	Ensure your Chrome browser is up to date.
•	If permission issues arise, try running with sudo (Linux/macOS) or as Administrator (Windows).
Uninstallation
To remove the project, delete the directory:
rm -rf fda-approvals-scraper

