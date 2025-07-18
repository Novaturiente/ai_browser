import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

script_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(script_dir, "chromedriver")
chrome_options = Options()
chrome_options.binary_location = "/nix/var/nix/profiles/default/bin/chromium"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

global latest_source
latest_source = ""


def browser_webpage(url: str) -> str:
    """Open a url and get contents of the page"""
    print(f"Opening {url}")
    global latest_source
    driver.get(url)
    html_data = driver.page_source
    latest_source = BeautifulSoup(html_data, "html5lib")

    return f"opened {url} and updated Latest source"


def input_text(element: str, text: str) -> str:
    """Input text to a field in the webpage"""
    print("Input")
    wait = WebDriverWait(driver, 10)
    input_field = wait.until(EC.presence_of_element_located((By.XPATH, element)))
    input_field.send_keys(text)

    return f"filled {element} with {text}"


def click_on_element(element: str) -> str:
    """Click on the given element in the webpage"""
    print("click")
    wait = WebDriverWait(driver, 10)

    element_to_click = wait.until(EC.presence_of_element_located((By.XPATH, element)))
    element_to_click.click()

    return f"clicked on {element}"


def get_current_status() -> str:
    """Get current source of the webpage"""
    print("update")
    global latest_source
    html_data = driver.page_source
    latest_source = BeautifulSoup(html_data, "lxml")

    return "Updated Latest source"


tool_list = [
    {
        "name": "browser_webpage",
        "description": "Open a webpage and get contents of the page as source data",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "url for the webpage to open",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "input_text",
        "description": "Enter text an input field identified by the XPATH on the webpage",
        "parameters": {
            "type": "object",
            "properties": {
                "element": {
                    "type": "string",
                    "description": "XPATH for the input field element",
                },
                "text": {
                    "type": "string",
                    "description": "text to enter in the field",
                },
            },
            "required": ["element", "text"],
        },
    },
    {
        "name": "click_on_element",
        "description": "Click on an element identified by XPATH in the webpage",
        "parameters": {
            "type": "object",
            "properties": {
                "element": {
                    "type": "string",
                    "description": "XPATH for the element to click",
                },
            },
            "required": ["element"],
        },
    },
    {
        "name": "get_current_status",
        "description": "Get source of the webpage to see the updated status of the page",
    },
]


tool_map = {
    "browser_webpage": browser_webpage,
    "input_text": input_text,
    "click_on_element": click_on_element,
    "get_current_status": get_current_status,
}
