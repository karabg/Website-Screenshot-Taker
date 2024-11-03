from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import time
import re


def take_screenshot(driver, url):
    sanitized_url = re.sub(r'[^\w\-_]', '_', url)
    output_file = f"{sanitized_url}_screenshot.png"

    print(f"Starting screenshot capture for URL: {url}")
    start_load = time.time()
    driver.get(url)
    end_load = time.time()

    start_height = time.time()
    total_height = driver.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight );"
    )
    driver.set_window_size(width=1920, height=max(total_height, 1080))
    end_height = time.time()

    start_screenshot = time.time()
    driver.save_screenshot(output_file)
    end_screenshot = time.time()

    print(f"Timing Statistics for {url}:")
    print(f" - Page Load Time: {(end_load - start_load):.2f} seconds")
    print(f" - Height Calculation Time: {(end_height - start_height):.2f} seconds")
    print(f" - Screenshot Time: {(end_screenshot - start_screenshot):.2f} seconds")
    print(f"Screenshot saved to {output_file}")
    print("-" * 80)

def take_full_page_screenshots(urls, profile_path=None):
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')

    if profile_path:
        chrome_options.add_argument(f"user-data-dir={profile_path}")
        chrome_options.add_argument("profile-directory=Profile 1")

    start_total_all = time.time()

    start_driver_init = time.time()
    driver = webdriver.Chrome(options=chrome_options)
    end_driver_init = time.time()
    print(f" - Driver Init Time: {(end_driver_init - start_driver_init):.2f} seconds")

    try:
        with ThreadPoolExecutor(max_workers=13) as executor:  # Adjust max_workers as needed
            executor.map(lambda url: take_screenshot(driver, url), urls)

        end_total_all = time.time()
        print(f"Total Execution Time for All URLs: {(end_total_all - start_total_all):.2f} seconds")

    finally:
        driver.quit()


# Usage example with profile path and list of URLs
profile_path = r"C:\Users\abgka\AppData\Local\Google\Chrome\User Data"
urls = [
    'https://www.gartenhaus-gmbh.de',
    'https://www.soldan.de',
    'https://www.example.com',
    'https://www.ebay.de/',
    'https://www.amazon.de/',
    'https://www.kleinanzeigen.de/',
    'https://www.idealo.de/',
    'https://www.otto.de/',
    'https://www.mediamarkt.de/',
    'https://www.thomann.de/gr/cat.html',
    'https://en.zalando.de/?_rfl=de',
    'https://www.lidl.de/',
    'https://www.saturn.de/',
    'https://obi.de'
]
take_full_page_screenshots(urls, profile_path=profile_path)
