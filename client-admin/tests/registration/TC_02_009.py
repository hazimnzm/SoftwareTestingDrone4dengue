import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from TestUtil import run_database_seed

# Test Case Data (TC-02-009)
BASE_URL = "http://localhost:3000"
SIGNUP_URL = f"{BASE_URL}/signup"
TEST_DATA = {
    "FullName": "Muhammad Hazim",
    "Email": "hazim009@um.edu.my",
    "UserName": "hazim_009",
    "PhoneNumber": "0123456789",
    "Pass": "Dengueee!",
    "ConfPass": "Dengueee!",
    "Terms": True
}

def test_password_no_number():
    """Verify that registration fails if password does not contain a number."""
    
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
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(TEST_DATA["Pass"])
        driver.find_element(By.ID, "confirmPassword").send_keys(TEST_DATA["ConfPass"])
        
        # Trigger blur to show error
        driver.find_element(By.TAG_NAME, "body").click()

        # Terms and Conditions
        terms_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Accept Terms and Privacy Policy']")
        terms_button.click()

        # 5. Submit the form
        print("Submitting the registration form...")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # 6. Verify Expected Results
        print("Verifying UI warning for password missing number...")
        
        # The system uses a combined message: "Password must be at least 8 characters and include a number"
        error_msg_xpath = "//p[contains(text(), 'include a number')]"
        error_msg = wait.until(EC.presence_of_element_located((By.XPATH, error_msg_xpath)))
        
        print(f"Detected error message: {error_msg.text}")
        
        if "include a number" in error_msg.text.lower():
            print("Confirmed: Password missing number error displayed.")
        else:
            raise Exception(f"Unexpected error message: {error_msg.text}")

        # Ensure we are still on the signup page
        assert SIGNUP_URL in driver.current_url
        print("Verified: User remains on the signup page.")

        print("\n" + "="*30)
        print("TEST CASE TC-02-009: PASSED")
        print("="*30)

    except Exception as e:
        print("\n" + "!"*30)
        print(f"TEST CASE TC-02-009: FAILED")
        print(f"Error: {str(e)}")
        print("!"*30)
        driver.save_screenshot("test_tc_02_009_failure.png")
        raise e

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    test_password_no_number()
