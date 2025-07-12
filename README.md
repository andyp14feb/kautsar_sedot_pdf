# Kautsar Sedot PDF

> 🛠️ This script was created by request of my friend **Al Kautsar**, to automatically collect and download PDF documents from the JDIH Provinsi DKI Jakarta website.

---

## 🎯 Purpose

The script automates the process of searching for government regulations (Peraturan), opening their detail pages, and downloading associated PDF files. It also avoids duplicate downloads and keeps a log of everything.

---

## 📁 Features

- Search documents using keywords
- Automatically navigate pagination
- Download PDF files from each result
- Avoid duplicates using a log (`downloaded_files.json`)
- `reset.bat` allows resetting downloaded log and files (Windows only)

---

## 🚀 How to Use (Step-by-step)

### How To Video:
[tutorial on youtube](https://youtu.be/ZyQ-ijTlpUk)

### 1. Clone or Download the Project
You can either:

- 🧲 Clone using Git:
  ```bash
  git clone https://github.com/yourusername/kautsar-sedot-pdf.git
  cd kautsar-sedot-pdf
  ```

- 📦 Or Download ZIP from GitHub, extract it, and open the folder.

---

### 2. Create and Activate a Virtual Environment

#### 🪟 On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### 🐧 On Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

> Make sure Google Chrome is installed, as the script uses Selenium + ChromeDriver.

---

### 4. Run the Script

```bash
python main.py
```

You will be prompted to input a search keyword (e.g., `sekolah`, `lingkungan`, `sampah`, etc.).

---

### 5. View the Results

- All downloaded PDF files are saved in the `downloads/` folder.
- Metadata for each download is stored in `downloaded_files.json`.

---

## 🧼 Optional: Reset the Environment (Windows Only)

To clear the `downloads/` folder and the `downloaded_files.json` log:

```bash
reset.bat
```

> If you're using macOS or Linux, you'll need to remove the folder and JSON manually.

---

## 📌 Notes

- The script uses `Selenium`, so it will open Chrome windows as it works.
- Avoid touching the mouse/keyboard while it runs to prevent disruption.
- Download may take time depending on internet speed and number of pages.

---

## 🙏 Credit
Thanks to chatgpt and gemini for help.

---
