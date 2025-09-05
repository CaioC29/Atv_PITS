from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
import time


def test_login(driver, site_url, username, password, user_field, pass_field, button_id, button_class):
    try:
        driver.delete_all_cookies()
        print("Cookies cleared")
        driver.get(site_url)
        print(f"Opening: {site_url}")

        wait = WebDriverWait(driver, 12)

        user_input = wait.until(EC.presence_of_element_located((By.NAME, user_field)))
        user_input.clear()
        user_input.send_keys(username)
        print(f"Inserted username '{username}' in {user_field}")

        pass_input = wait.until(EC.presence_of_element_located((By.NAME, pass_field)))
        pass_input.clear()
        pass_input.send_keys(password)
        print("Password entered")

        button = None
        if button_id:
            print(f"Looking for button with ID: {button_id}")
            button = wait.until(EC.element_to_be_clickable((By.ID, button_id)))
        elif button_class:
            print(f"Looking for button with class: {button_class}")
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, button_class)))

        if button:
            button.click()
            print("Login button clicked")

        time.sleep(1.5)
        print("Login attempt completed (check the site).\n")

    except TimeoutException:
        print(f"Timeout accessing {site_url}")
    except Exception as error:
        print(f"Error in {site_url}: {error}")


if __name__ == "__main__":
    websites = [
        {
            "url": "https://www.saucedemo.com/",
            "user_field": "user-name",
            "pass_field": "password",
            "button_id": "login-button",
            "button_class": "",
            "test_user": "standard_user",
            "correct_password": "secret_sauce"
        },
        {
            "url": "https://the-internet.herokuapp.com/login",
            "user_field": "username",
            "pass_field": "password",
            "button_id": "",
            "button_class": "radius",
            "test_user": "tomsmith",
            "correct_password": "SuperSecretPassword!"
        },
        {
            "url": "https://practicetestautomation.com/practice-test-login/",
            "user_field": "username",
            "pass_field": "password",
            "button_id": "submit",
            "button_class": "",
            "test_user": "student",
            "correct_password": "Password123"
        },
        {
            "url": "https://opensource-demo.orangehrmlive.com/",
            "user_field": "username",
            "pass_field": "password",
            "button_id": "",
            "button_class": "oxd-button.oxd-button--medium.oxd-button--main.orangehrm-login-button",
            "test_user": "Admin",
            "correct_password": "admin123"
        }
    ]

    browser = None
    try:
        service = FirefoxService(GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service)

        for site in websites:
            print("=" * 25, f" Testing: {site['url']} ", "=" * 25)

            print("\n→ Test with correct credentials")
            test_login(
                browser,
                site["url"],
                site["test_user"],
                site["correct_password"],
                site["user_field"],
                site["pass_field"],
                site["button_id"],
                site["button_class"]
            )
            print("-" * 60)
            time.sleep(2)

            print("\n→ Test with incorrect password")
            wrong_password = "invalid_pass123"
            test_login(
                browser,
                site["url"],
                site["test_user"],
                wrong_password,
                site["user_field"],
                site["pass_field"],
                site["button_id"],
                site["button_class"]
            )
            print("-" * 60)

            print("=" * 25, f" Finished: {site['url']} ", "=" * 25, "\n")

    except Exception as error:
        print(f"Error initializing browser: {error}")

    finally:
        if browser:
            browser.quit()
            print("Browser closed.")