from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import datetime
import re


def create_db_entry(link, title, cl_id, screenshot_path, time_posted, location, time_scraped):
    entry = {
        'link': link,
        'title': title,
        'cl_id': cl_id,
        'screenshot_path': screenshot_path,
        'time_posted': time_posted,
        'location': location,
        'time_scraped': time_scraped
    }
    return entry


def browser_setup():
    firefox_option = Options()
    firefox_option.add_argument('--headless')
    browser = webdriver.Firefox(options=firefox_option)
    browser.implicitly_wait(1)
    return browser


def translate_html_elements(timestamp: str, browser):
    listings = []
    delay = 5  # seconds
    beforePageLoad = datetime.datetime.now()
    print(beforePageLoad.strftime("%H:%M:%S"), " - Starting page load ")
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cl-search-result')))
        pass
    except TimeoutException:
        pass

    afterPageLoad = datetime.datetime.now()
    delta = afterPageLoad - beforePageLoad
    print(afterPageLoad.strftime("%H:%M:%S"),
          " - Page loaded, took ", delta.seconds, 's')

    free_elements = browser.find_elements(
        by=By.CLASS_NAME, value='cl-search-result')
    for el in free_elements:
        a_tag = el.find_element(By.CLASS_NAME, 'posting-title')
        title = a_tag.text
        link = a_tag.get_attribute('href')
        cl_id = link.split(sep='/')[-1].removesuffix('.html')
        meta_string = el.find_element(by=By.CLASS_NAME, value='meta').text
        posted_time, location = meta_string.split(sep='·')

        result = create_db_entry(link=link, title=title, cl_id=cl_id, screenshot_path='',
                                 time_posted=posted_time, location=location, time_scraped=timestamp)
        listings.append(result)
    return listings


def validate_url(url):
    # check if acceptable search query for craiglist (else the algorithm runs forever)
    pattern = r'^https://\w+\.craigslist\.org/search/.*$'


    passed = True 
    if not re.match(pattern, url):
        passed = False 
    if 'query' not in url:
        print(f"Wrong url. The url must include 'query' parameter")
        passed = False 

    return passed 



def scrape(urls, hour_limit, minute_limit):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = {}
    

    for url in urls:
        browser = browser_setup()
        browser.get(url)
        try:
            listings = translate_html_elements(timestamp, browser=browser)
            listings = [listing for listing in listings if
                        is_recent_listing(listing['time_posted'], hour_limit, minute_limit)]
            results[url] = listings
        except Exception as exc:
            results[url] = {'error': str(exc)}
        browser.quit()

    return results


def is_recent_listing(timestamp_str, hour_limit, minute_limit):
    mins_pattern = r'(\d+)\s+(mins?)\s+ago'
    hours_pattern = r'(\d+)h\s+ago'

    mins_match = re.search(mins_pattern, timestamp_str)
    hours_match = re.search(hours_pattern, timestamp_str)

    if mins_match:
        minutes_ago = int(mins_match.group(1))
        return minutes_ago <= minute_limit
    elif hours_match:
        hours_ago = int(hours_match.group(1))
        return hours_ago <= hour_limit
    else:
        return False
