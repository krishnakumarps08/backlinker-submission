import urllib
import asyncio
import json
from playwright.async_api import async_playwright
import time
# NST Browser details
profile_id = "d8b34215-0af3-4551-ac85-5f2f788cedfb"  # udhaya 1
host = 'localhost'
port = "8848"
api_key = "96b7cbfd-8080-4b6a-8676-d2cbe4c686b6"
config = {
    "headless": True,  # Set to True for headless operation
    "autoClose": False,
}

# Encode the config dictionary as a JSON string
config_json = urllib.parse.quote_plus(str(config).replace("'", '"'))

# WebSocket endpoint for connection
browser_ws_endpoint = f"ws://{host}:{port}/devtool/launch/{profile_id}?x-api-key={api_key}&config={config_json}"


async def perform_action(page, action, locator, value=None):
    """Perform actions based on the action type."""
    element = page.locator(locator)

    try:
        if action == "click":
            await element.scroll_into_view_if_needed()
            await element.click()

        elif action == "fill":
            await element.fill(value)

        elif action == "custom-click":
            await element.wait_for()
            await asyncio.sleep(5)
            await element.click()
            await asyncio.sleep(10)

        elif action == "dropdown":
           await element.click()
            # Wait for dropdown options to appear and select an option by its text
           dropdown_option = page.locator(f"//li[text()='{value}']")
           await dropdown_option.click()

        elif action == "select":
            await element.select_option(value)

        elif action == "scroll-down":
            await element.scroll_into_view_if_needed()

        elif action == "upload":
            await element.set_input_files(value)
            await asyncio.sleep(5)

        elif action == "iframe":
            # Wait for the iframe to load
            iframe_locator = page.frame_locator(locator)
            # Interact with the CAPTCHA checkbox inside the iframe
            await iframe_locator.locator("//div[@class='recaptcha-checkbox-border']").click()

    except Exception as e:
        print(f"Error occurred while performing step: {action} with locator: {locator}")
        print(str(e))


async def browser_connection():
    # Start Playwright and connect to the NST browser
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(browser_ws_endpoint)
        context = browser.contexts[0]
        page = await context.new_page()

        # Load user data
        with open("user_data1.json", "r") as f:
            data = json.load(f)

        try:
            await page.goto(data["website4"]["url"], timeout=60000, wait_until="domcontentloaded")
            print(f"Page Title: {await page.title()}")
            for step in data["website4"]["steps"]:
                action = step["action"]
                locator = step["locator"]
                value = step.get("value")  # Value might not exist for all steps

                await perform_action(page, action, locator, value)

            print("Script executed successfully!")


        except Exception as e:
            print("An error occurred during execution:")
            print(str(e))

        finally:
            # Pause and close the browser
            await browser.close()


# Run the main async function
asyncio.run(browser_connection())
