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

class TestRecommendationViewing(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options().load_capabilities(CAPABILITIES)
        self.driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def tearDown(self):
        self.driver.quit()

    def test_view_recommendations(self):
        """TCON-14-001: View High/Low risk recommendations."""

        setup_recommendation_test(self.driver)

        wait = self.wait

        print("Waiting for Recommendations screen...")

        # ensure screen is fully loaded
        time.sleep(3)

        def click_scroll_text(text):
            print(f"Looking for: {text}")

            for _ in range(5):
                try:
                    el = self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiScrollable(new UiSelector().scrollable(true))'
                        f'.scrollIntoView(new UiSelector().textContains("{text}"))'
                    )
                    el.click()
                    print(f"Clicked: {text}")
                    return True

                except Exception:
                    print(f"Scrolling to find {text}...")
                    try:
                        self.driver.swipe(500, 1600, 500, 600)
                    except:
                        pass
                    time.sleep(1)

            raise Exception(f"{text} not found")

        # 1. High Risk
        click_scroll_text("High Risk")

        time.sleep(2)

        # 2. Back button (more stable fallback)
        print("Clicking Back...")

        try:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Back"))).click()
        except:
            self.driver.back()

        time.sleep(2)

        # 3. Low Risk
        click_scroll_text("Low Risk")

if __name__ == "__main__":
    unittest.main()
