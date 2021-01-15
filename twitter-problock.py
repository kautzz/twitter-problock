"""
twitter-problock (WIP)
scrape your twitter account for promoted content and block the source account
"""

import secrets
import mechanicalsoup

fake_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
url = "https://mobile.twitter.com/login"

browser = mechanicalsoup.StatefulBrowser(user_agent=fake_agent)
browser.open(url)

print(browser.page)
