# twitter-problock

## Scrape your twitter account for promoted content and block the source. You Pay - I Block!

### Note, Read This:

Scraping and automating things on twitter are not allowed according to their [TOS](https://twitter.com/en/tos).
There is a good chance that your account gets banned! Seriously, only use this tool if you're okay with loosing your account!

#### I'm not responsible for your account getting shut down! You have been warned!!!

### Background:

Twitter has been ramping up the amount of promoted tweets in my timeline recently. I don't like ads, most of the time they are not relevant. I hate when people pay money to try to get my attention - I started blocking them, manually.

![Original Tweet](https://github.com/kautzz/twitter-problock/blob/master/tweet.png?raw=true)

This has been fun for a while and oddly comforting whenever I hit that block button. After a while I got addicted, now I need more blocking, mooooaaaaarrrrr! No, I'm not a cheap guy - I would happily pay for twitter pro without ads... if there ever was such a thing.

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

### Does It Actually Work?:

It does. Twitter seems to deliver less promoted content on web-browsers than in the native app so finding promoted tweets and blocking their source with this tool takes quite a while but it steadily grew my list of blocked accounts. As the list got longer and longer I now have to scroll quite a while on my phone to find any promoted tweets :)

### Coming Up / TODO

* make problock more robust i.e. catch more exceptions
* add metrics to see what accounts have been blocked and when
* out of curiosity add some sort of analytics to the tool to see who is promoting what at what time of the day
* any other ideas?

### Setup (WIP)

* install Firefox
* install geckodriver
* set up python and dependencies (you can use anaconda and the environment file included)
* add your twitter handle and password to the secrets file
* let her rip

### Approaches That Did Not Work:

* using the twitter API to retrieve the timeline as the response [does not contain promoted tweets](https://stackoverflow.com/questions/54081154/twitter-api-how-to-retrieve-timeline-including-promoted-or-sponsored-tweets)

* use the twitter API to add promoting accounts to the block list - you have to apply for an API key, even if I get one... other ppl using problock might not be so lucky. API keys could also be revoked...

* not using selenium but mechanicalsoup or something else

```html
<h1>JavaScript is not available.</h1>
<p>We’ve detected that JavaScript is disabled in this browser. Please enable JavaScript or switch to a supported browser to continue using twitter.com. You can see a list of supported browsers in our Help Center.</p>
```
