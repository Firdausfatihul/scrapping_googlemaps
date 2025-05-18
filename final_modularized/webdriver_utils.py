# webdriver_utils.py
from asyncio import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import config

def initialize_driver(
    process_id="WebDriver"
):
    print(
        f"[{process_id}] Initializing WebDriver"
    )

    options = webdriver.ChromeOptions()

    options.add_argument(
        f'--lang={config.BROWSER_LANG}'
    )
    print(
        f"[{process_id}] Browser language set to: {config.BROWSER_LANG}"
    )
    
    options.add_argument(
        f"user-agent={config.USER_AGENT}"
    )

    if config.HEADLESS_BROWSER:
        print(f"[{process_id}] WebDriver running in HEADLESS mode.")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080") 
        options.add_argument("--disable-gpu") 
        options.add_argument("--disable-dev-shm-usage") 
    else:
        print(f"[{process_id}] WebDriver running in VISIBLE mode.")
    
    try:
        print(
            f"[{process_id}] Attempting to install chromeDriver via webdriver_manager"
        )
        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=options
        )

        print(
            f"[{process_id}] Successfully installed chromeDriver via webdriver_manager"
        )
        return driver
    except Exception as e:
        print(
            f"[{process_id}] Error installing chromeDriver via webdriver_manager: {e}"
        )
        return None
        