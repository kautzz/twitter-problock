"""
twitter-problock (WIP)
scrape your twitter account for promoted content and block the source account
"""

import secrets

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()
browser.get(secrets.url)
browser.implicitly_wait(3)

assert secrets.target in browser.title

username_input = browser.find_element(By.NAME, 'session[username_or_email]')
username_input.send_keys(secrets.username)

password_input = browser.find_element(By.NAME, 'session[password]')
password_input.send_keys(secrets.password + Keys.RETURN)

timeline = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='primaryColumn']")))
print(timeline)

#TODO promoted_tweet = timeline.find_element_by_xpath("//*[contains(text(), 'Promoted')]")

print('!Successful Run')
browser.quit()

#end
