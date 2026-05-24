import time
import os
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

class TestRegistrationPasswordSymbol(unittest.TestCase):
    def setUp(self):
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

    def test_missing_symbol_error(self):
        """TC-02-015: Verify error message for missing special character/symbol (TCOV-02-015)."""
        print("Starting TC-02-015: Missing Special Character")
        email = "hazim@um.edu.my"
        password = "Dengue2026"
        
        try:
            # 1. Wait for the app to load
            print("Waiting for app to load...")
            self.wait.until(lambda d: 
                d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")') or
                d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create Account").className("android.widget.TextView")')
            )

            # 2. Ensure we are on the Register Screen
            if not self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your email")'):
                print("Navigating to Register screen...")
                signup_link = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign Up")')
                ))
                signup_link.click()

            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your email")')
            ))

            # 3. Fill in registration details
            print(f"Filling in details: Email={email}, Pass={password}")
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your email")').send_keys(email)
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create a password")').send_keys(password)
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confirm your password")').send_keys(password)

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
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create Account").className("android.widget.TextView").instance(1)')
            ))
            submit_button.click()

            # 6. Verify Error Message
            expected_error = "Password must include at least one symbol (e.g. !, @, #, $)."
            print(f"Verifying error message: {expected_error}")
            error_element = self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{expected_error}")')
            ))
            
            self.assertTrue(error_element.is_displayed())
            print("TEST CASE TC-02-015: PASSED")

        except Exception as e:
            print(f"TEST CASE TC-02-015: FAILED - {str(e)}")
            screenshot_path = os.path.join(os.getcwd(), "TC_02_015_failure.png")
            self.driver.save_screenshot(screenshot_path)
            raise e

if __name__ == "__main__":
    unittest.main()
