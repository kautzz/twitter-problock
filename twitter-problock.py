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

browser = webdriver.Firefox()
# !!! todo learn about browser settings

# Helper for waiting until page has loaded
class PageLoaded(object):
  def __call__(self, browser):
    if browser.execute_script("return document.readyState") == "complete":
      print('[Document Ready]')
      return True
    else:
      print('[Waiting For Page To Load]')
      return False

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

print('[Logging In As: ' + secrets.username + ']')
WebDriverWait(browser, 10).until(PageLoaded())

# TODO wait for page to load properly instead of just sleeping
time.sleep(10)


# Scroll Loop to get more lazy loaded tweets
for e in range(10):
  browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  print('[Lazy Load: ' + str(e+1) + ']')

  #TEMPORARY
  time.sleep(3)

# Select Timeline
WebDriverWait(browser, 10).until(PageLoaded())
timeline = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='primaryColumn']")))

promoted_tweet = timeline.find_element_by_xpath(".//*[contains(text(), 'Promoted')]")
print(promoted_tweet.get_attribute('outerHTML'))

#promoter_username = browser.find_element(with_tag_name("input").above(passwordField))


print('[End Of Program]')
#browser.quit()
