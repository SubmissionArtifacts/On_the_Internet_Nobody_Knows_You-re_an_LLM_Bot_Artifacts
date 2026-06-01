const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

const puppeteerPkg = require("puppeteer/package.json");
const PUPPETEER_VERSION = puppeteerPkg.version;

// =====================================================
// CONFIGURATION
// =====================================================

const WEBSITES = [
    "https://example.com/" // Write the website domain of interest
];

const RUNS_PER_WEBSITE = 5;
const TOOL_NAME = "Puppeteer";
const CSV_FILE = "./Results/puppeteer_results.csv";

const SCREENSHOT_DIR = "./Results/screenshots";
const ANTIBOT_WAIT_SECONDS = 15;

const FORM_SELECTORS = {
    first_name: "#first-name",
    last_name: "#last-name",
    post: "#blog-content",
    submit: "#blog-form button[type='submit']",
    page_id: "#unique-id"
};

const CSV_COLUMNS = [
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
];

fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

// =====================================================
// HELPERS
// =====================================================

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function antibotPresent(page) {
    const indicators = [
        "captcha",
        "checking your browser",
        "verify you are human",
        "access denied",
        "challenge",
    ];
    const content = (await page.content()).toLowerCase();
    return indicators.some(x => content.includes(x));
}

async function pageIsUsable(page) {
    try {
        await page.waitForSelector(FORM_SELECTORS.first_name, { timeout: 2000 });
        await page.waitForSelector(FORM_SELECTORS.last_name, { timeout: 2000 });
        await page.waitForSelector(FORM_SELECTORS.post, { timeout: 2000 });
        return true;
    } catch {
        return false;
    }
}

async function extractCookieId(page) {
    try {
        return await page.evaluate(() => {
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
        });
    } catch {
        return null;
    }
}

// =====================================================
// MAIN LOOP
// =====================================================

(async () => {

    const results = [];
    let postCounter = 0;

    for (const browserName of ["chromium", "firefox"]) {

        console.log(`\n🚀 Launching ${browserName.toUpperCase()}`);

        const browser = await puppeteer.launch({
            browser: browserName === "firefox" ? "firefox" : undefined,
            headless: false,
            args: browserName === "firefox"
                ? []
                : ["--no-sandbox", "--disable-setuid-sandbox"],
            defaultViewport: { width: 1280, height: 800 }
        });

        const defaultUA = await browser.userAgent?.() || "NO_BROWSER_UA";

        const browserVersion = await browser.version();

        for (const website of WEBSITES) {
            for (let run = 0; run < RUNS_PER_WEBSITE; run++) {

                console.log(`\n🌍 ${browserName.toUpperCase()} | ${website} | Run ${run}`);

                const context = await browser.createBrowserContext();
                const page = await context.newPage();

                let blocked = false;
                let timeout = false;
                let status = "OK";
                let pageId = "N/A";
                let screenshotPath = "FAILED";
                let actualUserAgent = defaultUA;
                let cookieId = null;
                let test_cookieId = null;

                const firstName = `Puppeteer_${postCounter}`;
                const lastName = `Test_${postCounter}`;
                const postContent = `This is post number ${postCounter} created by Puppeteer.`;
                const now = new Date();
                
                try {
                    await page.goto(website, {
                        timeout: 15000,
                        waitUntil: "domcontentloaded"
                    });

                    // Generate a unique cookie value
                    const testNumber = postCounter;
                    const agentName = "puppeteer";
                    const nowStr = new Date().toISOString().replace(/:/g, "-").split(".")[0];
                    test_cookieId = `${testNumber}_${agentName}_${nowStr}`;

                    // Set the cookie for the current page domain
                    await page.setCookie({
                        name: "test_cookieId",
                        value: test_cookieId,
                        domain: new URL(website).hostname, // ensures it matches current site
                        path: "/",
                        httpOnly: false,
                        secure: false
                    });

                    // Reload the page so that the cookie is active
                    await page.reload({ waitUntil: "domcontentloaded" });

                    // Re-extract it via page.cookies()
                    const cookies = await page.cookies();
                    const testCookie = cookies.find(c => c.name === "test_cookieId");
                    cookieId = testCookie ? testCookie.value : null;

                    console.log("🍪 Injected & extracted cookieId:", cookieId);
                    
                    await sleep(10000);
                    
                    cookieId = await extractCookieId(page);
                    console.log("🍪 Cookie ID:", cookieId);

                    const actualUserAgent = await page.evaluate(() => {
                        if (typeof navigator === "undefined") return "NO_NAVIGATOR";
                        return navigator.userAgent || "UA_EMPTY";
                    });


                    if (await antibotPresent(page)) {
                        console.log("⛔ Anti-bot detected — waiting…");
                        await sleep(ANTIBOT_WAIT_SECONDS * 1000);

                        if (await pageIsUsable(page)) {
                            status = "CHALLENGE_PASSED";
                        } else {
                            blocked = true;
                            status = "BLOCKED";
                            throw new Error("Blocked by anti-bot");
                        }
                    }

                    if (!(await pageIsUsable(page))) {
                        timeout = true;
                        status = "TIMEOUT";
                        throw new Error("Page unusable");
                    }

                    await page.type(FORM_SELECTORS.first_name, firstName);
                    await page.type(FORM_SELECTORS.last_name, lastName);
                    await page.type(FORM_SELECTORS.post, postContent);

                    try {
                        await page.waitForSelector(FORM_SELECTORS.page_id, { timeout: 5000 });
                        pageId = await page.evaluate(
                            selector => document.querySelector(selector)?.innerText || "N/A",
                            FORM_SELECTORS.page_id
                        );
                    } catch {
                        pageId = "NOT_FOUND";
                    }


                    await page.click(FORM_SELECTORS.submit);
                    console.log("✅ Post submitted");
                    
                    await sleep(1000);
                    
                    try {
                        await page.waitForSelector("#unique-id", { timeout: 5000 });
                        pageId = await page.evaluate(
                            () => document.getElementById("unique-id")?.innerText || "EMPTY"
                        );
                    } catch {
                        pageId = "NOT_FOUND";
                    }

                } catch (err) {
                    console.log(`⚠️ ${err.message}`);
                } finally {

                    try {
                        screenshotPath = path.join(
                            SCREENSHOT_DIR,
                            `${browserName}_${postCounter}_${status}.png`
                        );
                        await page.screenshot({
                            path: screenshotPath,
                            fullPage: true
                        });
                        console.log(`📸 Screenshot saved`);
                    } catch {}

                    await context.close();
                }

                results.push([
                    TOOL_NAME,
                    PUPPETEER_VERSION,
                    browserName,
                    browserVersion,
                    postCounter,
                    website,
                    now.toTimeString().slice(0, 8),
                    now.toISOString().slice(0, 10),
                    blocked,
                    timeout,
                    pageId,
                    firstName,
                    lastName,
                    postContent,
                    actualUserAgent,
                    screenshotPath,
                    cookieId,
                    test_cookieId,
                ]);

                postCounter++;
                await new Promise(r => setTimeout(r, 2000));
            }
        }

        await browser.close();
    }

    // =====================================================
    // CSV OUTPUT
    // =====================================================

    const csv = [
        CSV_COLUMNS.join(","),
        ...results.map(r => r.map(x => `"${String(x).replace(/"/g, '""')}"`).join(","))
    ].join("\n");

    fs.writeFileSync(CSV_FILE, csv, "utf8");
    console.log(`\n📄 CSV saved as ${CSV_FILE}`);

})();
