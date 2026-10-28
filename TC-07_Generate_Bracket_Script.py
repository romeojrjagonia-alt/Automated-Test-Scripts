from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from helpers import (
    BASE_URL,
    click,
    click_modal_button,
    login_as_admin,
    start_browser,
    wait_visible,
)

EVENT_NAME = "Demo Round Robin Cup"
CATEGORY_PREFIX = "Men"  

driver, wait = start_browser()


login_as_admin(driver, wait)
# Open the event from the events list
driver.get(f"{BASE_URL}/admin/events")
wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, f"//a[contains(@href,'/admin/events/')][contains(., '{EVENT_NAME}')]")
    )
).click()
# Open its Schedule tab (it lands on the first category)
click(wait, "a[href$='/schedule']")
wait_visible(wait, "select[aria-label='Category']")

# Switch to Men's Singles if another category is showing
category = Select(driver.find_element(By.CSS_SELECTOR, "select[aria-label='Category']"))
if not category.first_selected_option.text.startswith(CATEGORY_PREFIX):
    old_url = driver.current_url
    wanted = next(o.text for o in category.options if o.text.startswith(CATEGORY_PREFIX))
    category.select_by_visible_text(wanted)
    wait.until(lambda d: d.current_url != old_url)  # page reloads for the new category
    wait_visible(wait, "select[aria-label='Category']")

# Turn off auto dates so the schedule doesn't depend on the event's calendar
click(wait, "input[wire\\:model\\.live='autoDate']")
wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "input[wire\\:model='matchDuration']")))
# Generate, then confirm in the popup
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Generate Schedule']"))).click()
click_modal_button(wait)
message = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//p[contains(., 'Schedule generated')]"))
)
print("App says:", message.text)
click_modal_button(wait)
round_one = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//h3[normalize-space()='Round 1']"))
)
assert round_one.is_displayed()
print("[PASS] TC-07 Generate a Bracket")

