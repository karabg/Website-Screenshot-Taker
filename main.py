from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import re


def take_full_page_screenshots(urls, profile_path=None):
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = "/usr/bin/google-chrome"

    if profile_path:
        chrome_options.add_argument(f"user-data-dir={profile_path}")
        chrome_options.add_argument("profile-directory=Profile 1")

    start_total_all = time.time()

    start_driver_init = time.time()
    driver = webdriver.Chrome(options=chrome_options)
    end_driver_init = time.time()
    print(f" - Driver Init Time: {(end_driver_init - start_driver_init):.2f} seconds")

    try:
        for url in urls:
            sanitized_url = re.sub(r'[^\w\-_]', '_', url)  # Replace non-alphanumeric characters with underscores
            output_file = f"screenshots/{sanitized_url}_screenshot.png"

            print(f"Starting screenshot capture for URL: {url}")

            start_load = time.time()
            driver.get(url)
            WebDriverWait(driver, 3.5).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            end_load = time.time()

            start_height = time.time()
            total_height = driver.execute_script(
                "return Math.max( document.body.scrollHeight, document.body.offsetHeight );"
            )
            driver.set_window_size(width=1920, height=max(total_height,1080) )
            end_height = time.time()

            # Measure time to take the screenshot
            start_screenshot = time.time()
            driver.save_screenshot(output_file)
            end_screenshot = time.time()

            print(f"Timing Statistics for {url}:")
            print(f" - Page Load Time: {(end_load - start_load):.2f} seconds")
            print(f" - Height Calculation Time: {(end_height - start_height):.2f} seconds")
            print(f" - Screenshot Time: {(end_screenshot - start_screenshot):.2f} seconds")

            print(f"Screenshot saved to {output_file}")
            print("-" * 80)

        end_total_all = time.time()
        print(f"Total Execution Time for All URLs: {(end_total_all - start_total_all):.2f} seconds")

    finally:
        driver.quit()


profile_path = "/home/server3090ti/.config/google-chrome/"
urls = [
    'https://www.gartenhaus-gmbh.de',
    'https://www.soldan.de',
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
