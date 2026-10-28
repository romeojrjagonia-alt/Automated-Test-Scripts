from helpers import ADMIN_EMAIL, ERROR_TEXT, login, start_browser, wait_visible

driver, wait = start_browser()


login(driver, wait, ADMIN_EMAIL, "this-is-the-wrong-password")

error = wait_visible(wait, ERROR_TEXT)
print("Error shown:", error.text)

assert "/login" in driver.current_url, f"Left the login page: {driver.current_url}"
assert error.text != "", "Error message was empty"
print("[PASS] TC-02 Invalid Login")
