# LinkedIn Publici Profile Webscraping using Python and Selenium
Code to scrape LinkedIn Public profiles

The code scrapes 
- basic info (name, current job title, location)
- contacts
- past experiences
- education 
- spoken language

of LinkedIn public profiles using Selenium

# How to start
I am using Python 3.8 
Install required packages
```
pip install -r requirements.txt
```

Create `.env` file
```
USER_EMAIL=[your linkedin log-in email]
PASSWORD=[your linkedin password]
```
Make sure not to share your log-in information on github or anywhere public

# Scrape Linkedin Profile URLS from Google

# Scrape Linkedin Profile Information
Whether you decide to scrape URLS from Google or make your own URLS, save it using `dill` package as pickle file. It would be list of string URLS. 
Run script on the parent folder
```
python scripts/scrape_linkedin.py [result folder] [path to pickle file]
```
Example
```
python scripts/scrape_linkedin.py ./result ./data/linkedin_profiles.pkl
```
