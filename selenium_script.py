import undetected_chromedriver as webdriver
import time

options = webdriver.ChromeOptions()
profile ="C:\\Users\\krish\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options.add_argument(f"user-data-dir ={profile}")
driver = webdriver.Chrome(options=options, use_subprocess=True)
driver.get("https://myaccount.google.com/")
time.sleep(10000)