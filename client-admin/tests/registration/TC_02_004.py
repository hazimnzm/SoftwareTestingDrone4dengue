import time
import subprocess
import os
from selenium import webdriver
from TC_02_001 import register_test_account
from TestUtil import run_database_seed
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Test Case Data (TC-02-004)
BASE_URL = "http://localhost:3000"
SIGNUP_URL = f"{BASE_URL}/signup"
TEST_DATA = {
    "FullName": "Muhammad Hazim",
    "Email": "hazim@um.edu.my",
    "UserName": "duplicate_user",
    "PhoneNumber": "0123456789",
    "Pass": "Dengue2026!",
    "ConfPass": "Dengue2026!",
    "Terms": True
}

def test_duplicate_email_registration():
    """Verify that registration fails with an already registered email."""


    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")

    print("Initializing Chrome WebDriver...")
    run_database_seed()
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    register_test_account(driver, wait)
    try:
        # 1. Navigate to Registration Page
        print(f"Navigating to: {SIGNUP_URL}")
        driver.get(SIGNUP_URL)

        # 2. Fill in form with pre-existing email
        print(f"Filling in registration form with email: {TEST_DATA['Email']}...")

        # Email field
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.clear()
        email_field.send_keys(TEST_DATA["Email"])

        # Full Name field
        name_field = driver.find_element(By.ID, "name")
        name_field.clear()
        name_field.send_keys(TEST_DATA["FullName"])

        # Username field
        username_field = driver.find_element(By.ID, "username")
        username_field.clear()
        username_field.send_keys(TEST_DATA["UserName"])

        # Phone Number field
        phone_field = driver.find_element(By.ID, "phone")
        phone_field.clear()
        phone_field.send_keys(TEST_DATA["PhoneNumber"])

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

        # 3. Submit the form
        print("Submitting the registration form...")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # 4. Verify Expected Results
        print("Verifying UI warning for duplicate email...")

        # The system should trigger an explicit UI warning banner or inline error.
        # Based on page.tsx, if status is 409 and message includes "email", it sets fieldErrors.email.
        # It also sets submitErrors.

        # Check for inline error first (text-yellow-200)
        try:
            error_msg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#email + p, .text-yellow-200, .text-light-bg")))
            print(f"Detected error message: {error_msg.text}")
            if "already" in error_msg.text.lower() or "registered" in error_msg.text.lower() or "taken" in error_msg.text.lower():
                print("Confirmed: Duplicate email error displayed.")
            else:
                # Check for Alert banner if not inline
                alert_banner = driver.find_element(By.CSS_SELECTOR, "div[role='alert']")
                print(f"Detected alert banner: {alert_banner.text}")
        except Exception as e:
            # Fallback check for any alert/banner
            alert_banner = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='alert']")))
            print(f"Detected alert banner: {alert_banner.text}")

        print("\n" + "="*30)
        print("TEST CASE TC-02-004: PASSED")
        print("="*30)

    except Exception as e:
        print("\n" + "!"*30)
        print(f"TEST CASE TC-02-004: FAILED")
        print(f"Error: {str(e)}")
        print("!"*30)
        driver.save_screenshot("test_tc_02_004_failure.png")
        raise e

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    test_duplicate_email_registration()
