from helpers import login_as_admin, start_browser

driver, wait = start_browser()

login_as_admin(driver, wait)

assert "admin/dashboard" in driver.current_url, f"Login as admin successful: {driver.current_url}"

print("[PASS] TC-01 Valid Login\n Current Page: " + driver.current_url)