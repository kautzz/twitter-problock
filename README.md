# twitter-problock (WIP)

## Scrape your twitter account for promoted content and block the source. You Pay - I Block!

### Note:

* scraping and automating things on twitter are not allowed according to [TOS](https://twitter.com/en/tos)
* there is a good chance that your account might get banned!
  * seriously, only use this tool if you're okay with loosing your account!

## I'm not responsible for your account getting banned! You have been warned!!!

### Todo:

* use selenium to drive a browser ✓
* log in to twitter account ✓
* scrape timeline (highly illegal, I know...) ✓
* find any tweet marked with "promoted" ✓
* block the account that promoted the tweet by clicking more > block @user > confirm
* clean this up and make it more reliable

### Initial Ideas That Did Not Work:

* use the twitter API to add promoting accounts to the block list - you have to apply for an API key, even if I get one... other ppl using problock might not be so lucky. API keys could also be revoked...

* using a headless browser w/o JavaScript (mechanicalsoup)

```html
<h1>JavaScript is not available.</h1>
<p>We’ve detected that JavaScript is disabled in this browser. Please enable JavaScript or switch to a supported browser to continue using twitter.com. You can see a list of supported browsers in our Help Center.</p>
```

* using the API to retrieve the timeline as the response [does not contain promoted tweets](https://stackoverflow.com/questions/54081154/twitter-api-how-to-retrieve-timeline-including-promoted-or-sponsored-tweets)
