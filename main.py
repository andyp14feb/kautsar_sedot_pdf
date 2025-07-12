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
from bs4 import BeautifulSoup




# === CONFIGURATION ===
BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
LOG_FILE = os.path.join(BASE_DIR, 'downloaded_files.json')
META_FILE = os.path.join(BASE_DIR, 'files_meta.json')

# Ensure output folders exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(META_FILE):
    with open(META_FILE, 'w') as f:
        json.dump([], f)

# Setup driver for Selenium
def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to check if a PDF is already downloaded
def is_downloaded(url):
    with open(LOG_FILE, 'r') as f:
        try:
            downloaded = json.load(f)
        except:
            downloaded = []
    return any(entry['url'] == url for entry in downloaded)

# Log download details to a JSON file
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

# Function to download PDF file from a URL
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

# Function to extract metadata from the 'meta-doc' block
def get_meta_data(driver):
    try:
        # Wait for the meta-doc block to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "meta-doc"))
        )

        # Extract data from meta-doc section
        meta_doc = driver.find_element(By.CLASS_NAME, "meta-doc")
        meta_data = {}

        # Extract values from all <p class="font-semibold">
        for p_tag in meta_doc.find_elements(By.CLASS_NAME, "font-semibold"):
            label = p_tag.text.strip()
            # Ensure you get the correct sibling element for the value
            try:
                value = p_tag.find_element(By.XPATH, "following-sibling::div").text.strip()
                meta_data[label] = value
            except Exception as e:
                print(f"❌ Error extracting value for label '{label}': {e}")
        
        # Print out the metadata to check if it's being extracted properly
        print(f"✅ Extracted Meta Data: {meta_data}")
        
        return meta_data
    except Exception as e:
        print(f"❌ Error extracting meta data: {e}")
        return {}

# Function to save the extracted metadata to a JSON file
def save_meta_data(meta_data):
    try:
        # Load existing meta data
        with open(META_FILE, 'r') as f:
            existing_data = json.load(f)

        # Append new data
        if meta_data:
            existing_data.append(meta_data)

            # Save the updated data to the file
            with open(META_FILE, 'w') as f:
                json.dump(existing_data, f, indent=2)
            print("✅ Meta data saved to files_meta.json")
        else:
            print("❌ No meta data to save.")
    except Exception as e:
        print(f"❌ Error saving meta data to file: {e}")

def extract_meta_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    meta_doc_section = soup.select_one("div.meta-doc div.flex.flex-col")
    data = {}

    if not meta_doc_section:
        print("⚠️ meta_doc_section not found")
        return {}

    if meta_doc_section:
        for block in meta_doc_section.find_all("div", class_="flex", recursive=False):
            label_div = block.find("div", class_="w-2/5")
            value_div = block.find("div", class_="w-3/5")
            
            if label_div and value_div:
                label = label_div.get_text(strip=True)
                tag_block = value_div.find("div", class_="taging")
                value = tag_block.get_text(" ", strip=True) if tag_block else value_div.get_text(strip=True)
                data[label] = value
    return data



# Scraping function with added meta data extraction
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

        # Wait for the search results page to fully load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/section[2]/div/div[1]/div[2]/div[1]"))
        )
        print("Page fully loaded.")

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

                    # Wait for the detail page to fully load before scraping
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "meta-doc"))
                    )
                    time.sleep(4)

                    # Extract metadata from the 'meta-doc' block
                    meta_data = get_meta_data(driver)
                    if meta_data:
                        # Save the extracted meta data to the file
                        save_meta_data(meta_data)

                    try:
                        # 1. Find PDF download link
                        download_link = driver.find_element(By.XPATH, "/html/body/section[2]/div/div/div[2]/div[2]/div[2]/div/a")
                        pdf_url = download_link.get_attribute("href")

                        # 2. Buat nama file dan path penyimpanan
                        filename = os.path.basename(pdf_url.split('?')[0])
                        file_path = os.path.join(DOWNLOAD_DIR, filename)

                        # 3. Ambil metadata dari halaman
                        page_html = driver.page_source
                        metadata = extract_meta_from_html(page_html)

                        # 4. Ambil judul untuk log
                        title = metadata.get("Judul Peraturan", driver.title.strip().split("|")[0])

                        if not is_downloaded(pdf_url):
                            # 5. Download PDF-nya
                            download_pdf(pdf_url, file_path)
                            log_download(title, pdf_url)

                            # 6. Simpan metadata ke file JSON di samping PDF
                            meta_path = os.path.splitext(file_path)[0] + ".json"
                            with open(meta_path, "w", encoding="utf-8") as f:
                                json.dump(metadata, f, ensure_ascii=False, indent=2)
                            print(f"📝 Metadata saved to {meta_path}")
                        else:
                            print(f"⚠️ Already downloaded: {filename}")

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
    print('-------------------------------')
    print('-------------------------------')
    keyword = input("🔠 Enter search keyword: ")
    scrape_jdih(keyword)
