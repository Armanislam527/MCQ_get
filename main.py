import os
import time
import pdfkit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configure WebDriver
driver = webdriver.Chrome()
base_url = "https://prothomsir.com/job-solution"

# Configure pdfkit
pdfkit_options = {
    "page-size": "A4",
    "encoding": "UTF-8",
}

# Set of visited URLs to avoid duplication
visited_urls = set()


def scrape_directory(url, output_folder):
    try:
        if url in visited_urls:
            print(f"Skipping already visited URL: {url}")
            return
        visited_urls.add(url)

        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Parse the page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all links containing "/job-solution/cat/"
        target_links = []
        next_links = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            link_text = link.text.strip()

            # If the link contains "/job-solution/cat/", add to target_links
            if "/job-solution/cat/" in href:
                target_links.append(href)

            # If the link text is "Next", add to next_links
            elif "Next" in link_text:
                next_links.append(href)

        # Resolve relative links to full URLs
        target_links = [link if link.startswith(
            "http") else base_url + link for link in target_links]
        next_links = [link if link.startswith(
            "http") else base_url + link for link in next_links]

        # Prioritize target links, then Next links
        if target_links:
            for target_url in target_links:
                print(f"Redirecting to target: {target_url}")
                scrape_directory(target_url, output_folder)
        elif next_links:
            for next_url in next_links:
                print(f"Redirecting to Next: {next_url}")
                scrape_directory(next_url, output_folder)

        # Save the current page content as a PDF if it contains a date-like structure
        if "date" in url.lower():
            print(f"Saving content from: {url}")
            content = driver.page_source
            pdf_file_path = os.path.join(
                output_folder, f"{os.path.basename(url)}.pdf")

            # Save as PDF
            pdfkit.from_string(content, pdf_file_path, options=pdfkit_options)
            print(f"PDF saved: {pdf_file_path}")

            # Wait for confirmation
            input("Press Enter to confirm PDF creation and continue...")

    except Exception as e:
        print(f"Error occurred at {url}: {e}")
        time.sleep(2)  # Delay before retrying or moving on


# Main execution
try:
    root_output_folder = "./MCQ_Solution"
    os.makedirs(root_output_folder, exist_ok=True)
    scrape_directory(base_url, root_output_folder)
finally:
    driver.quit()
