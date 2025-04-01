import asyncio
from playwright.async_api import async_playwright
# from websites import websites

async def extract_text_from_url(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        # Wait for network to be idle
        await page.wait_for_load_state("networkidle")

        # Get all visible text
        text = await page.evaluate("""
            () => {
                function isVisible(el) {
                    return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
                }
                return Array.from(document.querySelectorAll('body *'))
                    .filter(isVisible)
                    .map(el => el.innerText)
                    .join('\\n');
            }
        """)

        await browser.close()
        return text



def write_text_to_directory(websites, output_dir):
    """Writes scraped text content from websites to files in the specified directory.

    Args:
        websites: List of dictionaries containing website information. Each dictionary
            should have 'url' and 'name' keys.
        output_dir: String path to the directory where text files will be written.

    Returns:
        None

    Raises:
        IOError: If there are issues writing to the output directory.
    """
    for website in websites:
        url = website["url"]
        name = website["name"]
        text = asyncio.run(extract_text_from_url(url))
        path = output_dir+f"/{name}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        # print(text)
