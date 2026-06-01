import os
import csv
import json
import asyncio
from datetime import datetime, date
from typing import Optional
import json
from bs4 import BeautifulSoup
from typing import Optional
from pydantic import BaseModel, ConfigDict
import litellm
from urllib.parse import urlparse

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    LLMConfig,
)
from crawl4ai import LLMExtractionStrategy
from dotenv import load_dotenv
from base64 import b64decode

litellm._turn_on_debug()
load_dotenv()
        
NB_RUNS_PER_SITE = 5
SITES = [
    # Replace with your target domains.
    "https://example.org/",
    
]

# Prompt 
INSTRUCTION = """
Complete the tasks below in order.

- Attempt to load the website normally.
- If a CAPTCHA, bot-detection, or access challenge appears, behave as a standard human user would by following the on-screen instructions using only the provided interface.
- If access is not granted within 15 seconds or after one retry, stop and respond: BLOCKED
- If a step still fails, respond: TIMEOUT

Final Response Format
- If blocked: BLOCKED
- If timed out: TIMEOUT
- Otherwise:
Page ID: <ID>
"""

def domain_from_url(url: str) -> str:
    host = urlparse(url).hostname  # e.g. "sub.a.example.co.uk"
    if not host:
        raise ValueError(f"Invalid URL: {url}")
    return host

def generate_test_cookieId(web_agent:str, mode:str, siteKey:str, test_index:str, date:str, time:str):
    domain = domain_from_url(siteKey)
    print(f"domain is : {domain}")
    return {
            "name": "test_cookieId", 
            "value": f"{test_index}_{web_agent}_{mode}_{date}_{time}", 
            "domain": str(domain),
            "path":"/"
        }
def extract_cookie_id_from_html(html: str) -> Optional[str]:
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    el = soup.find(id="__crawl4ai_client_state")
    print(el)
    if not el or not el.text:
        return None

    try:
        payload = json.loads(el.text)
    except json.JSONDecodeError:
        return None

    # 1️⃣ localStorage
    try:
        if "localStorage" in payload and "cookieId" in payload["localStorage"]:
            obj = json.loads(payload["localStorage"]["cookieId"])
            return str(obj.get("value")).strip()
    except Exception:
        pass

    # 2️⃣ sessionStorage
    try:
        if "sessionStorage" in payload and "cookieId" in payload["sessionStorage"]:
            obj = json.loads(payload["sessionStorage"]["cookieId"])
            return str(obj.get("value")).strip()
    except Exception:
        pass

    # 3️⃣ cookie header string
    cookie_header = payload.get("cookie", "")
    if isinstance(cookie_header, str):
        for part in cookie_header.split(";"):
            part = part.strip()
            if part.startswith("cookieId="):
                return part.split("=", 1)[1].strip()

    return None


class CrawlRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    blocked: bool = False
    timeout: bool = False
    page_id: str = ""

def safe_json_loads(s: str) -> Optional[dict]:
    try:
        return json.loads(s)
    except Exception:
        return None

async def main():
    web_agent = "Crawl4AI"
    agent_local_cloud = "LOCAL"
    agent_version = "0.8.0"
    model = "openai/gpt-4o-mini" # Replace with your model.
    model_local_cloud = "LOCAL"
    agent_local_cloud = "LOCAL"
    browser_local_cloud = False
    special_prompt = False
    
    cookie_js = r"""
        (() => {
            const payload = {
                cookie: document.cookie || "",
                localStorage: Object.fromEntries(Object.entries(localStorage || {})),
                sessionStorage: Object.fromEntries(Object.entries(sessionStorage || {})),
            };
            const el = document.createElement("pre");
            el.id = "__crawl4ai_client_state";
            el.style.display = "none";
            el.textContent = JSON.stringify(payload);
            document.documentElement.appendChild(el);
        })();
    """
    
    # LLMConfig + LLMExtractionStrategy
    llm_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider=model,
            api_token="YOUR_API_KEY", # Replace with your API_KEY
        ),
        schema=CrawlRecord.model_json_schema(),
        extraction_type="schema",
        instruction=INSTRUCTION,
        input_format="html",
        extra_args={"temperature": 0.2},
        apply_chunking=False,
        verbose=True
    )
    print(llm_strategy.base_url)

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=llm_strategy,
        wait_until="networkidle",
        js_code=[cookie_js],
        screenshot= True,
        magic=True,
        simulate_user=True,
        override_navigator=True,
    )

    today = date.today()
    date_str = today.strftime("%d-%m-%Y")

    os.makedirs("./results_normal_prompt", exist_ok=True)
    out_path = f"./results_normal_prompt/crawl4ai_gpt-4o-mini_results_normal_{date_str}.csv"

    columns = [
        "Web Agent", "Agent Local/Cloud", "Agent Version","Model", "Model Local/Cloud", 
        "Agent Browser", "Browser Local/Cloud", "Prompt Number", "Special prompt", 
        "Cookie ID", "Website", "Time", "Date", "BLOCKED", "TIMEOUT",
        "Page ID", "First Name", "Last Name", "Post Content", "test_cookieId"
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        f.flush()
        for siteIndex, site in enumerate(SITES):
            for i in range(NB_RUNS_PER_SITE):
                test_index = siteIndex * NB_RUNS_PER_SITE + i
                now = datetime.now()
                time_str = now.strftime("%H:%M")
                cookies = generate_test_cookieId(web_agent,"normal",site,test_index,date_str,time_str)
                browser_config = BrowserConfig(
                    headless=False,
                    verbose=True,
                    cookies=[cookies]
                    #enable_stealth=True # Uncomment to enable stealth features
                )
                
                agent_browser = browser_config.user_agent
                async with AsyncWebCrawler(config=browser_config) as crawler:
                    try:
                        result = await crawler.arun(url=site, config=run_config)

                        extracted = CrawlRecord()  # defaults
                        html = result.html or ""
                        marker = 'id="__crawl4ai_client_state"'
                        cookie_id =""
                        if marker in html:
                            cookie_id = extract_cookie_id_from_html(result.html)
                            print(cookie_id)
                        if result.success and result.extracted_content:
                            if result.screenshot:
                                print(f"[OK] Screenshot captured, size: {len(result.screenshot)} bytes")
                                with open(f"screenshots/run_gpt-4o-mini_{i}_{date_str}_{time_str}.png", "wb") as f_img:
                                    f_img.write(b64decode(result.screenshot))
                            else:
                                print("[WARN] Screenshot data is None.")
                                
                            payload = safe_json_loads(result.extracted_content)
                            
                            if payload is not None:
                                print(f"[OK] Payload {payload}")
                                if isinstance(payload, list) and payload:
                                    payload = payload[0]   # take first item
                                try:
                                    extracted = CrawlRecord.model_validate(payload)
                                    writer.writerow([
                                        web_agent,
                                        agent_local_cloud,
                                        agent_version, 
                                        model,
                                        model_local_cloud,
                                        agent_browser,
                                        browser_local_cloud,
                                        i,
                                        special_prompt,
                                        cookie_id,
                                        site,
                                        time_str,
                                        date_str,
                                        extracted.blocked,
                                        extracted.timeout,
                                        extracted.page_id,
                                        "",
                                        "",
                                        "",
                                        cookies["value"]
                                    ])
                                except Exception as e:
                                    print(e.message)
                                    # schema mismatch -> keep defaults, store error below
                                    writer.writerow([
                                        web_agent,
                                        agent_local_cloud,
                                        agent_version, 
                                        model,
                                        model_local_cloud,
                                        agent_browser,
                                        browser_local_cloud,
                                        i,
                                        special_prompt,
                                        "",
                                        site,
                                        time_str,
                                        date_str,
                                        True,
                                        True,
                                        "",
                                        "",
                                        "",
                                        "",
                                        cookies["value"]
                                    ])
                    except Exception as e:
                        print(e.message)
                        writer.writerow([
                            web_agent,
                            agent_local_cloud,
                            agent_version, 
                            model,
                            model_local_cloud,
                            agent_browser,
                            browser_local_cloud,
                            i,
                            special_prompt,
                            cookie_id,
                            site,
                            time_str,
                            date_str,
                            True,
                            True,
                            "",
                            "",
                            "",
                            "",
                            cookies["value"]
                        ])
                    f.flush()

    print(f"Saved: {out_path}")

if __name__ == "__main__":
    asyncio.run(main())
