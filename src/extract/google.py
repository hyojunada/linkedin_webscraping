from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict

import re
import time

def open_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.google.com/")
    return driver


def get_linkedin_profile_urls(driver, query, end=10, sleep_time=3):
    """
    get linkedin profile urls from google search
    input:
        driver: selenium driver
        query: query for searching starts with site:linkedin.com/in/ 
        end: define how many urls we want
    output:
        linkedin_profile_urls: list of linkedin profile urls in string
    """
    
    linkedin_profile_urls = []
    # find the search section of google
    search_input = driver.find_element_by_name('q')
    search_input.clear()
    # search query 
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
    
    #result stats, get how many results that google estimates
    result_stats = driver.find_element_by_id("result-stats").text
    result_num = re.findall(r'About (\d+(?:,\d+)?) results', result_stats)[0]
    result_num = int(result_num.replace(',', ''))
    
    # iterate until the length of list meets our goal
    page_num = 1
    while len(linkedin_profile_urls) < end:
        try:
            time.sleep(3*sleep_time) # adding sleep time so that google doesn't reject us
            # get profiles under class='r'
            profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
            linkedin_profile_urls.extend([p.get_attribute('href') for p in profiles])
            linkedin_profile_urls = list(set(linkedin_profile_urls))
            # if the list is larger than our goal, cut rest of it off
            if len(linkedin_profile_urls) > end:
                linkedin_profile_urls = linkedin_profile_urls[:end]
                break
            # scroll down to the end of page like humam
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
            time.sleep(sleep_time)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(sleep_time)
            driver.execute_script("window.scrollTo(0, 3*document.body.scrollHeight/4);")
            time.sleep(sleep_time)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_time)
            # go to the next page
            # keep track of page number so when google goes to captcha we can restart at the page we lost
            page_num += 1
            driver.find_element_by_id("pnnext").click()
        except:
            # if google thinks we are going to fast, sleep it off. usually we need to refresh the driver
            # need a better way 
            print(len(linkedin_profile_urls))
            time.sleep(10*sleep_time)
            print('restart')
            driver.get("https://www.google.com/")
            search_input = driver.find_element_by_name('q')
            search_input.clear()
            # search query 
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            driver.find_element_by_id("pnnext").click()
            driver.find_element_by_xpath('//a[@aria-label="Page {}"]'.format(page_num)).click()
            continue
    return linkedin_profile_urls, result_num