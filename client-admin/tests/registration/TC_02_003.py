import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Test Case Data (TC-02-003)
BASE_URL = "http://localhost:3000"
SIGNUP_URL = f"{BASE_URL}/signup"
EXPECTED_TERMS_URL = f"{BASE_URL}/terms"

def test_terms_link_opens():
    """Verify clicking the legal policies hyperlink opens the Terms and Conditions."""
    
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

        # 2. Locate and click 'Terms and Privacy Policy' link
        print("Locating 'Terms and Privacy Policy' link...")
        terms_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Terms and Privacy Policy']")))
        
        # Store original window handle
        original_window = driver.current_window_handle
        
        print("Clicking 'Terms and Privacy Policy' link...")
        terms_link.click()

        # 3. Wait for new window/tab to open (since target="_blank")
        wait.until(EC.number_of_windows_to_be(2))
        
        # Switch to new window
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        # 4. Verify Expected Result
        print(f"Verifying URL of new window: {driver.current_url}")
        wait.until(EC.url_to_be(EXPECTED_TERMS_URL))
        
        # Check for some content on the terms page
        terms_title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        print(f"Terms page title: {terms_title.text}")
        
        print("\n" + "="*30)
        print("TEST CASE TC-02-003: PASSED")
        print("="*30)

    except Exception as e:
        print("\n" + "!"*30)
        print(f"TEST CASE TC-02-003: FAILED")
        print(f"Error: {str(e)}")
        print("!"*30)
        driver.save_screenshot("test_tc_02_003_failure.png")
        raise e

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    test_terms_link_opens()
