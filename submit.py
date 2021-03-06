#!/usr/bin/env python3

import json
import time
from pprint import pprint
from datetime import datetime, timezone
from random import randrange
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

### Variables
#
#

form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSdha1TIwLnaI-e9K_Qqrr4lRIamXH5okJCTuit5nKTlzSJ8kQ/viewform?usp=sf_link'

# if less than or equal to 2: ailment true | 3:30 ratio | (10% chance)
random_has_ailment = randrange(30)
trigger_ailment_less_than_or_equal_to = 2

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
service = Service("./chromedriver")
# driver = webdriver.Chrome('./chromedriver', desired_capabilities=caps, options=chrome_options)

driver = webdriver.Chrome(service=service, options=chrome_options)

### Functions
#
#

def load_page(driver,form_url):
    driver.get(form_url)

def populate_name_text(driver,employee):
    # text_area = driver.find_element_by_xpath("//input[@type='text']")
    text_area = driver.find_element(By.XPATH,"//input[@type='text']")
    text_area_value = employee['attributes']['personalInfo']['firstName'] + " " + employee['attributes']['personalInfo']['lastName']
    if text_area:
        print("Found name field, populating it with: " + text_area_value)
        text_area.click()
        text_area.send_keys(text_area_value)
    else:
        print("No name field found!")
        exit

def click_not_ill_radio_button(driver):
    # radio_button = driver.find_element_by_css_selector('#i12')
    radio_button = driver.find_element(By.CSS_SELECTOR,"#i12")
    if radio_button:
        print("Found not ill radio button, clicking it")
        radio_button.click()
    else:
        print("Not ill radio button not found!")
        exit

def click_not_concerned_radio_button(driver):
    # radio_button = driver.find_element_by_css_selector('#i22')
    radio_button = driver.find_element(By.CSS_SELECTOR,"#i22")
    if radio_button:
        print("Found not concerned radio button, clicking it")
        radio_button.click()
    else:
        print("Not concerned radio button not found!")
        exit

def click_concerned_radio_button(driver):
    # radio_button = driver.find_element_by_css_selector('#i19')
    radio_button = driver.find_element(By.CSS_SELECTOR,"#i19")
    if radio_button:
        print("Found concerned radio button, clicking it")
        radio_button.click()
    else:
        print("Concerned radio button not found!")
        exit

def populate_concern_text(driver,ailment_message):
    # text_area = driver.find_element_by_xpath("//textarea")
    text_area = driver.find_element(By.XPATH,"//textarea")
    if text_area:
        print("Found concern text area, populating it with: " + ailment_message)
        text_area.click()
        text_area.send_keys(ailment_message)
    else:
        print("Concern text area not found!")
        exit

def click_submit(driver):
    # submit_button = driver.find_element_by_css_selector(".appsMaterialWizButtonEl")
    submit_button = driver.find_element(By.CSS_SELECTOR,".appsMaterialWizButtonEl")
    if submit_button:
        print("Found submit button, clicking it\n")
        submit_button.click()
    else:
        print("Submit button not found!")
        exit

### Main
#
#

started = datetime.now(timezone.utc).astimezone().isoformat()
print("\nStarted: " + started +"\n")

print("Reading employee file")
employee_file = open('employees.json',)
employee_data = json.load(employee_file)
employee_file.close()

# pprint(range(len(employee_data)))

print("Reading ailment file\n")
ailments_file = open('ailments.json',)
ailments_data = json.load(ailments_file)
ailments_file.close()

# pprint(range(len(ailments_data)))

employee_list = []

for employee in employee_data:
    has_ailment = False
    employee_details = {'id':None, 'attributes':None}
    employee_details['id'] = employee['id']
    
    if random_has_ailment <= trigger_ailment_less_than_or_equal_to:
        has_ailment = True
        random_ailment = randrange(len(ailments_data[employee['attributes']['personalInfo']['sex']]))
    
    if has_ailment:
        ailment_list = []

        for ailment in ailments_data[employee['attributes']['personalInfo']['sex']]:
            ailment_details = {'id':None, 'message':None}
            ailment_details['id'] = ailment['id']
            ailment_details['message'] = ailment['message']
            ailment_list.append(ailment_details)
        ailment_message = ailment_list[random_ailment]['message']

    employee_details['attributes'] = employee['attributes']
    employee_list.append(employee_details)

    load_page(driver,form_url)
    populate_name_text(driver,employee)

    if has_ailment:
        click_concerned_radio_button(driver)
        populate_concern_text(driver,ailment_message)
    else:
        click_not_ill_radio_button(driver)
        click_not_concerned_radio_button(driver)

    click_submit(driver)
    time.sleep(3)

# pprint(employee_list)

stopped = datetime.now(timezone.utc).astimezone().isoformat()
print("\nStopped: " + stopped + "\n")

### End