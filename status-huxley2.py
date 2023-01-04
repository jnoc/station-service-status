import requests
import json
import datetime
from bs4 import BeautifulSoup
import re
import tweepy
from discordwebhook import Discord

# cront tab 0,20,40 0,5-23 * * *

""" Ashtead station (arrivals/departures) checked every 20 minutes with a 60 minute look ahead window. 
Active tweet hours 5am-1am. 🛤️ """

delays = False
delaysVar = ""

def main():
    try:
        global station, delays, delaysVar, current
        # https://github.com/jpsingleton/Huxley2/blob/master/station_codes.csv
        station = "AHD" # can be changed to other station codes ^ 
        # though with bigger staions I'm not sure if you will run into character limits with the delays and cancellations reply tweets
        key = "your national rail datafeeds key" # update with your value
        r = requests.get("http://your url here/all/{0}?timeWindow=60&accessToken={1}".format(station, key)) # update with your value
        rjson = json.loads(r.text)
        
        d = requests.get("http://your url here/delays/{0}?accessToken={1}".format(station, key)) # update with your value
        delaysJson = json.loads(d.text)
        
        serveBoard = False
    
        nowTime = datetime.datetime.now()
        current = nowTime.strftime("%H:%M %d %b")

        tweet = "{} rail status at: {}\n".format(rjson["locationName"], current)

        if rjson["areServicesAvailable"] == True:
            if delaysJson["delays"] == True:
                if delaysJson["totalTrainsDelayed"] > 0:
                    delays = True
                    tweet += "\n⚠️ Train alerts: True"
                    output = [i["isCancelled"] for i in delaysJson["delayedTrains"]]
                    if output.count(True) > 0:
                        tweet += "\n❌ Trains cancelled: {}".format(output.count(True))
                        if delaysJson["totalTrainsDelayed"] - output.count(True) > 0:
                            tweet += "\n⏱️ Trains delayed: {}".format(delaysJson["totalTrainsDelayed"] - output.count(True))
                    else:
                        tweet += "\n⏱️ Trains delayed: {}".format(delaysJson["totalTrainsDelayed"])
                    serveBoard = True
                    delaysVar = delaysJson
                else:
                    tweet += "\n✅ Train alerts: None"
            if delaysJson["delays"] == False:
                tweet += "\n✅ Train alerts: None"
            
            if rjson["nrccMessages"] != None:
                tweet += "\n⚠️ Service alerts: True"
                serveBoard = True
                if "Industrial Action" in nrccOut(rjson["nrccMessages"]): # Added message for Industrial Action 4th Jan 2023
                    tweet += "\n❌ " + nrccOut(rjson["nrccMessages"])

            if rjson["nrccMessages"] == None:
                tweet += "\n✅ Service alerts: None"

            if rjson["busServices"] != None:
                tweet += "\n🚌 Replacement buses: Running"
                serveBoard = True

            if serveBoard == True:
                tweet += "\n\nMore info: https://ojp.nationalrail.co.uk/service/ldbboard/dep/{0}".format(station)
        else:
            tweet += "\nServices are not currently avaliable at this station ❌"
            tweet += "\nMore info: https://ojp.nationalrail.co.uk/service/ldbboard/dep/{0}\n".format(station)

        tweet += "\n\n#{}status".format(station)

        print(tweet)
        return tweet
    except requests.exceptions.RequestException: 
        print("Request Error")
        return "Request Error ❌ <@&965361764596326430>"
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        return "Connection Error ❌ <@&965361764596326430>"

# service alert break down function              
def nrccOut(nrccMsg):
    outputTxT = ""
    output = [i["value"] for i in nrccMsg]
    for i in range(len(output)):
        # search for industrial action
        industrialMatch = re.findall("industrial|Industrial", output[i])
        # search for html tags, if yes then soup if not then output value
        htmlMatch = re.findall("<.+?>", output[i])
        """if len(htmlMatch) != 0:
            soup = BeautifulSoup(output[i], "lxml")
            cleantext = soup.text
            href = soup.find(href=True)
            if href != None:
                href = href['href']
                outputTxT += "{0}\n{1}".format(cleantext, href)
            else:
                outputTxT += "{0}".format(cleantext)
        else:
            outputTxT += "{0}".format(output[i])  """
        if len(industrialMatch) != 0:
            outputTxT += "Industrial Action, please check more info."
    return outputTxT

def discordPing():
    hook = "discord webook that you can use to post the information to a discord server channel" # update with your value
    discord = Discord(url=hook)
    discord.post(
    content=main(),
    username="{} Service Status".format(station),
    avatar_url="https://pbs.twimg.com/profile_images/1295085239367344131/AB26q1l__400x400.jpg"
    )
    if delays == True:
        discord = Discord(url=hook)
        discord.post(
        content=delayed(),
        username="{} Service Status".format(station),
        avatar_url="https://pbs.twimg.com/profile_images/1295085239367344131/AB26q1l__400x400.jpg"
    )

def delayed():
    global delaysVar
    outputMsg = "{0} trains ⏱️ or ❌:\n".format(delaysVar["locationName"])
    delayed = delaysVar["delayedTrains"]
    for i in range(len(delayed)):
        sta = delayed[i]["sta"]
        to = delayed[i]["destination"][0]["locationName"]
        if delayed[i]["isCancelled"] == True:
            outputMsg += "\n❌ {0} to {1}".format(sta, to)
        else:
            outputMsg += "\n⏱️ {0} to {1}".format(sta, to)
    outputMsg += "\n\n#{}status".format(station)
    print(outputMsg)
    if len(outputMsg) <= 280: # twt char limit
        return outputMsg
    else:
        errMsg = "{0} trains delayed or cancelled\n\nToo many to list, see more info.".format(delaysVar["locationName"])
        return errMsg

def client():
    token = "twitter token" # update with your value
    token_secret = "twitter token secret" # update with your value
    consumer_key = "twitter consumer key" # update with your value
    consumer_secret = "twitter consumer secret" # update with your value
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    tweet = api.update_status(status=main())
    if delays == True:
        tweetId = tweet.id
        replyTweet = api.update_status(status=delayed(), in_reply_to_status_id = tweetId , auto_populate_reply_metadata=True)
    print("Executed", datetime.datetime.now().strftime("%X"))
    return tweet

if __name__ == "__main__":
    #main()
    client()
    discordPing()
