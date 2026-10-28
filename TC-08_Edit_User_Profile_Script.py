
import time

from selenium.webdriver.common.by import By

from helpers import click, login_as_player, start_browser, wait_visible

OPEN_PROFILE = "button[aria-label='Open your profile']"
EDIT_BUTTON = "button[wire\\:click='startEditing']"
SAVE_BUTTON = "button[wire\\:click='save']"
NAME_INPUT = "input[wire\\:model='name']"
ADDRESS_INPUT = "input[wire\\:model='address']"
PHONE_INPUT = "input[wire\\:model='phoneNumber']"

SHOWN_PHONE = "//p[normalize-space()='Contact Number']/following-sibling::p"
SHOWN_ADDRESS = "//p[normalize-space()='Address']/following-sibling::p"

driver, wait = start_browser()


def open_profile_in_edit_mode():
    click(wait, OPEN_PROFILE)
    click(wait, EDIT_BUTTON)
    wait_visible(wait, NAME_INPUT)


def replace_text(css, new_text):
    box = driver.find_element(By.CSS_SELECTOR, css)
    box.clear()
    box.send_keys(new_text)


def save_profile():
    click(wait, SAVE_BUTTON)
    wait_visible(wait, EDIT_BUTTON)  # the Edit button comes back once saving is done


try:
    login_as_player(driver, wait)

    # Remember the current values so we can restore them at the end
    open_profile_in_edit_mode()
    original_name = driver.find_element(By.CSS_SELECTOR, NAME_INPUT).get_attribute("value")
    original_address = driver.find_element(By.CSS_SELECTOR, ADDRESS_INPUT).get_attribute("value")
    original_phone = driver.find_element(By.CSS_SELECTOR, PHONE_INPUT).get_attribute("value")

    # Change the three fields and save
    stamp = int(time.time())
    new_name = f"Selenium Edited {stamp}"
    new_address = f"Purok {stamp % 10}, Ozamiz City, Misamis Occidental"
    new_phone = f"0917{stamp % 10000000:07d}"

    replace_text(NAME_INPUT, new_name)
    replace_text(ADDRESS_INPUT, new_address)
    replace_text(PHONE_INPUT, new_phone)
    save_profile()

    # Reload and reopen the profile: the values must come back from the database
    driver.refresh()
    click(wait, OPEN_PROFILE)
    wait_visible(wait, EDIT_BUTTON)
    shown_phone = driver.find_element(By.XPATH, SHOWN_PHONE).text
    shown_address = driver.find_element(By.XPATH, SHOWN_ADDRESS).text
    assert shown_phone == new_phone, f"Phone: expected {new_phone}, found {shown_phone}"
    assert shown_address == new_address, f"Address: expected {new_address}, found {shown_address}"

    # The name is shown in capitals by CSS, so read it from the edit box instead
    click(wait, EDIT_BUTTON)
    saved_name = wait_visible(wait, NAME_INPUT).get_attribute("value")
    assert saved_name == new_name, f"Name: expected {new_name}, found {saved_name}"

    # Put the original values back
    replace_text(NAME_INPUT, original_name)
    replace_text(ADDRESS_INPUT, original_address)
    replace_text(PHONE_INPUT, original_phone)
    save_profile()

    print("[PASS] TC-08 Edit User Profile")
finally:
    driver.quit()
