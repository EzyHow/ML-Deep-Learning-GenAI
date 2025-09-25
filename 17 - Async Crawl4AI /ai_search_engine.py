import asyncio
import sys
import time
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

OUTPUT_FILE = "crawl_output.txt"
TIME_LIMIT = 180  # seconds (3 minutes)

async def main():
    # Redirect print output to file
    sys.stdout = open(OUTPUT_FILE, "w", encoding="utf-8")

    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            include_external=False
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )

    async with AsyncWebCrawler() as crawler:
        try:
            # Run crawler with timeout
            results = await asyncio.wait_for(
                crawler.arun("https://www.wikipedia.org", config=config),
                timeout=TIME_LIMIT
            )

            print(f"Crawled {len(results)} pages in total")

            for result in results[:3]:
                print(f"URL: {result.url}")
                print(f"Depth: {result.metadata.get('depth', 0)}")

        except asyncio.TimeoutError:
            print(f"Crawl stopped after {TIME_LIMIT} seconds (timeout reached).")

    sys.stdout.close()

if __name__ == "__main__":
    asyncio.run(main())

    # Display the contents of the output file
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        print(f.read())