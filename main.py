import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# === CONFIGURATION ===
BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
LOG_FILE = os.path.join(BASE_DIR, 'downloaded_files.json')

# Ensure output folders exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def is_downloaded(url):
    with open(LOG_FILE, 'r') as f:
        try:
            downloaded = json.load(f)
        except:
            downloaded = []
    return any(entry['url'] == url for entry in downloaded)

def log_download(title, url):
    with open(LOG_FILE, 'r') as f:
        try:
            downloaded = json.load(f)
        except:
            downloaded = []

    downloaded.append({
        'title': title,
        'url': url,
        'downloaded_at': time.strftime('%Y-%m-%dT%H:%M:%S')
    })

    with open(LOG_FILE, 'w') as f:
        json.dump(downloaded, f, indent=2)

def download_pdf(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded: {file_path}")
        else:
            print(f"❌ Failed to download: {url}")
    except Exception as e:
        print(f"❌ Error downloading PDF: {e}")

def scrape_jdih(keyword):
    driver = setup_driver()
    driver.get("https://jdih.jakarta.go.id/pencarianCepat?tipe_dokumen=PU&jenis_dokumen_pu=semua")

    try:
        # === Step 1: Fill search field ===
        input_field = driver.find_element(By.XPATH, "/html/body/section[2]/div/div[2]/div[2]/form/div[1]/input")
        input_field.clear()
        input_field.send_keys(keyword)

        # === Step 2: Click search ===
        search_button = driver.find_element(By.XPATH, "/html/body/section[2]/div/div[2]/div[2]/form/button")
        search_button.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/section[2]/div/div[1]/div[2]/div[1]"))
        )

        while True:
            # === Step 3: Iterate search results ===
            results = driver.find_elements(By.XPATH, "/html/body/section[2]/div/div[1]/div[2]/div")
            print(f"🔎 Found {len(results)} results on this page.")

            for i in range(len(results)):
                try:
                    detail_button = results[i].find_element(By.XPATH, f"./div/a")
                    detail_url = detail_button.get_attribute("href")

                    # Open detail page in new tab
                    driver.execute_script("window.open(arguments[0], '_blank');", detail_url)
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)

                    try:
                        # Find PDF link
                        download_link = driver.find_element(By.XPATH, "/html/body/section[2]/div/div/div[2]/div[2]/div[2]/div/a")
                        pdf_url = download_link.get_attribute("href")

                        # Extract filename from URL
                        filename_from_url = os.path.basename(pdf_url.split('?')[0])
                        file_path = os.path.join(DOWNLOAD_DIR, filename_from_url)

                        # Get document title
                        title = driver.title.strip().split("|")[0]

                        if not is_downloaded(pdf_url):
                            download_pdf(pdf_url, file_path)
                            log_download(title, pdf_url)
                        else:
                            print(f"⚠️ Already downloaded: {filename_from_url}")

                    except Exception as e:
                        print(f"❌ PDF not found in detail page: {detail_url} | {e}")

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)

                except Exception as e:
                    print(f"⚠️ Failed to open result {i + 1}: {e}")

            # === Step 4: Pagination ===
            try:
                next_buttons = driver.find_elements(By.XPATH, "/html/body/section[2]/div/div[1]/nav/ul/a")
                next_found = False
                for btn in next_buttons:
                    if btn.text.strip().lower() == "next":
                        btn.click()
                        time.sleep(2)
                        next_found = True
                        break
                if not next_found:
                    print("✅ Reached last page.")
                    break
            except Exception as e:
                print(f"❌ Pagination error: {e}")
                break

    finally:
        driver.quit()

if __name__ == "__main__":
    keyword = input("🔠 Enter search keyword: ")
    scrape_jdih(keyword)
