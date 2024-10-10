from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from selenium.webdriver.common.action_chains import ActionChains
import time
from anticaptchaofficial.recaptchav2proxyless import *

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

# brightdata --code --sym errors
# def scrape_website(website):
#     print("Connecting to Scraping Browser...")
#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         driver.get(website)
#         print("Waiting captcha to solve...")
#         solve_res = driver.execute(
#             "executeCdpCommand",
#             {
#                 "cmd": "Captcha.waitForSolve",
#                 "params": {"detectTimeout": 10000},
#             },
#         )
#         print("Captcha solve status:", solve_res["value"]["status"])
#         print("Navigated! Scraping page content...")
#         html = driver.page_source
#         return html


def scrape_website(website):
    print("Launching chrome browser...")

    chrome_driver_path = ""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-javascript")  # Enable JavaScript
    options.add_argument(
        "--disable-blink-features=AutomationControlled")  # Avoid detection
    options.add_argument("--incognito")  # Launch browser in incognito mode

    # Enable cookies
    options.add_argument("--enable-cookies")
    # options.add_argument('--proxy-server=http://your_proxy_address:port')

    driver = webdriver.Chrome(service=Service(
        chrome_driver_path), options=options)
    # Simulate human-like interaction
    action = ActionChains(driver)
    action.move_by_offset(100, 200).perform()  # Move the mouse
    time.sleep(3)  # Delay to simulate human interaction

    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source

        return html
    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=8000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
