from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers import click, login_as_admin, start_browser

driver, wait = start_browser()


login_as_admin(driver, wait)
click(wait, "a[href$='/admin/users']")  # the sidebar link
wait.until(EC.url_contains("/admin/users"))
heading = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='User Management']"))
)
assert heading.is_displayed()
print("[PASS] TC-05 Navigate to Users Page:", driver.current_url)

