import dill as pickle

from argparse import ArgumentParser
import os
import sys
import ipdb
###Local###
src_dir = os.path.abspath(os.path.join('src'))
sys.path[0] = src_dir
from profiles import open_driver, get_linkedin_profile_urls

BASIC_QUERY = 'site:linkedin.com/in/ AND "interaction designer" AND "Chicago"'

def main(args):
    num_profiles = int(args.end)
    query = args.query
    if query == '':
        query = BASIC_QUERY

    driver =open_driver()
    linkedin_profile_urls, result_num = get_linkedin_profile_urls(driver, query, num_profiles)
    
    result_dir = os.path.abspath(args.result_dir)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    f_path = os.path.join(result_dir, 'linkedin_profiles.pkl')
    with open(f_path, "wb") as fp:   #Pickling
        pickle.dump(linkedin_profile_urls, fp)
    
    driver.close()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('query', action='store', default=query =  'site:linkedin.com/in/ AND "interaction designer" AND "Chicago"')
    parser.add_argument('result_dir', action='store', default='result/')
    parser.add_argument('--end', action='store', help='number of profiles', default=10)
    
    args = parser.parse_args()

    main(args)



