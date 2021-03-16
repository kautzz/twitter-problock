# coding=utf-8
#!/usr/bin/env python3

"""
twitter-problock (MVP)
Scrape your twitter account for promoted content and block the source. You Pay - I Block!
"""

import secrets

import time
import datetime
import simpleaudio as sa
import logging as log

import argparse
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# Read Config File
config = ConfigParser()
config.read('settings.ini')

# Command Line Options
parser = argparse.ArgumentParser(description='Scrape your twitter account for promoted content and block the source. You Pay - I Block!')
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()
if args.verbose:
    log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


# Set up selenium browser window
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", config.get('main', 'useragent'))
browser = webdriver.Firefox(profile)
browser.set_window_position(config.getint('browser_window', 'pos_x'), config.getint('browser_window', 'pos_y'))
browser.set_window_size(config.getint('browser_window', 'width'), config.getint('browser_window', 'height'))


# Saves browser window size and position to the config when you move the window
def update_browser_window_config():

    log.info('Checking For Browser Window Changes')
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
        with open('settings.ini', 'w') as f:
            config.write(f)
            log.info('Browser Window Config Written')


# Plays a notification sound when a user has been blocked if enabled in config
def play_notification_sound():
    log.info('Playing Notification Sound If Enabled')
    if config.getboolean('main', 'sound_enabled') == True:
        wave_obj = sa.WaveObject.from_wave_file("src/notification.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()


# Wait until content of the page has loaded completly
def wait_for_pageload():
    log.info('Waiting For Pageload')
    start_time = datetime.datetime.now()

    try:
        WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "//div[@role='progressbar']/following::div[contains(@style, '26px')]")))
    except:
        log.info('Could Not Trigger Loading New Content!')
        return

    try:
        WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@role='progressbar']/following::div[contains(@style, '26px')]")))
    except:
        log.info('Timed Out Waiting For New Content!')
        return 0

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds()

    log.info('New Content Loaded. Took: ' + str(execution_time) + 'seconds')
    return 1


# Log in to twitter with creds provided in secrets file
def login():
    log.info('Logging In')
    browser.get(secrets.url)
    print('[☩] Loading Target: ' + secrets.url)
    time.sleep(1)
    assert secrets.target in browser.title

    username_input = browser.find_element(By.NAME, 'session[username_or_email]')
    username_input.send_keys(secrets.username)
    password_input = browser.find_element(By.NAME, 'session[password]')
    password_input.send_keys(secrets.password + Keys.RETURN)

    #time.sleep(60) # give me some time to manually enter the second factor
    print('[☑] Logged In As User: ' + secrets.username)

    login_result = wait_for_pageload()
    timeline = browser.find_element(By.XPATH, "//div[@data-testid='primaryColumn']")

    print('')
    return timeline


# Search for any tweets in the timeline that are tagged with promoted
def search_promoted(timeline):
    log.info('Searching Timeline For Promoted Content')
    try:
        promoted = timeline.find_element(By.XPATH, ".//*[contains(text(), 'Promoted')]//ancestor::div[4]")
        print('-------------------------------')
        print('[⚠] Promoted Tweet Found!')
        return promoted

    except NoSuchElementException:
        return None


# Block the user that created the promoted tweet
def block_user(promoted):
    log.info('Blocking Promoter')
    promoter = promoted.find_element(By.XPATH, ".//*[contains(text(), '@')]")
    print('[⊘] Blocking User: ' + promoter.get_attribute('innerHTML'))

    try:
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, ".//div[@data-testid='caret']"))).click()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='block']"))).click()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='confirmationSheetConfirm']"))).click()
    except Exception as e:
        log.error('Could Not Block Promoter: ' + e)
        return False

# Scroll down to lazy load more tweets
def load_more_tweets():
    log.info('Scrolling To Lazy Load Tweets')
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    load_result = wait_for_pageload()

    if load_result == 1:
        timeline = browser.find_element(By.XPATH, "//div[@data-testid='primaryColumn']")
        return timeline


# Do a page reload instead of lazy loading to get more tweets
def refresh_page():
    log.info('Reloading Page')
    browser.refresh()
    refresh_result = wait_for_pageload()

    timeline = browser.find_element(By.XPATH, "//div[@data-testid='primaryColumn']")
    return timeline


def main():

    block_target = config.getint('main', 'blocks')
    blocked_users = 0
    lazy_loads = 0

    timeline = login()

    while blocked_users < block_target:

        promoted = search_promoted(timeline)

        if promoted is not None:
            block_result = block_user(promoted)
            if block_result is not False:
                blocked_users += 1
                print('[☭] Blocked ' + str(blocked_users) + '/' + str(block_target) + ' Promoters')
                print('===============================')
                play_notification_sound()

            timeline = refresh_page()

        else:
            log.info('No Promoted Content Found In Timeline')
            load_result = load_more_tweets()
            if load_result is not None:
                timeline = load_result
                lazy_loads += 1
                log.info('Number Of Lazy Loads Before Pagerefresh: ' + str(lazy_loads))
            else:
                timeline = refresh_page()
                lazy_loads = 0

        update_browser_window_config()
        log.info('****************************************')
        time.sleep(1) # just for good measure

if __name__ == "__main__":
    main()

print('[☑] End Of Program')
browser.quit()
