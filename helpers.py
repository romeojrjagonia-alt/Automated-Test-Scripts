import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:8000"


ADMIN_EMAIL = "admin@netplay.test"
ADMIN_PASSWORD = "password123"

PLAYER_EMAIL = "demo-player@netplay.test"
PLAYER_PASSWORD = "password123"


LOGIN_SUBMIT = "form[wire\\:submit='login'] button[type='submit']"
ERROR_TEXT = "p.text-red-600"  
MODAL_TITLE = "#system-modal-title"  
MODAL_PRIMARY_BUTTON = "button[x-ref='primary']"  


def start_browser(): #starts the browser and maximizes the window
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver, WebDriverWait(driver, 10)


def wait_visible(wait, css): #wait for an element to be visible
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))


def click(wait, css): #clicks on an element after waiting for it to be clickable
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css))).click()


def type_into(driver, css, text): #types text into an input field
    driver.find_element(By.CSS_SELECTOR, css).send_keys(text)


def login(driver, wait, email, password): #login function
    driver.get(f"{BASE_URL}/login")
    wait_visible(wait, "#email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    click(wait, LOGIN_SUBMIT)


def login_as_admin(driver, wait): #login as admin
    login(driver, wait, ADMIN_EMAIL, ADMIN_PASSWORD)
    wait.until(EC.url_contains("/admin/dashboard"))


def login_as_player(driver, wait): #login as player
    login(driver, wait, PLAYER_EMAIL, PLAYER_PASSWORD)
    wait.until(EC.url_contains("/player/dashboard"))


def click_modal_button(wait):
    click(wait, MODAL_PRIMARY_BUTTON)


def wait_for_modal_title(wait, expected):
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, MODAL_TITLE), expected))


def set_date(driver, element, value):
    driver.execute_script(
        "arguments[0].value = arguments[1];"
        "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
        "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
        element,
        value,
    )


# TC-03 writes the accounts it creates into this file (one email per line),
# and TC-06 reads it to delete them. It sits next to the scripts.
CREATED_USERS_FILE = Path(__file__).with_name("created_users.txt")


def save_created_user(email):
    with CREATED_USERS_FILE.open("a") as f:  # "a" = add a line, keep the old ones
        f.write(email + "\n")


def read_created_users():
    if not CREATED_USERS_FILE.exists():
        raise FileNotFoundError("No accounts to delete. Run TC-03 first.")
    return [line.strip() for line in CREATED_USERS_FILE.read_text().splitlines() if line.strip()]


def clear_created_users():
    CREATED_USERS_FILE.unlink(missing_ok=True)


def unique_email(prefix="selenium"):
    return f"{prefix}.{int(time.time())}@netplay.test"
