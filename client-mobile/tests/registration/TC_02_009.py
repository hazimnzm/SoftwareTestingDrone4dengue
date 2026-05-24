import time
import os
import unittest
import random
import string
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Test Case Data (TC-02-009)
# Appium Server URL
APPIUM_SERVER_URL = "http://localhost:4723"

# Desired Capabilities for Android
# Adjust these based on your local environment (emulator/real device)
CAPABILITIES = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android Device",
    # "udid": "f316778e", # Commented out to allow Appium to pick any available device

    # Target Expo Go for development testing
    "appPackage": "host.exp.exponent",

    "noReset": True,
    "ensureWebviewsHavePages": True,
    "nativeWebScreenshot": True,
    "newCommandTimeout": 3600,
    "connectHardwareKeyboard": True
}

def generate_random_email():
    """Generate a unique email to ensure registration succeeds every time."""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@example.com"

# Default test data - Email will be randomized in the test method
TEST_DATA = {
    "Email": generate_random_email(),
    "Pass": "Mobile123!",
    "ConfPass": "Mobile123!"
}

class TestMobileRegistrationAppium(unittest.TestCase):
    def setUp(self):
        print("Initializing Appium WebDriver...")
        options = UiAutomator2Options().load_capabilities(CAPABILITIES)

        # Core stabilization parameters
        options.set_capability("appium:ignoreHiddenApiPolicyError", True)
        options.set_capability("appium:adbExecTimeout", 60000)

        # --- EXPO GO BYPASS CODES ---
        # These help when testing inside the Expo Go container
        options.set_capability("appium:noReset", True)
        options.set_capability("appium:dontStopAppOnReset", True)
        options.set_capability("appium:forceAppLaunch", False)
        options.set_capability("appium:appWaitForLaunch", False)
        # ------------------------------

        self.driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        self.wait = WebDriverWait(self.driver, 30) # Increased timeout for splash screen

    def tearDown(self):
        print("Closing Appium session...")
        if self.driver:
            self.driver.quit()

    def test_mobile_registration_success(self):
        """Verify basic registration flow on the native mobile app using Appium."""
        
        # Use a fresh email for this run
        email = generate_random_email()
        print(f"Starting registration test with email: {email}")

        try:
            # 1. Wait for the app to load (bypass splash screen)
            print("Waiting for Login or Register screen to appear...")
            # We wait for either the 'Sign In' or 'Create Account' text to be present
            self.wait.until(lambda d: 
                d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")') or
                d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create Account")')
            )

            # 2. Ensure we are on the Register Screen

            print("Not on Register screen, attempting to navigate from Login...")
            # Find 'Sign Up' link on Login screen
            signup_link = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign Up")')
            ))
            signup_link.click()

            # Wait for Register screen to load
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your email")')
            ))

            # 3. Fill in registration details
            print("Filling in registration details...")

            # Email field
            email_field = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your email")'
            )
            email_field.send_keys(email)

            # Password field
            password_field = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create a password")'
            )
            password_field.send_keys(TEST_DATA["Pass"])

            # Confirm Password field
            confirm_password_field = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confirm your password")'
            )
            confirm_password_field.send_keys(TEST_DATA["ConfPass"])

            # 4. Accept Terms & Conditions
            print("Accepting Terms & Conditions...")
            # Click the text or the checkbox area
            terms_checkbox = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("I agree to DengueEye\'s")'
            )
            terms_checkbox.click()

            # 5. Submit the Form
            print("Clicking 'Create Account' button...")
            # We target the clickable button specifically. In RN, it might be a ViewGroup or the Text itself.
            # Usually text("Create Account") appears twice: Header and Button.
            # The button is usually the second one or has 'clickable' true.
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create Account").instance(1)')
            ))
            submit_button.click()

            # 6. Handle Success Alert
            print("Waiting for success alert...")
            # Native Android alerts have 'Success' title and 'OK' button
            try:
                success_alert_title = self.wait.until(EC.presence_of_element_located(
                    (AppiumBy.ID, "android:id/alertTitle")
                ))
                print(f"Alert detected: {success_alert_title.text}")
                
                ok_button = self.driver.find_element(AppiumBy.ID, "android:id/button1")
                ok_button.click()
            except Exception as alert_err:
                print(f"Standard alert not found, checking for custom alert or direct redirect: {alert_err}")

            # 7. Verify Redirect to Login
            print("Verifying redirect to Login screen...")
            # Look for 'Sign In' header or email field on login screen
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")')
            ))
            
            print("\n" + "="*30)
            print("TEST CASE TC-02-009 (Appium): PASSED")
            print("Email used: " + email)
            print("="*30)

        except Exception as e:
            print("\n" + "!"*30)
            print(f"TEST CASE TC-02-009 (Appium): FAILED")
            print(f"Error: {str(e)}")
            print("!"*30)
            # Save screenshot for debugging
            screenshot_path = os.path.join(os.getcwd(), "mobile_test_TC_02_009_appium_failure.png")
            try:
                self.driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
            except:
                print("Failed to save screenshot.")
            raise e

if __name__ == "__main__":
    unittest.main()
