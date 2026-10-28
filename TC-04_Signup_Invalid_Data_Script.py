from selenium.webdriver.common.by import By

from helpers import BASE_URL, ERROR_TEXT, click, start_browser, wait_visible

driver, wait = start_browser()


def error_messages():
    return [e.text for e in driver.find_elements(By.CSS_SELECTOR, ERROR_TEXT) if e.text]



driver.get(f"{BASE_URL}/register")

    # Part 1: press Next without choosing Player or Umpire
click(wait, "button[wire\\:click='nextStep']")
wait_visible(wait, ERROR_TEXT)
print("Step 1 errors:", error_messages())
assert any("choose" in m.lower() for m in error_messages()), "No user-type error"

# Part 2: choose Player, then submit step 2 with bad data
click(wait, "button[wire\\:click*='player']")
click(wait, "button[wire\\:click='nextStep']")
wait_visible(wait, "#firstName")  
driver.find_element(By.ID, "email").send_keys("not-an-email")
driver.find_element(By.ID, "password").send_keys("abc")
driver.find_element(By.ID, "password_confirmation").send_keys("xyz")
click(wait, "button[wire\\:click='nextStep']")

wait_visible(wait, ERROR_TEXT)
errors = error_messages()
print("Step 2 errors:", errors)

assert len(errors) >= 3, f"Expected several validation errors, got {errors}"
assert driver.find_elements(By.ID, "firstName"), "Wizard moved past step 2"
print("[PASS] TC-04 Sign Up Invalid Data")
