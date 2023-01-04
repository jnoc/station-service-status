import requests
import tweepy
import json
import datetime

def client():
    twitter_token = "update to yours"
    twitter_token_secret = "update to yours"
    twitter_app_consumer_key = "update to yours"
    twitter_app_consumer_secret = "update to yours"

    auth = tweepy.OAuthHandler(twitter_app_consumer_key, twitter_app_consumer_secret)
    auth.set_access_token(twitter_token, twitter_token_secret)
    api = tweepy.API(auth)
    tweet = api.update_status(status=output())
    print("Executed", datetime.datetime.now().strftime("%X"))
    return tweet
    
def getStationLines():
    # sID is the station ID from TFL 
    sID = "910GWATRLMN" # London Waterloo
    app_key = "your tfl key"
    r = requests.get("https://api.tfl.gov.uk/StopPoint/ServiceTypes?id=" + sID + "&app_key=" + app_key)
    rjson = json.loads(r.text)
    
    lines = []
    for response in rjson:
        if response.get("lineName"):
            lines.append(response.get("lineName"))
        else:
            pass
    return lines
    
def getLineStatus():
    services = getStationLines()
    services = ','.join(services)
    app_key = "your tfl key"
    r = requests.get("https://api.tfl.gov.uk/Line/" + services + "/Status?app_key=" + app_key)
    rjson = json.loads(r.text)
    
    lines = []
    status = []
    for response in rjson:
        if response.get("name"):
            lines.append(response.get("name"))
        if response.get("lineStatuses")[0].get("statusSeverityDescription"):
            status.append(response.get("lineStatuses")[0].get("statusSeverityDescription"))
        else:
            pass
    return lines + status
    
def output():
    list = getLineStatus()
    length = len(list)
    mindex = length // 2
    lines = list[:mindex]
    status = list[mindex:]
    # Reducing characters for 'South Western Railway'
    # lines = [s.replace(' Railway', '') for s in lines]
    
    output = "Station rail status at: "
    output += datetime.datetime.now().strftime("%H:%M %d %b") + "\n\n"
    for i in range(len(lines)):
        if status[i] == "Good Service":
            output += lines[i] + ": " + status[i] + " ✅\n"
        if status[i] != "Good Service":
            output += lines[i] + ": " + status[i] + " ⚠️\n"
    
    if any(x != "Good Service" for x in status):
        output += "\nCheck your journey before you travel! https://www.nationalrail.co.uk/"
    output += "\n#your_hashtag_here"
    return output
    
client()
