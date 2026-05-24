import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from TestUtil import run_database_seed

# Test Case Data (TC-02-011)
BASE_URL = "http://localhost:3000"
SIGNUP_URL = f"{BASE_URL}/signup"
TEST_DATA = {
    "FullName": "Muhammad Hazim",
    "Email": "hazim011@um.edu.my",
    "UserName": "hazim_011",
    "PhoneNumber": "0123456789",
    "Pass": "Dengue20!",
    "ConfPass": "Dengue20!",
    "Terms": True
}

def test_password_exactly_9():
    """Verify that registration succeeds with a password exactly 9 characters long."""
    
    # 1. Database Cleanup
    run_database_seed()

    # 2. Setup Selenium Chrome Driver
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # 3. Navigate to Registration Page
        print(f"Navigating to: {SIGNUP_URL}")
        driver.get(SIGNUP_URL)

        # 4. Fill in form
        print("Filling in registration form...")

        # Email field
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys(TEST_DATA["Email"])

        # Full Name field
        driver.find_element(By.ID, "name").send_keys(TEST_DATA["FullName"])

        # Username field
        driver.find_element(By.ID, "username").send_keys(TEST_DATA["UserName"])

        # Phone Number field
        driver.find_element(By.ID, "phone").send_keys(TEST_DATA["PhoneNumber"])

        # Company Select field
        company_elem = driver.find_element(By.ID, "company")
        company_select = Select(company_elem)
        wait.until(lambda d: len(company_select.options) > 1)
        company_select.select_by_index(1)

        # Password fields
        driver.find_element(By.ID, "password").send_keys(TEST_DATA["Pass"])
        driver.find_element(By.ID, "confirmPassword").send_keys(TEST_DATA["ConfPass"])

        # Terms and Conditions
        terms_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Accept Terms and Privacy Policy']")
        terms_button.click()

        # 5. Submit the form
        print("Submitting the registration form...")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # 6. Verify Expected Results
        print("Verifying successful registration and redirect to login...")
        
        # Should redirect to login (root URL)
        wait.until(EC.url_to_be(f"{BASE_URL}/"))
        print(f"Successfully redirected to: {driver.current_url}")

        # Final check: Ensure we are on the login page by looking for the login button
        login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
        if "LOGIN" in login_button.text:
            print("Verified: User is on the Login screen.")

        print("\n" + "="*30)
        print("TEST CASE TC-02-011: PASSED")
        print("="*30)

    except Exception as e:
        print("\n" + "!"*30)
        print(f"TEST CASE TC-02-011: FAILED")
        print(f"Error: {str(e)}")
        print("!"*30)
        driver.save_screenshot("test_tc_02_011_failure.png")
        raise e

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    test_password_exactly_9()
