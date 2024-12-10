import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

# Function to automate a single website
def automate_website(config):
    service = Service("C:/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get(config["url"])
        driver.maximize_window()

        for step in config["steps"]:
            try:
                if step["action"] in ["click", "fill", "select", "upload", "scroll-down", "iframe", "custom-click"]:
                    element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, step["locator"]))
                    )

                original_tabs = driver.window_handles
                if step["action"] == "click":
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                    driver.execute_script("arguments[0].click();", element)

                elif step["action"] == "fill":
                    element.send_keys(step["value"])

                elif step["action"] == "custom-click":
                    time.sleep(5)
                    element.click()
                    time.sleep(10)

                elif step["action"] == "dropdown":
                    dropdown_item = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, step["locator"]))
                    )
                    dropdown_item.click()

                elif step["action"] == "select":
                    select = Select(element)
                    select.select_by_visible_text(step["value"])

                elif step["action"] == "scroll-down":
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

                elif step["action"] == "upload":
                    element.send_keys(step["value"])
                    time.sleep(5)

                elif step["action"] == "iframe":
                    iframe = driver.find_element(By.XPATH, step["locator"])
                    driver.switch_to.frame(iframe)
                    time.sleep(5)

                new_tabs = driver.window_handles
                if len(new_tabs) > len(original_tabs):
                    driver.switch_to.window(new_tabs[-1])  # Switch to the newly opened tab
                    print("Switched to a new tab")

            except Exception as e:
                print(f"Error occurred while performing step: {step}")
                print(str(e))

        print(f"Script executed successfully for {config['url']}!")

    except Exception as e:
        print(f"An error occurred during execution for {config['url']}:")
        print(str(e))

    finally:
        time.sleep(5)
        driver.quit()

# Load user data
with open("user_data.json", "r") as f:
    data = json.load(f)

# Run automation for all websites in parallel
if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(automate_website, data[website]) for website in data]
        for future in futures:
            future.result()
