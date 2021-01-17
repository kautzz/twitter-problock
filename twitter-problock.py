"""
twitter-problock (WIP)
scrape your twitter account for promoted content and block the source account
"""

import secrets
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Firefox()
# TODO learn about browser settings

# Helper for waiting until page has loaded
class PageLoaded(object):
    def __call__(self, browser):
        time.sleep(5) # TODO remove this and make the doc.ready work instead
        if browser.execute_script("return document.readyState") == "complete":
          return True
        else:
          print('[Waiting For Page To Load]')
          return False

def login():
    # Load Target Page
    browser.get(secrets.url)
    print('[Loading Target: ' + secrets.url + ']')
    WebDriverWait(browser, 10).until(PageLoaded())
    assert secrets.target in browser.title

    # LOGIN
    username_input = browser.find_element(By.NAME, 'session[username_or_email]')
    username_input.send_keys(secrets.username)
    password_input = browser.find_element(By.NAME, 'session[password]')
    password_input.send_keys(secrets.password + Keys.RETURN)

    print('[Logging In As User: ' + secrets.username + ']')
    WebDriverWait(browser, 10).until(PageLoaded())

def load_tweets():
    # Scroll Loop to get more lazy loaded tweets
    for e in range(1):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('[Lazy Load: ' + str(e+1) + ']')

        time.sleep(2) # TODO make this dynamic

    # Select Timeline
    # TODO choose one of these delays...
    WebDriverWait(browser, 10).until(PageLoaded())
    timeline = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='primaryColumn']")))

    return timeline

def search_promoted(timeline):
    try:
        promoted_tweet = timeline.find_element_by_xpath(".//*[contains(text(), 'Promoted')]")
        print(promoted_tweet.get_attribute('outerHTML'))
        return promoted_tweet

    except NoSuchElementException:
        return None

def block_promoter(promoted_tweet):
    promoter_username = browser.find_element_by_xpath(".//*[contains(text(), '@')]")
    print(promoter_username.get_attribute('outerHTML'))
    print('blocked')

def main():
    login()
    while True:
        timeline = load_tweets()
        promoted_tweet = search_promoted(timeline)
        if promoted_tweet is not None:
            block_promoter(promoted_tweet)
            break
        else:
            print('[No Promoted Content Found. Reloading...]')
            browser.refresh()
            WebDriverWait(browser, 10).until(PageLoaded())


if __name__ == "__main__":
    main()

print('[End Of Program]')
#browser.quit()
