# coding=utf-8
#!/usr/bin/env python3

"""
twitter-problock (MVP)
Scrape your twitter account for promoted content and block the source. You Pay - I Block!
"""

import secrets
import time
import random
import simpleaudio as sa

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

# How many promoters should we block today
block_target = config.getint('main', 'blocks')

# Set up selenium browser window
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", config.get('main', 'useragent'))
browser = webdriver.Firefox(profile)
browser.set_window_position(config.getint('browser_window', 'pos_x'), config.getint('browser_window', 'pos_y'))
browser.set_window_size(config.getint('browser_window', 'width'), config.getint('browser_window', 'height'))


def update_browser_window_config():

    # Saves browser window size and position to the config file when you move the window
    window_position = browser.get_window_position(windowHandle ='current')
    window_size = browser.get_window_size(windowHandle ='current')
    save_changes = False

    if window_position['x'] != config.getint('browser_window', 'pos_x'):
        config.set('browser_window', 'pos_x', str(window_position['x']))
        save_changes = True
    if window_position['y'] != config.getint('browser_window', 'pos_y'):
        config.set('browser_window', 'pos_y', str(window_position['y']))
        save_changes = True
    if window_size['width'] != config.getint('browser_window', 'width'):
        config.set('browser_window', 'width', str(window_size['width']))
        save_changes = True
    if window_size['height'] != config.getint('browser_window', 'height'):
        config.set('browser_window', 'height', str(window_size['height']))
        save_changes = True

    if save_changes == True:
        with open('config.ini', 'w') as f:
            config.write(f)
            print('config updated')

def play_notification_sound():
    if config.getboolean('main', 'sound_enabled') == True:
        wave_obj = sa.WaveObject.from_wave_file("notification.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
    else:
        print('audio off')


# Helper for waiting until page has loaded
class PageLoaded(object):
    def __call__(self, browser):
        time.sleep(5) # TODO remove this and make the doc.ready work instead
        if browser.execute_script("return document.readyState") == "complete":
            return True
        else:
            print('[⧖] Waiting For Page To Load')
            return False


def login():

    # Load Target Page
    browser.get(secrets.url)
    print('[☩] Loading Target: ' + secrets.url)
    WebDriverWait(browser, 10).until(PageLoaded())
    assert secrets.target in browser.title

    # Login
    username_input = browser.find_element(By.NAME, 'session[username_or_email]')
    username_input.send_keys(secrets.username)
    password_input = browser.find_element(By.NAME, 'session[password]')
    password_input.send_keys(secrets.password + Keys.RETURN)
    #time.sleep(60) # give me some time to enter the second factor
    print('[⚷] Logged In As User: ' + secrets.username)
    WebDriverWait(browser, 10).until(PageLoaded())

    # Wait for Tweets to load and select the timeline
    timeline = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='primaryColumn']")))

    print('===============================')

    return timeline


def search_promoted(timeline):
    try:
        promoted = timeline.find_element(By.XPATH, ".//*[contains(text(), 'Promoted')]//ancestor::div[4]")
        print('-------------------------------')
        print('[⚠] Promoted Tweet Found!')
        return promoted

    except NoSuchElementException:
        return None


def block_user(promoted):

    promoter = promoted.find_element(By.XPATH, ".//*[contains(text(), '@')]")
    print('[⊘] Blocking User: ' + promoter.get_attribute('innerHTML'))

    time.sleep(1)
    promoted.find_element(By.XPATH, ".//div[@data-testid='caret']").click()
    browser.find_element(By.XPATH, "//div[@data-testid='block']").click()
    browser.find_element(By.XPATH, "//div[@data-testid='confirmationSheetConfirm']").click()
    print('[✝] R.I.P')

def rand_delay():
    time.sleep(random.randint(0,4))

def load_more_tweets():

    rand_delay()
    #print('[⬇] Scrolling To Lazy Load Tweets')
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    WebDriverWait(browser, 10).until(PageLoaded())
    timeline = browser.find_element(By.XPATH, "//div[@data-testid='primaryColumn']")

    return timeline


def refresh_page():

    rand_delay()
    #print('[⟳] Reloading Page')
    browser.refresh()
    WebDriverWait(browser, 10).until(PageLoaded())
    timeline = browser.find_element(By.XPATH, "//div[@data-testid='primaryColumn']")

    return timeline

def main():

    blocked_users = 0
    lazy_loads = 0

    timeline = login()

    while blocked_users < block_target:

        promoted = search_promoted(timeline)

        if promoted is not None:
            block_user(promoted)
            blocked_users += 1

            print('[☭] Blocked ' + str(blocked_users) + '/' + str(block_target) + ' Promoters')
            print('===============================')
            play_notification_sound()

            timeline = refresh_page()
            lazy_loads = 0

        elif lazy_loads < 4:
            #print('[⚲] No Promoted Content Found In Timeline')
            timeline = load_more_tweets()
            lazy_loads += 1

        else:
            #print('[⚲] No Promoted Content Found In Timeline')
            timeline = refresh_page()
            lazy_loads = 0

        update_browser_window_config()

if __name__ == "__main__":
    main()

print('[☑] End Of Program')
browser.quit()
