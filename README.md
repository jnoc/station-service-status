# Station service status
A [Tweepy](https://www.tweepy.org/) powered line service bot that pulls data via the [TFL](https://api.tfl.gov.uk/) API which uses the datafeeds from [Network Rail](https://datafeeds.networkrail.co.uk/) for overground information. This is then processed via Tweepy to tweet to Twitter.

## Ashtead Rail bot
![Bot image](https://i.imgur.com/x7UsLnn.png)
This is the bot that I set up for my local station [@AshteadRail](https://twitter.com/AshteadRail). It utilises crontab to execute the python file 5am through to 12:30am, this then repeats on a day to day basis. This was only made for my travel convenience as I commute to and from London daily.
