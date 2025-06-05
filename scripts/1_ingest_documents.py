import os
import fitz  # PyMuPDF
from docx import Document
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

DATA_FOLDER = "../data"
OUTPUT_FILE = "../data/raw_combined_text.txt"

# Crawl internal support & knowledge center URLs
def get_article_urls(base_url, max_links=50):
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        links = set()

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/support/") or href.startswith("/knowledge-center/"):
                full_url = "https://www.angelone.in" + href
                links.add(full_url)

        print(f"Found {len(links)} URLs from {base_url}")
        for url in list(links)[:max_links]:
            print(" -", url)
        return list(links)[:max_links]
        # return list(links)[:max_links]
    except Exception as e:
        print(f"[ERROR] Could not crawl {base_url}: {e}")
        return []

# Scrape content of each article using headless Chrome
def scrape_support_webpage():
    base_urls = [
        "https://www.angelone.in/support",
        "https://www.angelone.in/knowledge-center"
    ]

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    all_texts = []

    for base_url in base_urls:
        page_links = get_article_urls(base_url)
        for url in page_links:
            print(f"Visiting: {url}")
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "article"))
                )
                article_text = driver.find_element(By.TAG_NAME, "article").text
                print(f"Scraped content length: {len(article_text)}")
                all_texts.append(article_text)
            except Exception:
                print(f"Failed to scrape: {url} | Reason: {e}")
                continue  # skip failed pages

    driver.quit()
    return '\n\n'.join(all_texts)

def extract_pdf_text(pdf_path):
    text = ""
    pdf = fitz.open(pdf_path)
    for page in pdf:
        text += page.get_text()
    return text

def extract_docx_text(docx_path):
    doc = Document(docx_path)
    return '\n'.join(para.text for para in doc.paragraphs)

def main():
    combined_text = scrape_support_webpage() + "\n\n"

    for filename in os.listdir(DATA_FOLDER):
        path = os.path.join(DATA_FOLDER, filename)
        print(f"Processing file: {filename}")
        if filename.endswith(".pdf"):
            try:
                text = extract_pdf_text(path)
                print(f"Extracted {len(text)} characters from {filename}")
                combined_text += text + "\n\n"
            except Exception as e:
                print(f"Failed to read PDF: {filename} | {e}")
        elif filename.endswith(".docx"):
            try:
                text = extract_docx_text(path)
                print(f"Extracted {len(text)} characters from {filename}")
                combined_text += text + "\n\n"
            except Exception as e:
                print(f"Failed to read DOCX: {filename} | {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(combined_text)
    print(f"Ingestion complete. Total characters saved: {len(combined_text)}")
    print(f"Output file: {OUTPUT_FILE}")
    print("Ingestion complete. Data saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
