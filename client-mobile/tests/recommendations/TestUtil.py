import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Add the parent directory to sys.path to import from registration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from registration.TestUtil import run_database_seed

def setup_recommendation_test(driver):
    login_test_account(driver, "user1@drone4dengue.com", "userpass1")
    print("clicking action button")
    wait = WebDriverWait(driver, 30)
    rec_tab = wait.until(EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Action")')
    ))
    rec_tab.click()

def login_test_account(driver, email, password):
    wait = WebDriverWait(driver, 30)

    print("Waiting for Login screen...")

    # More stable login screen detection
    wait.until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Sign")'
        ))
    )

    print(f"Logging in with: {email}")

    # Safer field selection (avoid exact match issues)
    email_field = wait.until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(0)'
        ))
    )
    email_field.clear()
    email_field.send_keys(email)

    password_field = wait.until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(1)'
        ))
    )
    password_field.clear()
    password_field.send_keys(password)

    # Replace fragile Sign In click
    print("Clicking Sign In button...")

    sign_in_selectors = [
        'new UiSelector().text("Sign In")',
        'new UiSelector().textContains("Sign")',
        'new UiSelector().className("android.widget.TextView").textContains("Sign")'
    ]

    clicked = False
    for sel in sign_in_selectors:
        try:
            btn = wait.until(
                EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, sel))
            )
            btn.click()
            print(f"Clicked Sign In using: {sel}")
            clicked = True
            break
        except:
            continue

    if not clicked:
        raise Exception("Sign In button not found")

    # Wait for dashboard safely (more stable than exact text)
    print("Waiting for Dashboard...")

    wait.until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Dashboard")'
        ))
    )

def dismiss_expo_popup(driver):
    try:
        # Expo popups are usually Toasts or transient Views
        time.sleep(2)

        # Try tapping OK / Got it / Dismiss if exists
        buttons = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("OK")'
        )

        if buttons:
            buttons[0].click()
            print("Popup dismissed via OK button")
            return

        buttons = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Got it")'
        )

        if buttons:
            buttons[0].click()
            print("Popup dismissed via Got it")
            return

        print("No clickable popup found (ignored)")
    except:
        pass