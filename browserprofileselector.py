from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Path to your existing Chrome profile
chrome_profile_path = "/home/arman/.config/google-chrome"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument(
    f"user-data-dir={chrome_profile_path}")  # Use existing profile
chrome_options.add_argument("profile-directory=Default")  # Use default profile
# Enable remote debugging
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
# Disable shared memory usage
chrome_options.add_argument("--disable-dev-shm-usage")
# Uncomment below if not using extensions
# chrome_options.add_argument("--disable-extensions")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Test WebDriver with a simple URL
# Check IP address for VPN confirmation
driver.get("https://www.whatismyip.com/")

# Perform your tasks
driver.quit()
