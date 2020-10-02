from argparse import ArgumentParser
import os
import sys
import ipdb
from dotenv import load_dotenv
import time
from tqdm import tqdm
import random
import datetime
import pandas as pd
import dill as pickle

###Local###
src_dir = os.path.abspath(os.path.join('src'))
sys.path[0] = src_dir
from profiles import open_driver
import linkedin
import paths



def main(args):
    driver = open_driver()
    # get user id and pw
    time.sleep(3)
    load_dotenv(dotenv_path=os.path.join(paths.repository_root, '.env'))
    USER_ID = os.getenv('USER_EMAIL')
    USER_PASSWORD = os.getenv('PASSWORD')
    if not USER_ID:
        USER_ID = args.linkedin_id
        USER_PASSWORD = args.linkedin_pw

    driver = linkedin.login_linkedin(driver, USER_ID, USER_PASSWORD)
    with open(args.data_file, 'rb') as fp:
        profile_urls = pickle.load(fp)
    
    basic_info_data_all = []
    contacts_data_all = []
    experience_data_all = []
    education_data_all = []
    language_data_all = []
    for i, profile in tqdm(enumerate(profile_urls)):
        t = random.uniform(1.5,4.5)
        driver.get(profile)
        time.sleep(t)
        name, title, location = linkedin.get_basic_info(driver, profile)
        basic_info_data_all.append([profile, name, title, location])
        time.sleep(t)
        contact_data = linkedin.get_contacts(driver, profile, name)
        contacts_data_all.extend(contact_data)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(2*t)
        experience_data = linkedin.get_experience(driver, profile, name)
        experience_data_all.extend(experience_data)
        driver.execute_script("window.scrollTo(0, 2*document.body.scrollHeight/3);")
        time.sleep(t)
        try:
            education_data = linkedin.get_education(driver, profile, name)
            education_data_all.extend(education_data)
        except: # no education section
            continue
        driver.execute_script("window.scrollTo(0, 3*document.body.scrollHeight/4);")
        time.sleep(t)
        language = linkedin.get_language(driver)
        language_data_all.append([profile, name, language])
        time.sleep(5*t)

    df_basic_info = pd.DataFrame(basic_info_data_all, 
                                columns=['URL', 'Name', 'Title', 'Location'])
    df_contacts = pd.DataFrame(contacts_data_all,
                            columns=['URL', 'Name', 'Contact'])
    df_experience = pd.DataFrame(experience_data_all,
                                columns=['URL', 'Name', 'Company', 'Title', 
                                        'Start Date', 'End Date'])
    df_education = pd.DataFrame(education_data_all,
                                columns=['URL', 'Name', 'Institution', 
                                        'Degree', 'Field of Study', 
                                        'Start Year', 'End Year'])
    df_language = pd.DataFrame(language_data_all,
                            columns=['URL', 'Name', 'Language'])
    # Writing to file
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(os.path.join(args.result_dir, 'Linkedin_data.xlsx'), 
                            engine='xlsxwriter')

    # Write each dataframe to a different worksheet. you could write different string like above if you want
    df_basic_info.to_excel(writer, sheet_name='Basic Info')
    df_contacts.to_excel(writer, sheet_name='Contacts')
    df_experience.to_excel(writer, sheet_name='Experience')
    df_education.to_excel(writer, sheet_name='Education')
    df_language.to_excel(writer, sheet_name='Language')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    writer.close()
    driver.close()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('result_dir', action='store', default='result/')
    parser.add_argument('data_file', action='store', help='File that contains list of linkedin urls')
    parser.add_argument('--linkedin_id', action='store', help='Linkedin ID', default='')
    parser.add_argument('--linkedin_pw', action='store', default='',help='Linkedin PW')
    
    args = parser.parse_args()

    main(args)



