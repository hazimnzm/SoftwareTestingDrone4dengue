import time
import os
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestUtil import run_database_seed
# Appium Server URL
APPIUM_SERVER_URL = "http://localhost:4723"

# Desired Capabilities for Android
CAPABILITIES = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android Device",
    "appPackage": "host.exp.exponent",
    "noReset": True,
    "ensureWebviewsHavePages": True,
    "nativeWebScreenshot": True,
    "newCommandTimeout": 3600,
    "connectHardwareKeyboard": True
}

class TestRegistrationEmailCollision(unittest.TestCase):
    def setUp(self):
        run_database_seed()
        print("Initializing Appium WebDriver...")
        options = UiAutomator2Options().load_capabilities(CAPABILITIES)

        # Core stabilization parameters
        options.set_capability("appium:ignoreHiddenApiPolicyError", True)
        options.set_capability("appium:adbExecTimeout", 60000)

        # --- EXPO GO BYPASS CODES ---
        options.set_capability("appium:noReset", True)
        options.set_capability("appium:dontStopAppOnReset", True)
        options.set_capability("appium:forceAppLaunch", False)
        options.set_capability("appium:appWaitForLaunch", False)
        # ------------------------------

        self.driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def tearDown(self):
        print("Closing Appium session...")
        if self.driver:
            self.driver.quit()

    def test_email_already_exists_error(self):
        """TC-02-017: Verify 'Email already exists' error."""
        print("Starting TC-02-017: Identity Collision")
        email = "hazim@um.edu.my"
        password = "Dengue2026!"
        
        try:

            register_test_account(self, email, password)
            check_success_alert(self)
            register_test_account(self, email, password)

            # 6. Verify Error Message
            expected_error = "Email already exists. Please use another email."
            print(f"Verifying error message: {expected_error}")
            error_element = self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{expected_error}")')
            ))
            
            self.assertTrue(error_element.is_displayed())
            print("TEST CASE TC-02-017: PASSED")

        except Exception as e:
            print(f"TEST CASE TC-02-017: FAILED - {str(e)}")
            screenshot_path = os.path.join(os.getcwd(), "TC_02_017_failure.png")
            self.driver.save_screenshot(screenshot_path)
            raise e

def register_test_account(self, email, password):
    # 1. Wait for the app to load
    print("Waiting for app to load...")
    self.wait.until(lambda d:
                    d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")') or
                    d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiSelector().text("Create Account").className("android.widget.TextView")')
                    )

    # 2. Ensure we are on Register Screen
    print("Checking current screen...")

    on_register_screen = self.driver.find_elements(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Create a password")'
    )

    if not on_register_screen:
        print("Navigating to Register screen...")

        signup_link = self.wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Sign Up")'
            ))
        )

        signup_link.click()

        # Wait for register form to fully render
        self.wait.until(
            EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Create a password")'
            ))
        )

        time.sleep(1)

    # 3. Fill in registration details
    print(f"Filling in details: Email={email}")
    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your email")').send_keys(email)
    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create a password")').send_keys(
        password)
    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confirm your password")').send_keys(
        password)

    # 4. Accept Terms & Conditions
    print("Accepting Terms & Conditions...")

    try:
        # Locate the terms text block
        terms_text = self.wait.until(
            EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("I agree to DengueEye")'
            ))
        )

        rect = terms_text.rect

        # Checkbox is positioned LEFT of the text
        tap_x = rect['x'] - 40
        tap_y = rect['y'] + (rect['height'] // 2)

        print(f"Tapping checkbox area at ({tap_x}, {tap_y})")

        # Use mobile click gesture (more reliable than driver.tap)
        self.driver.execute_script(
            "mobile: clickGesture",
            {
                "x": tap_x,
                "y": tap_y
            }
        )

        time.sleep(1)

        # Safety check
        if "Terms & Conditions" in self.driver.page_source:
            raise Exception("Incorrectly opened Terms page instead of checking checkbox.")

        print("Checkbox clicked successfully.")

    except Exception as e:
        print(f"Checkbox interaction failed: {e}")
        raise

    # 5. Submit the Form
    print("Clicking 'Create Account' button...")
    submit_button = self.wait.until(EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().text("Create Account").className("android.widget.TextView").instance(1)')
    ))
    submit_button.click()



def check_success_alert(self):
    # 6. Handle Success Alert if present
    print("Checking for success alert...")

    try:
        # Wait briefly for popup animation
        time.sleep(2)

        # Try multiple selectors for OK button
        ok_button = None

        selectors = [
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
            (AppiumBy.XPATH, '//android.widget.Button[@text="OK"]'),
            (AppiumBy.XPATH, '//*[@text="OK"]'),
            (AppiumBy.ACCESSIBILITY_ID, 'OK')
        ]

        for by, value in selectors:
            try:
                ok_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((by, value))
                )

                if ok_button:
                    print(f"OK button found using: {value}")
                    break

            except:
                continue

        if ok_button:
            ok_button.click()
            print("Success alert dismissed.")

        else:
            print("OK button not found. Trying coordinate fallback...")

            # Fallback tap near bottom-right of popup
            window_size = self.driver.get_window_size()

            tap_x = int(window_size['width'] * 0.75)
            tap_y = int(window_size['height'] * 0.63)

            self.driver.execute_script(
                "mobile: clickGesture",
                {
                    "x": tap_x,
                    "y": tap_y
                }
            )

            print("Fallback popup tap executed.")

    except Exception as e:
        print(f"Success alert handling failed: {e}")

    print("Waiting for redirect back to Login screen...")

    self.wait.until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Sign In")'
        ))
    )

    time.sleep(2)

if __name__ == "__main__":
    unittest.main()
