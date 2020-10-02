import dill as pickle

from argparse import ArgumentParser
import os
import sys
import ipdb
###Local###
src_dir = os.path.abspath(os.path.join('src'))
sys.path[0] = src_dir
import connect.google as google

BASIC_QUERY = 'site:linkedin.com/in/ AND "interaction designer" AND "Chicago"'

def main(args):
    query = args.query
    if query == '':
        query = BASIC_QUERY

    driver = google.open_driver()
    linkedin_profile_urls, result_num = google.get_linkedin_profile_urls(driver, query, args.end)
    
    result_dir = os.path.abspath(args.result_dir)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    f_path = os.path.join(result_dir, 'linkedin_profiles.pkl')
    with open(f_path, "wb") as fp:   #Pickling
        pickle.dump(linkedin_profile_urls, fp)
    
    driver.close()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('result_dir', action='store', default='result/')
    parser.add_argument('--linkedin_id', action='store', help='Linkedin ID', default='')
    parser.add_argument('--linkedin_pw', action='store', default='',help='Linkedin PW')
    
    args = parser.parse_args()

    main(args)



