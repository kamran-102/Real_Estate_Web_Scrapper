from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from time import sleep
import chromedriver_autoinstaller
import pandas as pd
import random 
import string
import glob
import os
import io
import re

tax_year_input = '2023'

# The code to download csv file to target directory
# Ensure the download directory exists
download_dir = os.path.join(os.getcwd(), "TD_files")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# setting download directory
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,  # Set the download directory to the case_files directory
    "download.prompt_for_download": False,  # Disable the download confirmation prompt
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True  # Enable safe browsing to avoid security warnings
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")
chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://county-taxes.net/lake/lake/reports/real-estate')
sleep(5)

# Locate the iframe using the src attribute
iframe = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'https://county-taxes.net/iframe-taxsys/lake.county-taxes.com/govhub/reports/real-estate')]"))
)

# Switch to the iframe
driver.switch_to.frame(iframe)
sleep(2)

select_button = driver.find_element(By.XPATH, """//*[@id="selected-report-filter"]""").click()
sleep(1)
unpaid_tax_button = driver.find_element(By.XPATH, """//*[@id="422"]""").click()
sleep(5)

tax_year_button = driver.find_element(By.XPATH, """//*[@id="tax_year"]""").send_keys(tax_year_input)
sleep(1)
search_button = driver.find_element(By.XPATH, """//*[@id="run-search"]""").click()
sleep(4)

download_csv_button = driver.find_element(By.XPATH, """//*[@id="report_results"]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/button/i""")
if download_csv_button:
    download_csv_button.click()
    sleep(2)
    download = driver.find_element(By.XPATH, """//*[@id="download-report"]""").click()
    print(f"The csv file has been downloaded")
    sleep(30)
    driver.quit()
else:
    print(f"The record corresponding to the target year {tax_year_input} doesn't exist")
    driver.quit()


# Open the downloaded Unpaid_Taxes csv
dir = 'TD_files'
for file in os.listdir(dir):
    file_path = os.path.join(dir, file)
df = pd.read_csv(file_path)
df = df.filter(items = ['Tax Yr', 'Account Number', 'Account Status',
       'Balance Amount','Owner Name', 'Billing Address Lines', 'Billing Address City',
       'Billing Address State', 'Billing Address ZIP']) 

# Code to extract property data as per requirements
df_length = df.shape[0]
for i in range(df_length):
    account_number = df['Account Number'][i]
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://county-taxes.net/lake/property-tax')
    sleep(30)  
    try:
        search_button = driver.find_element(By.CSS_SELECTOR, '[id^="typeahead-input-"]')
        actions = ActionChains(driver)
        actions.move_to_element(search_button)
        actions.click()
        actions.send_keys(account_number).send_keys(Keys.ENTER).perform()
    except:
        print(f"Record corresponding to Account_Number {account_number} doesn't exist")
        break
    property_page_url = driver.current_url
    iframe1 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='govhub/property-tax']"))
    )
    iframe_id = iframe1.get_attribute("id")
    driver.switch_to.frame(driver.find_element(By.ID,iframe_id))
    sleep(1)
    owner_name = driver.find_element(By.XPATH, """//*[@class='owner']""")
    if owner_name:
        df.at[i, 'Owner Name'] = owner_name.text
    sleep(1)
    property_address = driver.find_element(By.XPATH, """/html/body/div[2]/main/section/div[2]/div[2]/div[2]/div[2]""")
    if property_address:
        df.at[i, 'Property Address'] = property_address.text
    sleep(2)
    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cells = row.find_elements(By.XPATH, ".//td[@colspan='3']")
        if cells:
            for cell in cells:
                Amount_due = cell.text.split(":")[-1]
                Amount_due = Amount_due.strip()
                df.at[i,'Balance Amount'] = Amount_due
    sleep(1)
    Property_appraiser_redirect = driver.find_element(By.XPATH, """/html/body/div[2]/main/section/div[2]/div[2]/div[3]/div[3]/a""").click()
    sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    sleep(1)
    # For Scraping person info
    record_table = driver.find_element(By.XPATH, """//*[@id="content"]/div[4]/table""")
    record_table_rows = record_table.find_elements(By.TAG_NAME, 'tr')[:2]
    data = {}
    for row in record_table_rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        for j in range(0, len(cells), 2):
            key = cells[j].text.strip(':')
            value = cells[j + 1].text
            data[key] = value
    sleep(2)
    # For scraping property info
    property_table = driver.find_element(By.XPATH, """//*[@id="resBldgs"]/div[2]/table""")
    table_rows = property_table.find_elements(By.TAG_NAME, 'tr')
    property_results = {}
    for row in table_rows[:1]:
        cells = row.find_elements(By.XPATH, ".//td[@colspan='3']")[1:2]
        for cell in cells:
            # Split the text content into individual items
            items = cell.text.split()
            # Parse and store the data in the dictionary
            property_results["Year Built"] = items[2]
            property_results["Total Living Area"] = items[6]
            property_results["Central A/C"] = items[9]
            property_results["Fireplaces"] = items[11]
            property_results["Bedrooms"] = items[13]
            property_results["Full Bathrooms"] = items[16]
            property_results["Half Bathrooms"] = items[19]
    google_map_link = driver.get("https://www.google.com/maps/")
    sleep(5)
    p_address_input = driver.find_element(By.XPATH, """//*[@id="searchboxinput"]""")
    ad = df.loc[1,'Billing Address Lines': 'Billing Address ZIP'].values
    ad = ' '.join(ad)
    p_address_input.send_keys(ad)
    p_address_input.send_keys(Keys.ENTER)
    sleep(4)
    property_image_link = driver.current_url
    new_data = {
        'Parcel Number': data.get('Parcel Number'),
        'Year Built': property_results.get('Year Built'),
        'Total Living Area': property_results.get('Total Living Area'),
        'Central A/C': property_results.get('Central A/C'),
        'Fireplaces': property_results.get('Fireplaces'),
        'Bedrooms': property_results.get('Bedrooms'),
        'Full Bathrooms': property_results.get('Full Bathrooms'),
        'Half Bathrooms': property_results.get('Half Bathrooms'),
        'Property Page URL': property_page_url,
        'Property Image Link': property_image_link
    }

    # Append the dictionary as a new row to the DataFrame
    for key, value in new_data.items():
        df.at[i, key] = value
    df.to_csv("unpaid_taxes.csv", index = False)

    driver.quit()
        
        
                
    