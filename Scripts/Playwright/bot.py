import csv
import os
import time
from datetime import datetime

from importlib.metadata import version

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# =====================================================
# CONFIGURATION
# =====================================================

PLAYWRIGHT_VERSION = version("playwright")

WEBSITES = [
    "https://example.com/" # Write the website domain of interest
]

RUNS_PER_WEBSITE = 5
TOOL_NAME = "Playwright"
CSV_FILE = "./Results/playwright_results.csv"

SCREENSHOT_DIR = "./Results/screenshots"
ANTIBOT_WAIT_SECONDS = 15

FORM_SELECTORS = {
    "first_name": "#first-name",
    "last_name": "#last-name",
    "post": "#blog-content",
    "submit": "#blog-form button[type='submit']",
    "page_id": "#unique-id"
}

CSV_COLUMNS = [
    "Tools",
    "Agent Version",
    "Browser",
    "Browser Version",
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

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =====================================================
# HELPERS
# =====================================================

def generate_test_cookie(test_number, agent_name):
    now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    return f"{test_number}_{agent_name}_{now}"

def antibot_present(page) -> bool:
    indicators = [
        "captcha",
        "checking your browser",
        "verify you are human",
        "access denied",
        "challenge",
    ]
    content = page.content().lower()
    return any(x in content for x in indicators)


def page_is_usable(page) -> bool:
    try:
        page.wait_for_selector(FORM_SELECTORS["first_name"], timeout=2000)
        page.wait_for_selector(FORM_SELECTORS["last_name"], timeout=2000)
        page.wait_for_selector(FORM_SELECTORS["post"], timeout=2000)
        return True
    except PlaywrightTimeoutError:
        return False

def extract_cookie_id(context):
    try:
        cookies = context.cookies()
        print(context)
        print(cookies)
        for cookie in cookies:
            if cookie["name"] == "cookieId":
                return cookie["value"]
        return None
    except Exception:
        return None


# =====================================================
# MAIN TEST LOOP
# =====================================================

results = []
post_counter = 0

with sync_playwright() as p:

    for browser_name in ["chromium", "firefox"]:

        if browser_name == "firefox":
            browser = p.firefox.launch(
                headless=False,
                firefox_user_prefs={
                    "network.cookie.cookieBehavior": 0,  # allow all cookies
                    "privacy.trackingprotection.enabled": False,
                    "privacy.trackingprotection.pbmode.enabled": False,
                }
            )

        else:
            browser = getattr(p, browser_name).launch(headless=False)


        for website in WEBSITES:
            for run in range(RUNS_PER_WEBSITE):

                print(f"\n🌍 {browser_name.upper()} | {website} | Run {run}")

                context = browser.new_context(
                    viewport={"width": 1280, "height": 800},
                )

                page = context.new_page()

                now = datetime.now()
                status = "OK"
                blocked = False
                timeout = False
                page_id = "N/A"
                cookie_id = ""
                test_cookieId = ""

                first_name = f"Playwright_{post_counter}"
                last_name = f"Test_{post_counter}"
                post_content = f"This is post number {post_counter} created by Playwright."

                try:
                    page.goto(website, timeout=15000)
                    time.sleep(1)

                    # Extract any existing cookieId
                    page.wait_for_timeout(10000)
                    cookie_id = extract_cookie_id(context)
                    print(f"🍪 Existing cookieId: {cookie_id}")

                    # Generate test_cookieId and inject via context
                    test_cookie_value = generate_test_cookie(post_counter, "playwright")
                    context.add_cookies([{
                        "name": "test_cookieId",
                        "value": test_cookie_value,
                        "url": website,
                        # "path": "/",
                        "httpOnly": False,
                        "secure": False
                    }])

                    # Refresh page to ensure cookie is active
                    page.reload(wait_until="domcontentloaded")
                    page.wait_for_timeout(1000)

                    # Extract the injected cookie
                    cookies = context.cookies(website)
                    test_cookie = next((c for c in cookies if c["name"] == "test_cookieId"), None)
                    test_cookieId = test_cookie["value"] if test_cookie else None

                    print("🍪 Injected test_cookieId:", test_cookieId)

                    STANDARD_USER_AGENT = page.evaluate("() => navigator.userAgent")

                    browser_version = page.evaluate("() => navigator.userAgentData?.brands || navigator.userAgent")

                    page.wait_for_timeout(1000)

                    if antibot_present(page):
                        print("⛔ Anti-bot detected — waiting…")
                        time.sleep(ANTIBOT_WAIT_SECONDS)

                        if page_is_usable(page):
                            status = "CHALLENGE_PASSED"
                        else:
                            status = "BLOCKED"
                            blocked = True
                            raise Exception("Blocked by anti-bot")

                    if not page_is_usable(page):
                        status = "TIMEOUT"
                        timeout = True
                        raise PlaywrightTimeoutError("Page unusable")

                    # Fill form
                    page.fill(FORM_SELECTORS["first_name"], first_name)
                    page.fill(FORM_SELECTORS["last_name"], last_name)
                    page.fill(FORM_SELECTORS["post"], post_content)

                    try:
                        page_id = page.text_content(FORM_SELECTORS["page_id"])
                    except Exception:
                        pass

                    page.click(FORM_SELECTORS["submit"])
                    print("✅ Post submitted")

                except PlaywrightTimeoutError:
                    timeout = True
                    status = "TIMEOUT"
                    print("⏱️ TIMEOUT")

                except Exception as e:
                    blocked = True
                    status = "BLOCKED"
                    print(f"⛔ {e}")

                finally:
                    try:
                        browser_dir = os.path.join(SCREENSHOT_DIR, browser_name)
                        os.makedirs(browser_dir, exist_ok=True)

                        screenshot_path = os.path.join(
                            browser_dir,
                            f"{browser_name}_{post_counter}_{status}.png"
                        )

                        ua = page.evaluate("navigator.userAgent")
                        print(ua)

                        page.screenshot(path=screenshot_path, full_page=True)
                        print(f"📸 Screenshot saved: {screenshot_path}")

                    except Exception as e:
                        screenshot_path = "FAILED"
                        print(f"⚠️ Screenshot failed: {e}")

                    context.close()

                results.append([
                    TOOL_NAME,
                    PLAYWRIGHT_VERSION,
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
                time.sleep(2)

        browser.close()

# =====================================================
# CSV OUTPUT
# =====================================================

with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(CSV_COLUMNS)
    writer.writerows(results)

print(f"\n📄 CSV saved as {CSV_FILE}")
