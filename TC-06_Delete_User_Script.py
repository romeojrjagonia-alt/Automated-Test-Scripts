import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from helpers import (
    click,
    click_modal_button,
    clear_created_users,
    login_as_admin,
    read_created_users,
    start_browser,
    wait_for_modal_title,
    wait_visible,
)

emails_to_delete = read_created_users()  # stops with a clear message if TC-03 wasn't run

driver, wait = start_browser()


def delete_user(email):
    # Search for the user so exactly one row is left
    search = wait_visible(wait, "input[aria-label='Search users']")
    search.send_keys(Keys.CONTROL, "a", Keys.DELETE)  # empty the box from the previous search
    search.send_keys(email)
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "button[aria-label^='Actions for']")) == 1)
    row_email = driver.find_element(By.XPATH, f"//span[normalize-space()='{email}']")
    assert row_email.is_displayed(), f"{email} was not found in the list"


    actions = wait_visible(wait, "button[aria-label^='Actions for']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", actions)
    time.sleep(0.5)
    actions.click()

    # Choose Delete, then confirm
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']"))).click()
    wait_for_modal_title(wait, "Delete user?")
    click_modal_button(wait)

    wait_for_modal_title(wait, "User deleted")
    click_modal_button(wait)

    empty = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[normalize-space()='No users found.']"))
    )
    assert empty.is_displayed()
    print(f"Deleted {email}")



    login_as_admin(driver, wait)
    click(wait, "a[href$='/admin/users']")
    wait.until(EC.url_contains("/admin/users"))

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(normalize-space(), 'Filter')]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Players']"))).click()
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//span[normalize-space()='admin@netplay.test']")))

    for email in emails_to_delete:
        delete_user(email)

    clear_created_users()  # everything is deleted, so empty the list
    print(f"[PASS] TC-06 Delete a user ({len(emails_to_delete)} account(s) from TC-03)")
