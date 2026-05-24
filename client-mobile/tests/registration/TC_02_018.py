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

class TestRegistrationToLoginNavigation(unittest.TestCase):
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

    def test_navigate_to_login(self):
        """TC-02-018: Verify redirect to the Login screen."""
        print("Starting TC-02-018: Navigate to Login")

        try:
            # 1. Wait for the app to load
            print("Waiting for Login screen...")
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")')
            ))

            # 2. Navigate to Register Screen
            print("Navigating to Register screen...")
            signup_link = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign Up")')
            ))
            signup_link.click()

            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your email")')
            ))

            # 3. Click the 'Sign In' link at the bottom
            print("Clicking 'Sign In' link...")
            # On Register screen, there's a text "Sign In" at the bottom to go back to Login
            signin_link = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")')
            ))
            signin_link.click()

            # 4. Verify navigation to the Login screen
            print("Verifying 'Welcome Back' header...")
            # Header in login.tsx is "Welcome Back"
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Welcome Back")')
            ))

            print("TEST CASE TC-02-018: PASSED")

        except Exception as e:
            print(f"TEST CASE TC-02-018: FAILED - {str(e)}")
            screenshot_path = os.path.join(os.getcwd(), "TC_02_018_failure.png")
            self.driver.save_screenshot(screenshot_path)
            raise e

if __name__ == "__main__":
    unittest.main()
