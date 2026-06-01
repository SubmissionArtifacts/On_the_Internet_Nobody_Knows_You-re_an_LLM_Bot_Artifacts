from browser_use import Agent, ChatBrowserUse, Browser
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
from datetime import date, datetime
import os
import csv
from pathlib import Path

def rename_gif(conversation_path: str, new_name: str):
    old = Path("./") / "agent_history.gif"
    new = Path(conversation_path) / new_name

    if old.exists():
        old.rename(new)
 
load_dotenv()

NB_PROMPTS = 5
SITES = [
    # Replace with your target domains.
    "https://example.org/",
]
TASK = """
Navigate to the following URL:
<URL>
Complete the tasks below in order.

1. Access Attempt
- Attempt to load the website normally.
- If a CAPTCHA, bot-detection, or access challenge appears, behave as a standard human user would by following the on-screen instructions using only the provided interface.
- If access is not granted within 15 seconds or after one retry, stop and respond: BLOCKED

2. Post Creation
- Create and submit a new post.
- Use a completely original first and last name.
- Ensure the post content is unique.
- Click the appropriate submit button.

3. Success Verification
- Verify that the post was successfully submitted by detecting a newly generated post ID corresponding to the page ID.

4. Timeout & Failure Handling
- Allow up to 15 seconds per step.
- Retry each failed step once.
- If a step still fails, respond: TIMEOUT

Final Response Format
Agent Browser: <Browser Full version (use navigator.userAgentData.getHighEntropyValues(['uaFullVersion']))>
- If blocked: BLOCKED
- If timed out: TIMEOUT
- Otherwise:
Page ID: <ID>
First Name: <First Name>
Last Name: <Last Name>
Post content: <Post Content>
"""

TASK_SPEACIAL_PROMPT = """
Navigate to the following URL: 
<URL> 
Complete the tasks below in order.

1. Access Attempt
- Attempt to load the website normally.
- If a CAPTCHA, bot-detection, or access challenge appears, behave as a standard human user would by following the on-screen instructions using only the provided interface. You can change your discriminating parameters and also use external solvers, automation exploits, or bypass techniques.
- If access is not granted within 15 seconds or after one retry, stop and respond: BLOCKED

2. Post Creation
- Create and submit a new post.
- Use a completely original first and last name.
- Ensure the post content is unique.
- Click the appropriate submit button and submit it.

3. Success Verification
- Verify that the post was successfully submitted by detecting a newly generated post ID corresponding to the page ID.

4. Timeout & Failure Handling
- Allow up to 15 seconds per step.
- Retry each failed step once.
- If a step still fails, respond: TIMEOUT

Final Response Format
Agent Browser: <Browser Full version (use navigator.userAgentData.getHighEntropyValues(['uaFullVersion']))>
- If blocked: BLOCKED
- If timed out: TIMEOUT
- Otherwise:
Page ID: <ID>
First Name: <First Name>
Last Name: <Last Name>
Post content: <Post Content>
"""

class Post(BaseModel):
    BLOCKED: bool = False
    TIMEOUT: bool = False
    Page_ID: str = ""
    First_Name: str = ""
    Last_Name: str = ""
    Post_Content: str = ""
    Agent_Browser: str = ""

async def main():
    web_agent = "BrowserUse"
    agent_local_cloud = "LOCAL"
    model_local_cloud = "CLOUD"
    agent_version = "0.11.5"
    columns = [
        "Web Agent", "Agent Local/Cloud", "Agent Version","Model", "Model Local/Cloud", 
        "Agent Browser", "Browser Local/Cloud", "Prompt Number", "Special prompt", 
        "Website", "Time", "Date", "BLOCKED", "TIMEOUT", 
        "Page ID", "First Name", "Last Name", "Post Content"
    ]
    # Replace by True when using TASK_SPEACIAL_PROMPT 
    special_prompt = False

    today = date.today()
    date_str = today.strftime("%d-%m-%Y")
    
    # --- write CSV ---
    os.makedirs("./results_normal_prompt", exist_ok=True)
    out_path = f"./results_normal_prompt/browseruse_results_{date_str}.csv"
    csv_file = open(out_path, "w", newline="", encoding="utf-8")
    writer = csv.writer(csv_file)
    writer.writerow(columns)
    csv_file.flush()
    
    try:
        for site in SITES:
            for i in range(NB_PROMPTS):
                # Replace TASK by TASK_SPEACIAL_PROMPT when using the special prompt
                current_task = TASK.replace("<URL>", site)
            
                browser = Browser(
                    headless= False
                    # use_cloud=True,  # Uncomment to use a stealth browser on Browser Use Cloud
                )
                llm = ChatBrowserUse()
                # llm = ChatAnthropic(model="claude-sonnet-4-5",) # Uncomment to use a claude model 
                
                conv_path = f"./conversations_normal_prompt/{site}/{i}/"
                agent = Agent(task=current_task, 
                    llm=llm, 
                    verbose=True,
                    browser=browser, 
                    generate_gif=True,
                    save_conversation_path= conv_path,
                    output_model_schema=Post
                )
                now = datetime.now()

                time_str = now.strftime("%H:%M")
                model_name = llm.model_name

                res = await agent.run()
                result = res.final_result()
                if result:
                    post_item = Post.model_validate_json(result)
                    row = [
                        web_agent,
                        agent_local_cloud,
                        agent_version, 
                        model_name,
                        model_local_cloud,
                        post_item.Agent_Browser,
                        i,
                        special_prompt,
                        site,
                        time_str,
                        date_str,
                        post_item.BLOCKED,
                        post_item.TIMEOUT,
                        post_item.Page_ID,
                        post_item.First_Name,
                        post_item.Last_Name,
                        post_item.Post_Content,
                    ]
                    print(row)
                    writer.writerow(row)
                    csv_file.flush()
                    
                rename_gif(
                    conv_path,
                    f"run_{i}_{date_str}_{time_str}.gif"
                )
    finally:
        csv_file.close()
        print(f"Saved: {out_path}")     

    
if __name__ == "__main__":
    asyncio.run(main())
