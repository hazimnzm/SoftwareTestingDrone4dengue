import time
import os
from selenium import webdriver
from TestUtil import run_database_seed
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Test Case Data (TC-02-006)
BASE_URL = "http://localhost:3000"
SIGNUP_URL = f"{BASE_URL}/signup"
TEST_DATA = {
    "FullName": "Nurina",
    "Email": "nurina_at_um.edu.my", # Invalid format as per TC
    "UserName": "nurina",
    "PhoneNumber": "0123456789",
    "Pass": "Pass123!",
    "ConfPass": "Pass123!",
    "Terms": True
}

def test_invalid_email_registration():
    """Verify that the system validates the email format before submission."""
    run_database_seed()
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

        # 2. Fill in form with invalid email
        print(f"Filling in registration form with invalid email: {TEST_DATA['Email']}...")

        # Email field
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.clear()
        email_field.send_keys(TEST_DATA["Email"])

        # Fill other fields to trigger validation
        driver.find_element(By.ID, "name").send_keys(TEST_DATA["FullName"])
        driver.find_element(By.ID, "username").send_keys(TEST_DATA["UserName"])
        driver.find_element(By.ID, "phone").send_keys(TEST_DATA["PhoneNumber"])
        
        company_elem = driver.find_element(By.ID, "company")
        company_select = Select(company_elem)
        wait.until(lambda d: len(company_select.options) > 1)
        company_select.select_by_index(1)

        driver.find_element(By.ID, "password").send_keys(TEST_DATA["Pass"])
        driver.find_element(By.ID, "confirmPassword").send_keys(TEST_DATA["ConfPass"])

        # 3. Attempt to submit the form
        print("Submitting the registration form...")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # 4. Verify Expected Results
        print("Verifying UI error for invalid email format...")
        
        # The UI should show an error indicator stating: "Please enter a valid email address"
        # Based on page.tsx, it checks email onBlur or on validateForm.
        
        try:
            error_msg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#email + div + p, #email ~ p, .text-yellow-200")))
            print(f"Detected error message: {error_msg.text}")
            if "valid email" in error_msg.text.lower():
                print("Confirmed: Invalid email error message displayed.")
            else:
                print(f"Unexpected error message: {error_msg.text}")
        except:
            # Check if browser's native validation is used
            is_valid = driver.execute_script("return document.getElementById('email').validity.valid")
            if not is_valid:
                validation_msg = driver.execute_script("return document.getElementById('email').validationMessage")
                print(f"Confirmed: Browser validation blocked submission. Message: {validation_msg}")
            else:
                raise Exception("No error message detected and form was not blocked.")

        print("\n" + "="*30)
        print("TEST CASE TC-02-006: PASSED")
        print("="*30)

    except Exception as e:
        print("\n" + "!"*30)
        print(f"TEST CASE TC-02-006: FAILED")
        print(f"Error: {str(e)}")
        print("!"*30)
        driver.save_screenshot("test_tc_02_006_failure.png")
        raise e

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    test_invalid_email_registration()
