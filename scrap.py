import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

dir_in = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(dir_in, "Downloads")

options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
})

# options.add_argument('--headless')
options.add_argument('--no-sandbox')

# Start Chrome driver
driver = webdriver.Chrome(options=options)

# Trigger the download
driver.get('https://cricsheet.org/matches/')
download_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/dl/dd[1]/a[1]')
download_button.click()
time.sleep(5)


# Function to wait for download to complete
def wait_for_downloads(download_dir, timeout=60):
    seconds = 0
    # while seconds < timeout:
    #     files = os.listdir(download_dir)
    #     print(files)
    #     if any(file.endswith(".crdownload") for file in files):
    #         time.sleep(1)
    #         seconds += 1
    #         print(seconds)
    #     else:
    #         break
    files = os.listdir(download_dir)
    while any(file.endswith(".crdownload") for file in files):
        time.sleep(1)
        seconds += 1
        print(seconds)
        

wait_for_downloads(download_dir)

print("Download complete!")

# You can now safely close the browser
driver.quit()