import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Define constants
BASE_URL = "https://prothomsir.com/job-solution/subcat/mcq/{}/all"
START_FROM_FILE = "last_visited.txt"
OUTPUT_FOLDER = "saved_pdfs"

# Function to load the last visited index


def load_last_visited():
    if os.path.exists(START_FROM_FILE):
        with open(START_FROM_FILE, "r") as file:
            return int(file.read().strip())
    return 1

# Function to save the last visited index


def save_last_visited(index):
    with open(START_FROM_FILE, "w") as file:
        file.write(str(index))

# Function to setup Chrome options


def setup_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--guest")  # Launch in guest mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")
    return chrome_options

# Function to save a page as PDF


def save_page_as_pdf(driver, output_folder):
    # Get the page title from <h1> tag
    try:
        h1_tag = driver.find_element("tag name", "h1").text
        safe_title = "".join(
            c if c.isalnum() else "_" for c in h1_tag).strip("_")
        pdf_path = os.path.join(output_folder, f"{safe_title}.pdf")

        # Trigger print dialog and save to PDF
        driver.execute_script("window.print();")
        print(f"PDF saved: {pdf_path}")
    except Exception as e:
        print(f"Error saving PDF: {e}")

# Main script logic


def main():
    # Load the last visited page number
    start_index = load_last_visited()

    # Create output folder if not exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Setup WebDriver
    chrome_options = setup_chrome_options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Loop through the pages
        for i in range(start_index, 1849):  # Adjust range as per requirement
            url = BASE_URL.format(i)
            print(f"Visiting: {url}")
            driver.get(url)
            time.sleep(5)  # Adjust delay as needed

            # Check for blocking
            if "blocked" in driver.page_source.lower():
                print("Blocked detected! Exiting program...")
                save_last_visited(i)
                break

            # Save the page as PDF
            save_page_as_pdf(driver, OUTPUT_FOLDER)

            # Update the last visited index
            save_last_visited(i)
    except Exception as e:
        print(f"Error encountered: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
