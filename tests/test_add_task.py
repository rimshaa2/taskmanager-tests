import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Configuration
BASE_URL = "http://16.171.44.94:8081"

@pytest.fixture(scope="module")
def driver():
    """Initialize and configure the WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(3)
    yield driver
    driver.quit()

@pytest.fixture
def clean_state(driver):
    """Reset application state before each test"""
    driver.get(f"{BASE_URL}/")
    yield

def test_initial_empty_state(driver, clean_state):
    """Verify empty state is displayed correctly"""
    no_tasks_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'alert-info') and contains(., 'No tasks')]")
        )
    )
    assert no_tasks_msg.is_displayed()
    
    task_list = driver.find_element(By.CLASS_NAME, "list-group")
    assert len(task_list.find_elements(By.TAG_NAME, "li")) == 0

def test_add_and_verify_task(driver, clean_state):
    """Test adding a new task"""
    task_text = f"Selenium test task {time.time()}"
    
    task_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "task"))
    )
    task_input.send_keys(task_text)
    
    add_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    add_button.click()
    
    task_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//li[contains(@class, 'list-group-item') and contains(., '{task_text}')]")
        )
    )
    assert task_item.is_displayed()
    assert task_item.find_element(By.CSS_SELECTOR, ".btn-danger").is_displayed()

def test_delete_task_functionality(driver, clean_state):
    """Test deleting a task"""
    task_text = f"Task to delete {time.time()}"
    
    driver.find_element(By.NAME, "task").send_keys(task_text)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    task_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//li[contains(., '{task_text}')]")
        )
    )
    
    delete_btn = task_item.find_element(By.CSS_SELECTOR, ".btn-danger")
    delete_btn.click()
    
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert "Delete this task?" in alert.text
    alert.accept()
    
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (By.XPATH, f"//li[contains(., '{task_text}')]")
        )
    )

def test_form_validation(driver, clean_state):
    """Test form validation for empty input"""
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    
    task_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "task"))
    )
    assert "is-invalid" in task_input.get_attribute("class")
    assert len(driver.find_elements(By.CLASS_NAME, "list-group-item")) == 0

def test_multiple_task_management(driver, clean_state):
    """Test adding multiple tasks"""
    tasks = [f"Multi-task {i} {time.time()}" for i in range(3)]
    
    for task in tasks:
        driver.find_element(By.NAME, "task").send_keys(task)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element_value((By.NAME, "task"), "")
        )
    
    task_items = driver.find_elements(By.CLASS_NAME, "list-group-item")
    assert len(task_items) == len(tasks)
    
    for item in task_items:
        assert item.find_element(By.CSS_SELECTOR, ".btn-danger").is_displayed()

def test_persistence_after_refresh(driver, clean_state):
    """Verify tasks persist after refresh"""
    task_text = f"Persistent task {time.time()}"
    
    driver.find_element(By.NAME, "task").send_keys(task_text)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//li[contains(., '{task_text}')]")
        )
    )
    
    driver.refresh()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//li[contains(., '{task_text}')]")
        )
    )