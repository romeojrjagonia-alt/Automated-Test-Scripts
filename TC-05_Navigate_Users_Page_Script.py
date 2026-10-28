import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers import click, login_as_admin, start_browser, scroll_up_down

driver, wait = start_browser()


login_as_admin(driver, wait)
click(wait, "a[href$='/admin/users']")  # the sidebar link
wait.until(EC.url_contains("/admin/users"))
heading = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='User Management']"))
)
time.sleep(0.5)
scroll_up_down(driver, 10000)  # scroll down 
time.sleep(1.5)
scroll_up_down(driver, -10000)  # scroll up
time.sleep(1.5)
assert heading.is_displayed()
print("[PASS] TC-05 Navigate to Users Page:", driver.current_url)

