from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def test_add_task():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("http://13.60.221.109:8081/app/index.php")

    # Replace the following with actual logic
    task_input = driver.find_element("name", "task")
    task_input.send_keys("Buy groceries")

    submit_btn = driver.find_element("name", "submit")
    submit_btn.click()

    time.sleep(2)
    assert "Buy groceries" in driver.page_source
    driver.quit()
