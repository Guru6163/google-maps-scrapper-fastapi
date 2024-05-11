from playwright.async_api import async_playwright

async def extract_urls(page):
    """
    Extract URLs from Google Maps search results page.
    """
    urls = []
    while True:
        page_content = await page.content()
        if "You've reached the end of the list." in page_content:
            print("Reached the end of the list.")
            break
        else:
            await page.evaluate('''() => {
                const scrollElement = document.evaluate('/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                scrollElement.scrollTop += 500;
            }''')

    urls = await page.evaluate('''() => {
        let elements = Array.from(document.querySelectorAll('a[href*="https://www.google.com/maps/place"]'));
        return elements.map(element => element.href);
    }''')

    return urls


async def fetch_details(url, context):
    """
    Fetch details from a single Google Maps business page.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='domcontentloaded')
        await page.wait_for_selector('[jstcache="3"]')

        details = await page.evaluate('''() => {
            const getText = (selector) => {
                const element = document.querySelector(selector);
                return element ? element.innerText : '';
            };

            const getHref = (primarySelector, fallbackSelector) => {
                let element = document.querySelector(primarySelector);
                if (!element) {
                    element = document.querySelector(fallbackSelector);
                }
                return element && element.href ? element.href : '';
            };

            const getTextFromXPath = (xpath) => {
                const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                return result.singleNodeValue ? result.singleNodeValue.innerText : '';
            };

            const companyName = getTextFromXPath('/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1');
            const rating = getTextFromXPath('/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]');
            let numberReviews = getTextFromXPath('/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span');
            numberReviews = numberReviews.replace(/\(|\)/g, '');
            const category = getTextFromXPath('/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button');
            return {
                company: companyName,
                rating: rating,
                reviews: numberReviews,
                category: category,
                address: getText('button[data-tooltip="Copy address"]'),
                website: getHref('a[data-tooltip="Open website"]', 'a[data-tooltip="Open menu link"]'),
                phone: getText('button[data-tooltip="Copy phone number"]')
            };
        }''')

        await browser.close()
        return details
