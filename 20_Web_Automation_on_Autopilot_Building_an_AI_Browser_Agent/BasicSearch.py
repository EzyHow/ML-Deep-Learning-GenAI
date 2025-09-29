import asyncio
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
load_dotenv()

from browser_use import Agent, ChatGoogle

async def main():
    
    # Verify API key is loaded
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    print("GEMINI_API_KEY loaded successfully")

    # Initialize agent
    llm = ChatGoogle(model="gemini-flash-latest")
    task = "Search Google for 'what is browser automation' and tell me the top 3 results"
    agent = Agent(task=task, llm=llm)

    try:
        history = await agent.run()
    except Exception as e:
        print(f"Agent run failed: {e}")
        return

    # if history has a urls() method
    try:
        urls = history.urls()
    except AttributeError:
        print("Returned object has no urls() method; full history object:", history)
        return

    with open("agent_result.txt", "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=2)

    print("Result saved to agent_result.txt")

if __name__ == "__main__":
    asyncio.run(main())
