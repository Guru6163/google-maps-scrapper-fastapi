from playwright.async_api import async_playwright
import asyncio
import urllib.parse

BASE_GOOGLE_SEARCH_URL = "https://www.google.com"
GOOGLE_SEARCH_TEXT = "site:lever.co OR site:greenhouse.io associate frontend developer"


async def scrape_jobs():
    links = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        job_postings = []
        try:
            await page.goto(BASE_GOOGLE_SEARCH_URL)
            await page.fill('textarea[name="q"]', GOOGLE_SEARCH_TEXT)
            await page.press('textarea[name="q"]', "Enter")

            # Wait for the "Tools" button to become visible
            await page.wait_for_selector('div[id="hdtb-tls"]')

            # Clicking on the "Tools" button
            await page.click('div[id="hdtb-tls"]')

            # Waiting for the menus to load (you may need to adjust the timeout)
            await page.wait_for_timeout(4000)

            # Clicking on the "Any time" dropdown
            await page.click('div[class="KTBKoe"]')

            # Selecting "Past Week"
            try:
                await page.click('a[href*="qdr:d"]')
            except playwright._impl._errors.TimeoutError:
                print("Past 24 hours option not found, selecting Past Week instead")
                await page.click('a[href*="qdr:w"]')

            await page.wait_for_timeout(4000)

            links = await page.evaluate(
                """() => {
                const links = [];
                document.querySelectorAll('a').forEach(link => {
                    if (link.href.startsWith('http') && !link.href.includes('google.com')) {
                        links.push(link.href);
                    } 
                });
                return links;
            }"""
            )

            greenhouse_or_lever_links = [
                link for link in links if "greenhouse" in link or "lever" in link
            ]

            for link in greenhouse_or_lever_links:
                company_name = get_company_name(link)
                job_postings.append({"job_link": link, "company_name": company_name})

        finally:
            await browser.close()
        return job_postings


def get_company_name(link):
    parsed_url = urllib.parse.urlparse(link)
    domain = parsed_url.netloc
    if "greenhouse.io" in domain:
        company_name = parsed_url.path.split("/")[1]
    elif "jobs.lever.co" in domain:
        company_name = parsed_url.path.split("/")[1]
    else:
        company_name = None
    return company_name
