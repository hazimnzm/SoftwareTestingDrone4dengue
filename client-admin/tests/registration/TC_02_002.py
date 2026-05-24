import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Test Case Data (TC-02-002)
BASE_URL = "http://localhost:3000"
SIGNUP_URL = f"{BASE_URL}/signup"

def test_login_link_redirect():
    """Verify the 'Log in' text navigation link redirects to the main login view."""
    
    # Setup Selenium Chrome Driver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # 1. Navigate to Registration Page
        print(f"Navigating to: {SIGNUP_URL}")
        driver.get(SIGNUP_URL)

        # 2. Locate and click 'Login' link
        print("Locating 'Login' link...")
        login_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Login']")))
        
        print("Clicking 'Login' link...")
        login_link.click()

        # 3. Verify Expected Result
        print("Verifying redirect to Login screen...")
        # Login screen is at the root URL (/)
        wait.until(EC.url_to_be(f"{BASE_URL}/"))
        print(f"Successfully redirected to: {driver.current_url}")

        # Final check: Ensure we are on the login page by looking for the login button
        login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
        if "LOGIN" in login_button.text:
            print("Verified: User is on the Login screen.")
        
        print("\n" + "="*30)
        print("TEST CASE TC-02-002: PASSED")
        print("="*30)

    except Exception as e:
        print("\n" + "!"*30)
        print(f"TEST CASE TC-02-002: FAILED")
        print(f"Error: {str(e)}")
        print("!"*30)
        driver.save_screenshot("test_tc_02_002_failure.png")
        raise e

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    test_login_link_redirect()
