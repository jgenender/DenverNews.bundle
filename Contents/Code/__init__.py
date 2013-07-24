from cStringIO import StringIO
import re 

ATTRIBUTELISTPATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
ext_x_stream_inf = '#EXT-X-STREAM-INF'

TITLE = 'Denver News' # Your Channel title here
PREFIX = '/video/denvernews' # Change the 'youruniqueidhere' part

ART = '9News-icon.jpg'
ICON = '9News-icon.png'

CH2NEWS_ART = '2News-art.png'
CH2NEWS_ICON = '2News-icon.jpg'
CH2NEWS_LIVESTREAM_SUB = "3486375"
CH2NEWS_SUMMARY = "Live webcasts are available at the following times: \n\nMonday - Friday: 5:00 - 9:00 AM, 7:00 - 8:00 PM\n\nContinuously plays the last broadcasted news at all other times."

CH7NEWS_ART = '7News-art.jpg'
CH7NEWS_ICON = '7News-icon.jpg'
CH7NEWS_URL = "http://stskmghstr01-i.akamaihd.net/hls/live/203185/anvato/master.m3u8"
CH7NEWS_SUMMARY = "Live webcasts are available at the following times: \n\nMonday - Friday: 4:30 - 7:00 AM, 11:00 - 12:00 PM, 5:00 - 5:30 PM, 10:00 - 10:30 PM\n\nSaturday: 7:00 - 9:00 AM, 5:00 - 6:00 PM, 10:00 - 10:30 PM\n\nSunday: 7:00 - 10:00 AM, 5:00 - 6:00 PM, 10:00 - 11:00 PM"

CH9NEWS_ART = '9News-icon.jpg'
CH9NEWS_ICON = '9News-icon.png'
CH9NEWS_URL = "http://b_kusa-f.akamaihd.net/i/KUSA_Live_1@98937/master.m3u8"
CH9NEWS_SUMMARY = "Live webcasts are available at the following times: \n\nMonday - Friday: 4:30 - 9:00 AM, 11:00 - 11:30 PM, 12:00 - 12:30 PM, 4:00 - 5:30 PM, 6:00 - 6:30 PM, 9:00 - 10:30 PM\n\nSaturday - Sunday: 6:00 - 9:00 AM, 5:00 - 6:00 PM, 9:00 - 10:30 PM"

CH31NEWS_ART = 'FOX31-art.jpg'
CH31NEWS_ICON = 'FOX31-icon.jpg'
CH31NEWS_LIVESTREAM_SUB = "3417789"
CH31NEWS_SUMMARY = "Live webcasts are available at the following times: \n\nMonday - Friday: 5:00 - 9:00 AM, 5:00 - 6:00 PM, 9:00 - 10:30 PM\n\nSaturday: 5:00-6:00 PM, 9:00 - 10:00 PM\n\nSunday: 8:00 - 9:00 AM, 5:00-6:00 PM, 9:00 - 10:30 PM\n\nContinuously plays the last broadcasted news at all other times."

###################################################################################################
def Start():

    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = TITLE

    DirectoryObject.thumb = R(ICON)
    VideoClipObject.thumb = R(ICON)
    InputDirectoryObject.thumb = R(ICON)
    PrefsObject.thumb = R(ICON)
    NextPageObject.thumb = R(ICON)

    HTTP.CacheTime = 1
    HTTP.Headers['User-Agent'] = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"

###################################################################################################
@handler(PREFIX, TITLE, thumb=ICON, art=ART)
def MainMenu():

    oc = ObjectContainer()

    oc.add(StreamfromLiveStreamAPI(CH2NEWS_LIVESTREAM_SUB, "2 News Live - KWGN", CH2NEWS_ICON, CH2NEWS_ART, CH2NEWS_SUMMARY))
    oc.add(StreamM3U8("7 News Live - KMGH", CH7NEWS_ICON, CH7NEWS_ART, CH7NEWS_URL, CH7NEWS_SUMMARY))
    oc.add(StreamM3U8("9 News Live - KUSA", CH9NEWS_ICON, CH9NEWS_ART, CH9NEWS_URL, CH9NEWS_SUMMARY))
    oc.add(StreamfromLiveStreamAPI(CH31NEWS_LIVESTREAM_SUB, "Fox 31 News Live - KDVR", CH31NEWS_ICON, CH31NEWS_ART, CH31NEWS_SUMMARY))

    return oc
###################################################################################################
def StreamfromLiveStreamAPI(subId, title1, icon, art, summary, include_container=False):
    url = getLiveStreamAPIURL(subId)
    Log.Debug("****** FOUND livestream.com URL for %s at %s", subId, url)
    return StreamM3U8(title1, icon, art, url, summary)
###################################################################################################
def StreamM3U8(title1, icon, art, url, summary, include_container=False):
    stream = GetStreamURL(url)
    vco = VideoClipObject(
        key = Callback(StreamM3U8, title1=title1, icon=icon, art=art, url=url, summary=summary, include_container=True),
        rating_key = url,
        title = title1,
        art = R(art),
        thumb = R(icon),
        summary = summary,
        items = [
            MediaObject(
                optimized_for_streaming = True,                   
                parts = [
                    PartObject(key=HTTPLiveStreamURL(url = stream))
                ]
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects=[vco])
    else:
        return vco
###################################################################################################
def GetStreamURL(url):
    content = HTTP.Request(url, cacheTime=1).content
    buf = StringIO(content)
    lines = buf.readlines()
    best_bandwidth = 0L
    best_url = '' 
    for index, line in enumerate(lines):
        bandwidth = getBandwidth(line)
        if bandwidth > best_bandwidth:
            best_bandwidth = bandwidth
            best_url = lines[index + 1]

    if best_url != '':
            Log.Debug("Streaming URL found = %s", best_url)
            return best_url.rstrip()
    Log.Error("Could not determine the stream from %s", url)
    Log.Error("Content = %s", url)
    return ""
###################################################################################################
def getBandwidth(line):
    params = ATTRIBUTELISTPATTERN.split(line.replace(ext_x_stream_inf + ':', ''))[1::2]
    if len(params) <= 1:
        return 0

    for param in params:
        if param.startswith('BANDWIDTH'):
            name, value = param.split('=', 1)
            return long(value)

    return 0 
###################################################################################################
def normalize_attribute(attribute):
    return attribute.replace('-', '_').lower().strip()
###################################################################################################
def getLiveStreamAPIURL(id):
    idObj = JSON.ObjectFromURL("http://api.new.livestream.com/accounts/" + id)
    events = idObj["upcoming_events"]["data"]
    eventId = getLiveStreamEventId(events)
    Log.Info("******* ID = %s and EventID = %s",id,eventId)
    eventObj = JSON.ObjectFromURL("http://api.new.livestream.com/accounts/" + id + "/events/" + str(eventId))
    return eventObj["stream_info"]["m3u8_url"]
###################################################################################################
def getLiveStreamEventId(events):
    for event in events:
        if event["short_name"] == "live":
            return event["id"]
    Log.Error("Cannot find a live event from the livestream JSON")
    return ''
###################################################################################################
