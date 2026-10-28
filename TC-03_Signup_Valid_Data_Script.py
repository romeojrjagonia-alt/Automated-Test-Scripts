from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from helpers import BASE_URL, click, save_created_user, set_date, start_browser, unique_email, wait_visible

driver, wait = start_browser()
email = unique_email("new.player")


driver.get(f"{BASE_URL}/register")

    # Step 1: choose the "Player" card, then Next
click(wait, "button[wire\\:click*='player']")
click(wait, "button[wire\\:click='nextStep']")

    # Step 2: account details (the fields use their property name as the id)
wait_visible(wait, "#firstName").send_keys("Selenium")
driver.find_element(By.ID, "lastName").send_keys("Tester")
driver.find_element(By.ID, "middleInitial").send_keys("T")
driver.find_element(By.ID, "email").send_keys(email)
driver.find_element(By.ID, "password").send_keys("Selenium123")
driver.find_element(By.ID, "password_confirmation").send_keys("Selenium123")
click(wait, "button[wire\\:click='nextStep']")

set_date(driver, wait_visible(wait, "#birthDate"), "1998-01-15")
driver.find_element(By.ID, "phoneNumber").send_keys("09123456789")
Select(driver.find_element(By.ID, "gender")).select_by_value("male")
driver.find_element(By.ID, "purok").send_keys("Purok 5")
driver.find_element(By.ID, "city").send_keys("Ozamiz City")
driver.find_element(By.ID, "province").send_keys("Misamis Occidental")
driver.find_element(By.ID, "club").send_keys("OBC Badminton Club")
click(wait, "button[wire\\:click='register']")

wait.until(EC.url_contains("/player/dashboard"))
assert "/player/dashboard" in driver.current_url
save_created_user(email)  # so TC-06 can clean this account up
print(f"[PASS] TC-03 Sign Up Valid Data ({email})")

