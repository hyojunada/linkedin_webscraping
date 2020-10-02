from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict
import datetime

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

def get_contacts(driver, profile, name):
    contact_data = []
    contact_link = driver.find_element_by_xpath('//a[@data-control-name="contact_see_more"]')
    contact_link.click()
    time.sleep(3)
    contacts = driver.find_elements_by_xpath("//a[contains(@class, 'pv-contact-info__contact-link')]")#.get_attribute('href')
    contacts = [i.get_attribute('href') for i in contacts]
    other_contacts = [i for i in contacts if 'linkedin' not in i and '@' not in i]
    emails = [i.replace('mailto:', '') for i in contacts if '@' in i]
    driver.find_element_by_xpath('//button[@aria-label="Dismiss"]').click()
    for contact in emails+other_contacts:
        contact_data.append([profile, name, contact])
    return contact_data

def get_start_end_date(duration):
    duration = duration.replace('Dates Employed\n','')
    start_date, end_date = duration.split(' – ')
    start_date = datetime.datetime.strptime(start_date, '%b %Y').date()
    if end_date == 'Present':
        end_date = datetime.datetime.today().date()
    else:
        end_date = datetime.datetime.strptime(end_date, '%b %Y').date()
    return start_date, end_date

def get_experience(driver, profile, name):
    experience_data = []
    exp_section = driver.find_element_by_xpath('//section[@id="experience-section"]')
    experiences = exp_section.find_elements_by_xpath('.//li[@class="pv-entity__position-group-pager pv-profile-section__list-item ember-view"]')
    for i, exp in enumerate(experiences):
        try: #when one only had one position
            company = exp.find_element_by_xpath('.//a[@data-control-name="background_details_company"]')
            job_title = company.find_element_by_tag_name('h3').text.replace('Company Name\n', '')
            company_name = company.find_element_by_tag_name('img').get_attribute('alt')
            duration = company.find_element_by_xpath('.//h4[contains(@class, "pv-entity__date-range")]').text
            start_date, end_date = get_start_end_date(duration)
            try:
                location = company.find_element_by_xpath('.//h4[contains(@class, "pv-entity__location")]').text.replace('Location\n', '')
            except:
                location = ''
            experience_data.append([profile, name, company_name, job_title, start_date, end_date])
        except: # when there were multiple positions
            company = exp.find_element_by_xpath('.//section[contains(@class,"pv-profile-section")]')
            company_name = company.find_element_by_tag_name('img').get_attribute('alt')
            roles = company.find_elements_by_xpath('.//li[contains(@class, "pv-entity__position")]')
            for r in roles:
                job_title = r.find_element_by_tag_name('h3').text.replace('Title\n', '')
                duration = company.find_element_by_xpath('.//h4[contains(@class, "pv-entity__date-range")]').text
                start_date, end_date = get_start_end_date(duration)
                experience_data.append([profile, name, company_name, job_title, start_date, end_date])

    return experience_data

def get_education(driver, profile, name):
    education_data = []
    education_section = driver.find_element_by_xpath('*//section[@id="education-section"]')
    educations = education_section.find_elements_by_xpath('.//li[contains(@class, "pv-education-entity")]')
    for ed in educations:
        school_name = ed.find_element_by_xpath('.//h3[contains(@class, pv-entity__school-name)]').text
        ed_info = [e.text for e in ed.find_elements_by_xpath('.//p[contains(@class, pv-entity)]')]
        degree = [i for i in ed_info if 'Degree Name' in i]
        if len(degree) > 0:
            degree = degree[0].replace('Degree Name\n', '')
        else:
            degree = ''
        fos = [i for i in ed_info if 'Field Of Study' in i]
        if len(fos) > 0:
            fos = fos[0].replace('Field Of Study\n', '')
        else:
            fos = ''
        date_range = [i for i in ed_info if 'Dates attended or expected graduation' in i]
        if len(date_range) > 0:
            date_range = date_range[0].replace('Dates attended or expected graduation\n', '')
            start_year, end_year = date_range.split(' – ')

        else:
            date_range = ''
            start_year = None
            end_year = None

        education_data.append([profile, name, school_name, degree, fos, start_year, end_year])
    return education_data

def get_language(driver):
    try:
        language = driver.find_element_by_xpath('.//div[@aria-labelledby="languages-title"]').text
    except:
        language = ''
    return language

    