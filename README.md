# twitter-problock (WIP)

## scrape your twitter account for promoted content and block the source account

### Todo:

* use selenium to log in to twitter account ✓
* scrape timeline (highly illegal, I know...) ✓
* find any tweet marked with "promoted" ✓
* save the name / id of the account that promoted that tweet (✓)
* clean this up and make it more reliable
* use the twitter API to add this account to the block list

### Initial Ideas That Did Not Work:

* using a headless browser w/o JavaScript (mechanicalsoup)

```html
<h1>JavaScript is not available.</h1>
<p>We’ve detected that JavaScript is disabled in this browser. Please enable JavaScript or switch to a supported browser to continue using twitter.com. You can see a list of supported browsers in our Help Center.</p>
```

* using the API to retrieve the timeline as the response [does not contain promoted tweets](https://stackoverflow.com/questions/54081154/twitter-api-how-to-retrieve-timeline-including-promoted-or-sponsored-tweets)
