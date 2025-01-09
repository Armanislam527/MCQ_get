from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def test_default_chrome_profile():
    chrome_options = Options()
    # Path to the Chrome user data directory
    chrome_options.add_argument(
        "user-data-dir=/home/arman/.config/google-chrome")
    # Default profile (Default directory is automatically used)
    chrome_options.add_argument("--start-maximized")  # Open browser maximized
    # Disable popups for testing
    chrome_options.add_argument("--disable-popup-blocking")

    # Setup the ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to a test website
    test_url = "https://www.google.com"
    driver.get(test_url)

    # Print the title of the loaded page
    print(f"Page title: {driver.title}")

    # Let the browser stay open for 10 seconds (for manual inspection)
    input("Press Enter to close the browser...")

    # Close the browser
    driver.quit()


# Run the test
if __name__ == "__main__":
    test_default_chrome_profile()
