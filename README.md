# Station service status
A twitter station bot that uses [Tweepy](https://www.tweepy.org/) library to tweet up to date information about trains running through the target station. This data is pulled from DARWIN via [Huxley2](https://github.com/jpsingleton/Huxley2), then processed in python and pushed to Tweepy.

Please note that `status-tlf-api.py` is an outdated version or version 1 of this bot, this was pulling information via the TFL API, processing via python and pushing to twitter via Tweepy.

## AshteadRail bot

<div align="center">
  <img src="https://i.imgur.com/fIloKQp.png">
</div>

## About `status-huxley2.py`
This is the bot that I set up for my local station [@AshteadRail](https://twitter.com/AshteadRail). It utilises crontab to execute the python file 5am through to 1am, this then repeats on a day to day basis. This was only made for my travel convenience when communting to and from London.

The script is made to output:
- Train Alerts
  - This being any train delays or cancellations.
- Service Alerts
  - This being if there are any National Rail Communication Centre (NRCC) messages for the specified station.
  - If there is industrial action (strikes ect), this is seemingly different from `areServicesAvailable` vs `nrccMessage` field.
- If replacement buses are running.
- If there are any services running.

Here are some example outputs:

### Services running as normal

<div align="center">
  <img src="https://i.imgur.com/WCOfgmp.png">
</div>

### Services have trains delayed or cancelled 
(can be either or both)

<div align="center">
  <img src="https://i.imgur.com/pdkr9L5.png">
</div>

### If there are service alerts via the NRCC

<div align="center">
  <img src="https://i.imgur.com/Rw58Ii6.png">
</div>

### If there is industrial action

<div align="center">
  <img src="https://i.imgur.com/SRwRUlY.png">
</div>

### If there are replacement buses running

<div align="center">
  <img src="https://i.imgur.com/Z5xBxs1.png">
</div>
