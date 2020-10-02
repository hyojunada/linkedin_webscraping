from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict

import re
import time


def login_linkedin(driver, linkedin_id, linkedin_pw):
    driver.get('https://www.linkedin.com')
    driver.find_element_by_xpath('//a[text()="Sign in"]').click()
    time.sleep(10)
    username_input = driver.find_element_by_name('session_key')
    username_input.send_keys(linkedin_id)

    password_input = driver.find_element_by_name('session_password')
    password_input.send_keys(linkedin_pw)
    driver.find_element_by_xpath('//button[text()="Sign in"]').click()
    return driver

def get_basic_info(driver, profile):
    #linkedin url
    ln_url = profile
    #name 
    name = driver.find_element_by_xpath('//ul//li[@class="inline t-24 t-black t-normal break-words"]').text
    # current title
    title = driver.find_element_by_xpath('//h2[@class="mt1 t-18 t-black t-normal break-words"]').text
    # location
    location = driver.find_element_by_xpath('//ul//li[@class="t-16 t-black t-normal inline-block"]').text
    return name, title, location


def get_contacts(driver):
    contact_link = driver.find_element_by_xpath('//a[@data-control-name="contact_see_more"]')
    contact_link.click()
    time.sleep(3)
    contacts = driver.find_elements_by_xpath("//a[contains(@class, 'pv-contact-info__contact-link')]")#.get_attribute('href')
    contacts = [i.get_attribute('href') for i in contacts]
    other_contacts = [i for i in contacts if 'linkedin' not in i and '@' not in i]
    emails = [i.replace('mailto:', '') for i in contacts if '@' in i]
    driver.find_element_by_xpath('//button[@aria-label="Dismiss"]').click()
    try:
        email = emails[0]
    except IndexError:
        email = None
    return other_contacts, email
    