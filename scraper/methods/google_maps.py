from playwright.async_api import async_playwright
from .utils import extract_urls, fetch_details
import asyncio
import urllib.parse


async def scrape_google_maps(google_maps_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print("Maps URL:", google_maps_url)
        await page.goto(google_maps_url, wait_until="domcontentloaded")
        await page.wait_for_selector('[jstcache="3"]', timeout=60000)

        urls = await extract_urls(page)

        await page.close()

        print(f"Number of URLs extracted: {len(urls)}")

        concurrency = 5
        results = []
        promises = []
        for url in urls:
            p = fetch_details(url, context)
            promises.append(p)

            if len(promises) >= concurrency:
                for result in await asyncio.gather(*promises):
                    results.append(result)
                promises = []

        # Process any remaining promises
        for result in await asyncio.gather(*promises):
            results.append(result)

        await browser.close()

        return results
