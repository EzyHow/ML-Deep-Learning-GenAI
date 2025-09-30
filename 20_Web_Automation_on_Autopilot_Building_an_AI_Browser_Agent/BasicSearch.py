import asyncio
import os
import json

from dotenv import load_dotenv
load_dotenv()

from browser_use import Agent, ChatGoogle, BrowserProfile

async def main():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables")
        return
    print("GOOGLE_API_KEY loaded successfully")

    browser_profile = BrowserProfile(headless=True)

    llm = ChatGoogle(model="gemini-flash-latest")

    task = (
        "Open google.com. Type 'what is browser automation' in search field and click on Lens icon to search. "
        "Wait for results and tell me the top 3 results"
    )

    agent = Agent(task=task, llm=llm, browser_profile=browser_profile)

    try:
        history = await agent.run()
    except Exception as e:
        print(f"Agent run failed: {e}")
        return

    try:
        if hasattr(history, "urls") and callable(history.urls):
            urls = history.urls()
        else:
            print("No .urls() method; using raw history object.")
            urls = history
    except Exception as e:
        print(f"Error accessing URLs: {e}")
        return

    with open("agent_result.txt", "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=2)

    print("Result saved to agent_result.txt")

if __name__ == "__main__":
    asyncio.run(main())
