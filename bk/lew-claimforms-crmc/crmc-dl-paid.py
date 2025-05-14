
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import Select 
# from selenium.webdriver.chrome.options import Options
import time
import subprocess
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import ActionChains
# import os
# import shutil
# import pygetwindow as gw

# Attach to existing Chrome session (running with remote debugging)
subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222", r"--user-data-dir=C:\Users\andrew.cabaj\AppData\Local\Google\Chrome\User Data"])
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Connect to running Chrome

# Start WebDriver (without launching a new Chrome instance)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

# Open the CRMC website; login
url = "https://eclaims.claimsres.com/ECX"
driver.get(url)
username = "ACabaj"
password = "SWMWLaw2025!"
username_field = wait.until(EC.visibility_of_element_located((By.ID, "UserName")))
username_field.clear()
username_field.send_keys(username)
password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
password_field.clear()
password_field.send_keys(password)
login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnLoginSubmit")))
login_button.click()

# Navigate to Claim Listing page 
search_menu = wait.until(EC.presence_of_element_located((By.ID, "Search")))
actions.move_to_element(search_menu).perform()
claim_listing = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Claim Listing")))
claim_listing.click()

# Filter for Trust and Status
trust_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "ddlTrust_ddlTrust_chosen")))
trust_dropdown.click()
manville_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='Manville']")))
manville_option.click()
status_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "ddlStatus_chosen")))
status_dropdown.click()
status_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'Settled Paid')]")))
status_option.click()
list_claims_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnListClaims")))
list_claims_btn.click()

links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@title='To Claim Demographics']")))
for link in links:
    link.click()
    
    name_element= driver.find_element(By.ID, "lblClaimantName")
    name = name_element.text
    claim_id_element = driver.find_element(By.ID, "lblClaimID")
    claim_id = claim_id_element.text
    descr = 'Manville Claim Form (CRMC)'
    status = 'Settled Paid'
    filename = f"{name} - {descr} - {claim_id} - {status}.pdf"
    print(filename)

    expand_print = wait.until(EC.element_to_be_clickable((By.ID, "ExpandPrintBtn")))
    expand_print.click()
    actions.send_keys(Keys.ENTER).perform()


#     # Navigate back to the listing page and wait for the elements to reload
#     driver.back()
#     wait.until(EC.presence_of_element_located((By.XPATH, "//a[@title='To Claim Demographics']")))


# time.sleep(2)  # Wait for new tab to load
# for handle in driver.window_handles:
#     driver.switch_to.window(handle)
#     if "Dashlane" in driver.title or "Dashlane" in driver.current_url:
#         print("Closing Dashlane tab...")
#         driver.close()
# driver.switch_to.window(driver.window_handles[-1]) 
# print("Switched to new tab.")
# 20 entries per pages - 76 pages for settled/paid claims; withdrawn can be done by hand


# ------------ VERUS STEPS as GUIDANCE ------------

# # Locate the "Paid" column link (First row under 'Paid' column)
# try:
#     paid_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//table//td/a[contains(text(), '769')]")))
#     paid_link.click()
#     print("Clicked 'Paid' link.")
# except TimeoutException:
#     print("Failed to find 'Paid' link.")
#     driver.quit()
#     exit(1)

# # def go_to_page(page_num, current_page_group):
# #     if page_num == 1:
# #         print("🟢 Already on page 1, no need to click.")
# #         return current_page_group
# #     if page_num <= 10:
# #         offset = page_num - 1  # ctl00 to ctl09
# #     else:
# #         offset = (page_num - 1) % 10 + 1  # ctl01 to ctl10

# #     ctl_id = f"ctl{offset:02}"
# #     page_str = f"ctl03$DGClaimDetail$ctl19${ctl_id}"

# #     if page_num > 10:
# #         target_group = (page_num - 1) // 10
# #         for _ in range(current_page_group, target_group):
# #             ellipsis_id = "ctl10" if _ == 0 else "ctl11"
# #             ellipsis_str = f"ctl03$DGClaimDetail$ctl19${ellipsis_id}"
# #             ellipsis_link = wait.until(EC.element_to_be_clickable(
# #                 (By.XPATH, f"//a[contains(@href, \"__doPostBack('{ellipsis_str}'\")]")))
# #             ellipsis_link.click()
# #             time.sleep(2)
# #         current_page_group = target_group

# #     page_link = wait.until(EC.element_to_be_clickable(
# #         (By.XPATH, f"//a[contains(@href, \"__doPostBack('{page_str}'\")]")))
# #     page_link.click()
# #     print(f"Navigated to page {page_num}")
# #     time.sleep(2)

# #     return current_page_group

# def process_claims_on_page():
#     for i in range(15):
#         claim_links = driver.find_elements(By.XPATH, 
#                                     "//a[string-length(normalize-space(text()))=7 and translate(normalize-space(text()), '0123456789', '')='']")
#         print(f"Processing claim {i+1}/{len(claim_links)}")
#         claim = claim_links[i]
#         claim.click()
#         claim_actions_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id, 'ClaimActions')]")))
#         wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Claim ID')]")))

#         # Extract Name (text in the row below "Name")
#         first_name_element = driver.find_element(By.ID, "ctl03_txtFirstName")
#         last_name_element = driver.find_element(By.ID, "ctl03_txtLastName")

#         first_name = first_name_element.get_attribute("value").strip()
#         last_name = last_name_element.get_attribute("value").strip()

#         # Extract Claim ID (text in the row below "Claim ID")
#         claim_id_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Claim ID')]/parent::tr/following-sibling::tr/td")
#         claim_id = claim_id_element.text.strip() 
#         print(f"Claim ID: {claim_id}")

#         descr = 'Quigley Trust Claim Form'
#         status = 'Paid'
#         file_name = f"{last_name}, {first_name} - {descr} - {claim_id} - {status}.pdf"
#         print(f"Downloading {file_name}...")
#         if claim_actions_dropdown:
#             select = Select(claim_actions_dropdown)
#             select.select_by_visible_text("Print Claim Form")  # Select "Print Claim Form"
#             print("Selected 'Print Claim Form'.")
#             go_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Go']")))
#             go_button.click()
        
#         time.sleep(3)  # Wait for popup/download

#         download_folder = r"C:\Users\andrew.cabaj\Downloads"
#         destination = os.path.join(r"T:\LEW - Claim Form Document Retention\Verus - Quigley\Paid", file_name)

#         # Wait for the file to download
#         timeout = 30
#         start_time = time.time()
#         downloaded_file = None

#         while time.time() - start_time < timeout:
#             files = os.listdir(download_folder)
#             pdfs = [f for f in files if f.endswith(".pdf") and not f.endswith(".crdownload")]
#             if len(pdfs) == 1:
#                 downloaded_file = os.path.join(download_folder, pdfs[0])
#                 break
#             time.sleep(1)

#         # Rename and move the file
#         if downloaded_file:
#             try:
#                 shutil.move(downloaded_file, destination)
#                 print(f"File renamed and moved to: {destination}")
#             except FileExistsError:
#                 print(f"File already exists: {destination}")
#             except Exception as e:
#                 print(f"Move failed: {e}")
#         else:
#             print("PDF download timed out or multiple files present.")

#         pdf_windows = [w for w in gw.getWindowsWithTitle("Untitled - Google Chrome") if w.visible]

#         if pdf_windows:
#             pdf_window = pdf_windows[0]
#             time.sleep(1)  # Optional, gives time for the window to activate

#             # Close the window directly
#             pdf_window.close()
        
#         time.sleep(1)
        
#         driver.back()
#         time.sleep(1)
#         driver.back()
#         time.sleep(1)

# current_page_group = 0
# for page_num in range(1, 53):
#     try:
#         current_page_group = go_to_page(page_num, current_page_group)
#         process_claims_on_page()
#     except Exception as e:
#         print(f"Error on page {page_num}: {e}")
#         continue

# driver.back()  # Navigate back to the first table page
# wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'first-table')]")))
print("Back to the main table.")

print("Finished processing all claims on this page.")