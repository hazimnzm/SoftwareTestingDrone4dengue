import unittest
import sys
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from TestUtil import setup_recommendation_test

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

class TestRecommendationNavigateDashboard(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options().load_capabilities(CAPABILITIES)
        self.driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def tearDown(self):
        self.driver.quit()

    def test_navigate_to_dashboard(self):
        """TCON-14-002: Navigate to Dashboard."""

        setup_recommendation_test(self.driver)

        wait = self.wait

        print("Waiting for bottom navigation...")

        time.sleep(3)  # allow dashboard + nav to fully render

        def click_bottom_nav(text):
            print(f"Clicking bottom nav: {text}")

            for _ in range(5):
                try:
                    el = self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiScrollable(new UiSelector().scrollable(true))'
                        f'.scrollIntoView(new UiSelector().textContains("{text}"))'
                    )
                    el.click()
                    print(f"Clicked: {text}")
                    return

                except Exception:
                    try:
                        self.driver.swipe(500, 1600, 500, 800)
                    except:
                        pass
                    time.sleep(1)

            raise Exception(f"Bottom nav '{text}' not found")

        # Click Dashboard
        click_bottom_nav("Dashboard")
if __name__ == "__main__":
    unittest.main()
