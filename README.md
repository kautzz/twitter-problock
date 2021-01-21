# twitter-problock (MVP)

## Scrape your twitter account for promoted content and block the source. You Pay - I Block!

### Note, Read This:

* scraping and automating things on twitter are not allowed according to their [TOS](https://twitter.com/en/tos)
* there is a good chance that your account gets banned!
  * seriously, only use this tool if you're okay with loosing your account!

#### I'm not responsible for your account getting shut down! You have been warned!!!

### What This Tool Is Doing:

* use selenium to drive a browser ✓
* log in to twitter account ✓
* scrape timeline ✓
* find any tweet marked with "promoted" ✓
* block the account that promoted the tweet by clicking more > block @user > confirm ✓

### Output Sample:

```
[☩] Loading Target: XXX
[⚷] Logged In As User: XXX
===============================
[⚲] No Promoted Content Found In Timeline
[⬇] Scrolling To Lazy Load Tweets
-------------------------------
[⚠] Promoted Tweet Found!
[⊘] Blocking User: @XYZ
[✝] R.I.P
[☭] Blocked 1/1 Promoters
===============================
[☑] End Of Program
```

### Background:

Twitter has been ramping up the amount of promoted tweets in my timeline recently. I don't like ads, most of the time they are not relevant, they totally mess up my doom scrolling experience. I hate when people pay money to try to get my attention - I started blocking them, manually.

![Original Tweet](https://github.com/kautzz/twitter-problock/blob/master/tweet.png?raw=true)


This has been fun for a while and oddly comforting whenever I hit that block button buuut automation, b*tch!


### Initial Ideas That Did Not Work:

* use the twitter API to add promoting accounts to the block list - you have to apply for an API key, even if I get one... other ppl using problock might not be so lucky. API keys could also be revoked...

* using a headless browser w/o JavaScript (mechanicalsoup)

```html
<h1>JavaScript is not available.</h1>
<p>We’ve detected that JavaScript is disabled in this browser. Please enable JavaScript or switch to a supported browser to continue using twitter.com. You can see a list of supported browsers in our Help Center.</p>
```

* using the API to retrieve the timeline as the response [does not contain promoted tweets](https://stackoverflow.com/questions/54081154/twitter-api-how-to-retrieve-timeline-including-promoted-or-sponsored-tweets)
