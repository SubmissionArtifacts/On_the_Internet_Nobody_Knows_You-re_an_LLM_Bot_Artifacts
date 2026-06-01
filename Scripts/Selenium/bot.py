import csv
from datetime import datetime
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import os

from importlib.metadata import version

# =====================================================
# CONFIGURATION
# =====================================================

SELENIUM_VERSION = version("selenium")

GECKO_DRIVER_PATH = GeckoDriverManager().install()
CHROME_DRIVER_PATH = ChromeDriverManager().install()

WEBSITES = [
    "https://example.com/" # Write the website domain of interest
]

RUNS_PER_WEBSITE = 5
TOOL_NAME = "Selenium"
CSV_FILE = "./Results/selenium_cross_browser_results.csv"

FORM_SELECTORS = {
    "first_name": (By.ID, "first-name"),
    "last_name": (By.ID, "last-name"),
    "post": (By.ID, "blog-content"),
    "submit": (By.CSS_SELECTOR, "#blog-form button[type='submit']"),
    "page_id": (By.ID, "unique-id")
}

COLUMNS = [
    "Tools",
    "Agent Version",
    "Browser",
    "Browser_Version",
    "Post Number",
    "Website",
    "Time",
    "Date",
    "BLOCKED",
    "TIMEOUT",
    "Page_ID",
    "First_name",
    "Last_name",
    "Post_content",
    "Agent_Browser",
    "Screenshot",
    "Cookie_ID",
    "test_cookieId",
]

SCREENSHOT_DIR = "./Results/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

ANTIBOT_WAIT_SECONDS = 15

# =====================================================
# HELPERS
# =====================================================

def generate_test_cookie(test_number, agent_name):
    now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    return f"{test_number}_{agent_name}_{now}"

def antibot_present(driver) -> bool:
    indicators = [
        "captcha",
        "checking your browser",
        "verify you are human",
        "access denied",
        "challenge",
    ]
    src = driver.page_source.lower()
    return any(x in src for x in indicators)


def page_is_usable(driver) -> bool:
    try:
        driver.find_element(*FORM_SELECTORS["first_name"])
        driver.find_element(*FORM_SELECTORS["last_name"])
        driver.find_element(*FORM_SELECTORS["post"])
        return True
    except Exception:
        return False

def extract_cookie_id(driver):
    try:
        return driver.execute_script("""
            try {
                // localStorage (preferred)
                const ls = localStorage.getItem("cookieId");
                if (ls) {
                    const parsed = JSON.parse(ls);
                    if (parsed?.value) {
                        return String(parsed.value).trim();
                    }
                }

                // sessionStorage fallback
                const ss = sessionStorage.getItem("cookieId");
                if (ss) {
                    const parsed = JSON.parse(ss);
                    if (parsed?.value) {
                        return String(parsed.value).trim();
                    }
                }

                // document.cookie fallback
                const match = document.cookie
                    .split(";")
                    .map(c => c.trim())
                    .find(c => c.startsWith("cookieId="));

                if (match) {
                    return match.split("=")[1].trim();
                }

                return null;

            } catch (e) {
                return null;
            }
        """)
    except Exception:
        return None


# =========================
# DRIVER FACTORY
# =========================

def create_driver(browser: str):
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        return webdriver.Chrome(
            service=ChromeService(CHROME_DRIVER_PATH),
            options=options
        )

    if browser == "firefox":
        options = FirefoxOptions()
        return webdriver.Firefox(
            service=FirefoxService(GECKO_DRIVER_PATH),
            options=options
        )

    raise ValueError("Unsupported browser")


# =========================
# MAIN TEST LOOP
# =========================

results = []
post_counter = 0

for browser in ["chrome", "firefox"]:
    for website in WEBSITES:
        for run in range(RUNS_PER_WEBSITE):

            print(f"\n🌍 {browser.upper()} | {website} | Run {run}")

            driver = create_driver(browser)
            wait = WebDriverWait(driver, 10)

            now = datetime.now()
            blocked = False
            timeout = False
            page_id = None
            cookie_id = None
            test_cookieId = None

            first_name = f"Selenium_{post_counter}"
            last_name = f"Test_{post_counter}"
            post_content = f"This is post number {post_counter} created by Selenium."

            status = "OK"

            try:
                driver.get(website)

                # Give JS a brief moment to start rendering
                time.sleep(2)

                cookie_id = extract_cookie_id(driver)
                print(f"🍪 Cookie ID: {cookie_id}")
                cookie_value = generate_test_cookie(post_counter, "selenium")

                driver.add_cookie({
                    "name": "test_cookieId",
                    "value": cookie_value,
                    "path": "/",
                })

                driver.refresh()

                test_cookieId = driver.get_cookie("test_cookieId")["value"]

                print("Injected cookie :", test_cookieId)

                time.sleep(5)

                STANDARD_USER_AGENT = driver.execute_script("return navigator.userAgent;")

                capabilities = driver.capabilities
                browser_name = capabilities.get("browserName")
                browser_version = capabilities.get("browserVersion")

                if antibot_present(driver):
                    print("⛔ Anti-bot detected — waiting…")
                    time.sleep(ANTIBOT_WAIT_SECONDS)

                    if page_is_usable(driver):
                        status = "CHALLENGE_PASSED"
                    else:
                        status = "BLOCKED"
                        blocked = True
                        raise Exception("Blocked by anti-bot")

                if not page_is_usable(driver):
                    status = "TIMEOUT"
                    timeout = True
                    raise TimeoutException("Page unusable")

                wait.until(EC.presence_of_element_located(FORM_SELECTORS["first_name"])).send_keys(first_name)
                driver.find_element(*FORM_SELECTORS["last_name"]).send_keys(last_name)
                driver.find_element(*FORM_SELECTORS["post"]).send_keys(post_content)

                try:
                    page_id = driver.find_element(*FORM_SELECTORS["page_id"]).text
                except Exception:
                    page_id = "N/A"

                driver.find_element(*FORM_SELECTORS["submit"]).click()

                print("✅ Submitted")

            except TimeoutException:
                timeout = True
                status = "TIMEOUT"
                print("⏱️ TIMEOUT")

            except WebDriverException as e:
                timeout = True
                status = "TIMEOUT"
                print(f"❌ WebDriver error: {e}")

            except Exception as e:
                blocked = True
                status = "BLOCKED"
                print(f"⛔ {e}")


            finally:
                try:
                    browser_dir = os.path.join(SCREENSHOT_DIR, browser)
                    os.makedirs(browser_dir, exist_ok=True)

                    screenshot_name = f"{browser}_{post_counter}_{status}.png"
                    screenshot_path = os.path.join(browser_dir, screenshot_name)

                    driver.save_screenshot(screenshot_path)
                    print(f"📸 Screenshot saved: {screenshot_path}")

                except Exception as e:
                    print(f"⚠️ Failed to take screenshot: {e}")

                driver.quit()

            results.append([
                TOOL_NAME,
                SELENIUM_VERSION,
                browser_name,
                browser_version,
                post_counter,
                website,
                now.strftime("%H:%M:%S"),
                now.strftime("%Y-%m-%d"),
                blocked,
                timeout,
                page_id,
                first_name,
                last_name,
                post_content,
                STANDARD_USER_AGENT,
                screenshot_path,
                cookie_id,
                test_cookieId
            ])

            post_counter += 1
            time.sleep(2)  # Spacing between sessions


# =========================
# CSV OUTPUT
# =========================

with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(COLUMNS)
    writer.writerows(results)

print(f"\n📄 Results saved to {CSV_FILE}")
