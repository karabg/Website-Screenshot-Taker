from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ProcessPoolExecutor
import tempfile
import shutil
import time
import re
import os


def take_screenshot(url, base_profile_path):
    # Create a temporary directory for each process to copy the base profile
    with tempfile.TemporaryDirectory() as temp_profile_dir:
        temp_profile_path = os.path.join(temp_profile_dir, 'Profile 1')
        shutil.copytree(base_profile_path, temp_profile_path)
        
        # Configure Chrome options for Selenium
        chrome_options = Options()
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument(f"user-data-dir={temp_profile_dir}")
        chrome_options.add_argument("profile-directory=Profile 1")

        # Start the WebDriver with options
        driver = webdriver.Chrome(options=chrome_options)

        try:
            sanitized_url = re.sub(r'[^\w\-_]', '_', url)  # Replace non-alphanumeric characters with underscores
            output_file = f"screenshots/{sanitized_url}_screenshot.png"

            print(f"Starting screenshot capture for URL: {url}")

            # Load the page
            start_load = time.time()
            driver.get(url)
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            end_load = time.time()

            # Calculate the full page height and set window size
            start_height = time.time()
            total_height = driver.execute_script(
                "return Math.max( document.body.scrollHeight, document.body.offsetHeight );"
            )
            driver.set_window_size(width=1920, height=max(total_height, 1080))
            end_height = time.time()

            # Take the screenshot
            start_screenshot = time.time()
            driver.save_screenshot(output_file)
            end_screenshot = time.time()

            # Print timing statistics
            print(f"Timing Statistics for {url}:")
            print(f" - Page Load Time: {(end_load - start_load):.2f} seconds")
            print(f" - Height Calculation Time: {(end_height - start_height):.2f} seconds")
            print(f" - Screenshot Time: {(end_screenshot - start_screenshot):.2f} seconds")
            print(f"Screenshot saved to {output_file}")
            print("-" * 80)

        finally:
            driver.quit()


def take_full_page_screenshots_parallel(urls, base_profile_path, max_workers=4):
    # Start the total execution timer
    start_total_time = time.time()

    # Ensure the screenshots directory exists
    os.makedirs("screenshots", exist_ok=True)

    # Use ProcessPoolExecutor to handle parallel processing
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(take_screenshot, url, base_profile_path) for url in urls]
        # Wait for all futures to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

    # End the total execution timer and print total time
    end_total_time = time.time()
    print(f"Total Execution Time for All URLs: {(end_total_time - start_total_time):.2f} seconds")


# Base Chrome profile path to be used as the template for each process
base_profile_path = "/home/server3090ti/.config/google-chrome/Profile 1"
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

# Set max_workers to a reasonable number based on system resources (e.g., number of CPU cores)
take_full_page_screenshots_parallel(urls, base_profile_path, max_workers=4)
