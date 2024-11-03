# Website Screenshot Taker

A Python script that captures full-page screenshots of multiple websites using Selenium with a specified Chrome profile. 

## Requirements

- Python 3.x
- Selenium library
- ChromeDriver (compatible with your Chrome version)
- Google Chrome

## Installation

1. Install Selenium:
   ```bash
   pip install selenium


2. Download ChromeDriver from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/) and ensure it's accessible in your PATH.

## Usage

1. Update the script with the path to your Chrome profile and the URLs you want to capture:
   ```python
   profile_path = r"C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data"
   urls = [
       'https://www.example.com',
       'https://www.anotherexample.com'
   ]
   take_full_page_screenshots(urls, profile_path=profile_path)
   ```

2. Run the script:
   ```bash
   python your_script_name.py
   ```

## Output

Screenshots will be saved in the current directory with filenames based on the URLs.

## License

This project is licensed under the MIT License.