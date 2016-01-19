# Best of NHK - by misty 2013-2015.
# import python libraries
import urllib
import urllib2
import re
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
#import random
#import string
import sys
import os
import datetime
import time
import calendar
import json
import plugintools

#import SimpleDownloader as downloader
#downloader = downloader.SimpleDownloader()
addon01 = xbmcaddon.Addon('plugin.video.bestofnhk')
addonname = addon01.getAddonInfo('name')
addon_id = 'plugin.video.bestofnhk'
from t0mm0.common.addon import Addon
addon = Addon(addon_id, sys.argv)
from t0mm0.common.net import Net
net = Net()
settings = xbmcaddon.Addon(id='plugin.video.bestofnhk')
from F4mProxy import f4mProxyHelper
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET

# globals
#host1 = 'http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/'
host2 = 'http://www3.nhk.or.jp/'
host3 = 'http://ak.c.ooyala.com/'
host4 = 'http://player.ooyala.com/player/all/'
radio = 'nhkworld/app/radio/clip/'
icon = addon01.getAddonInfo('icon') # icon.png in addon directory
download_path = settings.getSetting('download_folder')
Time = str(time.strftime ('%H:%M:%S%p/%Z/%c'))
Yr = int(time.strftime ('%Y'))
Mth = int(time.strftime ('%m'))
Dy = int(time.strftime ('%d'))
Hr = str(time.strftime ('%H'))
Min = str(time.strftime ('%M'))
Date = str(time.strftime ('%m/%d/%Y'))
TimeZone = settings.getSetting('tz')
day = ''
tz_C = ''
#print "tz_C is:" + tz_C
#print "Time zone is: " + TimeZone
print "Date and time is: " + Date + " " + Time

# NHK World Schedule Time Zone and DST correction
print "Time zone is: " + TimeZone
if TimeZone == " ":
    print "TimeZone is not selected."
    line1 = "The schedule will not be correct for your time zone."
    line2 = "Please set your time zone in the Best of NHK addon settings."
    line3 = "Changes take effect after close and re-open of Best of NHK."
    xbmcgui.Dialog().ok(addonname, line1, line2, line3)
    #xbmc.executebuiltin('ActivateWindow(10140)')
else:
    pass
isdst = time.localtime().tm_isdst
print "isdst is: " + str(isdst)
tz_link = TimeZone
match=re.compile('\((.+?)\) .+?').findall(tz_link)
for tz_gmt in match:
    try:
        if isdst == int(1) and tz_gmt == 'GMT':
            tz_corrected = -60
        elif isdst == int(0) and tz_gmt == 'GMT':
            tz_corrected = 0
        print int(tz_corrected)
        tz_C = tz_corrected
    except:
        t = tz_gmt[4:]
        (H,M) = t.split(':')
        result = int(H) + int(M)/60.0
        print "result = "+str(result)
        if isdst == int(1) and tz_gmt[3:4] == '-':
            tz_corrected = (result - 1) * 60
        elif isdst == int(0) and tz_gmt[3:4] == '-':
            tz_corrected = result * 60
        elif isdst == int(1) and tz_gmt[3:4] == '+':
            tz_corrected = (result + 1) * -60
        elif isdst == int(0) and tz_gmt[3:4] == '+':
            tz_corrected = result * -60
        print int(tz_corrected)
        tz_C = tz_corrected
d_atetime = datetime.datetime(Yr,Mth,Dy,00,00,00)
e_poch_midnt = calendar.timegm(d_atetime.timetuple())
start_time = e_poch_midnt + (60*tz_C) # e_poch_midnt = GMT midnight
end_time = start_time + ((60*60*24)-60) # date+23:59:00

sch = 'http://api.nhk.or.jp/nhkworld/epg/v4/world/s'+str(int(start_time))+'-e'+str(int(end_time))+'.json?apikey=EJfK8jdS57GqlupFgAfAAwr573q01y6k'


# Main Menu
def CATEGORIES():
    addDir('NHK World Live Schedule', sch, 'schedule', icon)
    media_item_list('NHK World Live Stream', 'http://nhkwglobal-i.akamaihd.net/hls/live/222714/nhkwglobal/index_1180.m3u8', icon)
    addDir('NHK World On Demand', host2+'nhkworld/en/vod/vod_episodes.xml', 'vod', icon)
    addDir('NHK Newsroom Tokyo - Updated daily M-F', host2+'nhkworld/newsroomtokyo/', 'newsroom', icon)
    addDir('NHK News Top Stories', host2+'nhkworld/english/news/', 'topnews', icon)
    addDir('NHK Radio News', '', 'audio', icon)
    addDir('NHK Videos on Youtube', '', 'youtube1', icon)

# Create content list
def addDir(name,url,mode,iconimage):
     params = {'url':url, 'mode':mode, 'name':name}
     addon.add_directory(params, {'title': str(name)}, img = icon)


# NHK World Live Schedule
def IDX_SCHED(url):
    root = addon.get_path()
    sch_path = os.path.join(root, 'nhk_schedule.txt')
    try:
        with open (sch_path) as f: pass
        print 'File "nhk_schedule.txt" already exists.'
    except IOError as e:
        print 'Creating new file "nhk_schedule.txt".'
    req = urllib2.urlopen(url)
    sch_json = json.load(req)
    f = open(sch_path, 'w')
    try:
        for i in range(200):
            pubDate = int(sch_json['channel']['item'][i]['pubDate'])
            name = str(sch_json['channel']['item'][i]['title'])
            desc = str(sch_json['channel']['item'][i]['description'])
            sub_name = str(sch_json['channel']['item'][i]['subtitle'])
            show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
            if sub_name == "":
                f.write('[COLOR blue][B]' + show_time + ' - ' + name + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc + '[/COLOR]' + '\n' + '\n')
            else:
                f.write('[COLOR blue][B]' + show_time + ' - ' + name + ' - ' + sub_name + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc + '[/COLOR]' + '\n' + '\n')
    except:
        pass
    f.close()
    TextBox()        
        

class TextBox:
    # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        # activate the text viewer window
        xbmc.executebuiltin('ActivateWindow(%d)' % ( self.WINDOW, ))
        # get window
        self.win = xbmcgui.Window(self.WINDOW)
        # give window time to initialize
        xbmc.sleep(1000)
        self.setControls()

    def setControls(self):
        # set heading
        heading = 'NHK World Schedule for ' + Date
        self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
        # read & set text
        root = addon.get_path()
        sch_path = os.path.join(root, 'nhk_schedule.txt')
        f = open(sch_path)
        text = f.read()
        self.win.getControl(self.CONTROL_TEXTBOX).setText(text)

# video on demand
def IDX_VOD(url):
    vod_xml = urllib2.urlopen(url)
    tree = ET.parse(vod_xml)
    root = tree.getroot()
    for item in root.findall('item'):
        vod_img = item.find('main_img').text
        vod_url = item.find('epi_url').text
        od_img = ''.join(vod_img)
        od_url = ''.join(vod_url)
        thumbnl = host2[:-1]+od_img
        link = net.http_GET(host2[:-1]+od_url).content
        match1 = re.compile('<h2 class="detail-top-player-title__h"><a href="/nhkworld/en/vod/.+?/">(.+?)</a></h2>').findall(link)
        match2 = re.compile("<script>nw_vod_ooplayer\('movie-area', '(.+?)'\)").findall(link)
        match3 = re.compile('<div class="episode-detail">\n.+?<h3>(.+?)</h3>').findall(link)
        series = str(match1).replace('[\'','').replace('\']','')
        ep_name = str(match3).replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ')
        vid_id = str(match2).replace('[\'','').replace('\']','')
        media_item_list(series + ' - ' + ep_name, host4 + vid_id + '.m3u8', thumbnl)
    
# Newsroom Tokyo news broadcast updated daily M-F
def IDX_NEWS(url):
    link = net.http_GET(url).content
    match=re.compile('nw_vod_ooplayer\(\'movie-area\', \'(.+?)\', playerCallback\);</script>\n</div>\n<h2>Latest edition</h2>\n<h3></h3>\n<p class="date">(.+?)</p>\n<!--latest_end-->').findall(link)
    for vid_id, d_ate in match:
        media_item_list('Newsroom Tokyo for '+ d_ate, host4 + vid_id + '.m3u8','')

# Top news stories
def IDX_TOPNEWS(url):
    link = net.http_GET(url).content
    match1=re.compile('<h1 class="top-title"><a href="/(.+?)">(.+?)</a></h1>\n.+?<div class="cat-info">\n.+?<a href="/nhkworld/english/news/.+?.html" class="linkBtn">.+?</a><a href').findall(link)
    match2=re.compile('<h3 class="sub-title"><a href="/(.+?)">(.+?)</a></h3>\n.+?<div class="cat-info">\n.+?<div class="fll"><a href="/nhkworld/english/news/.+?.html" class="linkBtn">.+?</a><a href').findall(link)
    for pg_link,name in match1+match2:
        link2 = net.http_GET(host2+pg_link).content
        match3=re.compile("movie_play\('(.+?)'").findall(link2)
        for xml_link in match3:
            file = urllib2.urlopen(host2+xml_link)
            data = file.read()
            file.close()
            dom = parseString(data)
            xmlTag = dom.getElementsByTagName('file.high')[0].toxml()
            xmlData=xmlTag.replace('<file.high><![CDATA[','').replace(']]></file.high>','')
            media_item_list(name,xmlData,'')

# Pre-recorded NHK World Radio in 18 languages
def IDX_RADIO(url):
    media_item_list('NHK Radio News in Arabic', host2+radio+'arabic_news.xml','')
    media_item_list('NHK Radio News in Bengali', host2+radio+'bengali_news.xml','')
    media_item_list('NHK Radio News in Burmese', host2+radio+'burmese_news.xml','')
    media_item_list('NHK Radio News in Chinese', host2+radio+'chinese_news.xml','')
    media_item_list('NHK Radio News in English', host2+radio+'english_news.xml','')
    media_item_list('NHK Radio News in French', host2+radio+'french_news.xml','')
    media_item_list('NHK Radio News in Hindi', host2+radio+'hindi_news.xml','')
    media_item_list('NHK Radio News in Indonesian', host2+radio+'indonesian_news.xml','')
    media_item_list('NHK Radio News in Japanese', host2+radio+'japanese_news.xml','')
    media_item_list('NHK Radio News in Korean', host2+radio+'korean_news.xml','')
    media_item_list('NHK Radio News in Persian', host2+radio+'persian_news.xml','')
    media_item_list('NHK Radio News in Portuguese', host2+radio+'portuguese_news.xml','')
    media_item_list('NHK Radio News in Russian', host2+radio+'russian_news.xml','')
    media_item_list('NHK Radio News in Spanish', host2+radio+'spanish_news.xml','')
    media_item_list('NHK Radio News in Swahili', host2+radio+'swahili_news.xml','')
    media_item_list('NHK Radio News in Thai', host2+radio+'thai_news.xml','')
    media_item_list('NHK Radio News in Urdu', host2+radio+'urdu_news.xml','')
    media_item_list('NHK Radio News in Vietnamese', host2+radio+'vietnamese_news.xml','')

def IDX_YOUTUBE1():
    plugintools.log("nhkworld1.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list1(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Youtube menu
def main_list1(params):
    plugintools.log("nhkworld1.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="NHK World Channel",
        url="plugin://plugin.video.youtube/user/NHKWorld/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Youtube Search for 'NHK World'",
        url='plugin://plugin.video.youtube/search/?q=NHK World',
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 01",
        url="plugin://plugin.video.youtube/channel/UCySEkVg1Q3QXjDvRFB0H41Q/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 02",
        url="plugin://plugin.video.youtube/channel/UCcajZR_EkvQro0ZgFX6lgtQ/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 03",
        url="plugin://plugin.video.youtube/channel/UCs8DHpkt9f61vUOZO_qwiSQ/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 04",
        url="plugin://plugin.video.youtube/channel/UC4w_dcTPt8iaLE18TB7RLtQ/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 05",
        url="plugin://plugin.video.youtube/channel/UCgP5mLnSCcP8tj1jWIWYP5Q/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 06",
        url="plugin://plugin.video.youtube/channel/UCgP5mLnSCcP8tj1jWIWYP5Q/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 07",
        url="plugin://plugin.video.youtube/playlist/PLKQaIKexM4LJL4GL-lfgvDdlLElTjJIUW/",
        thumbnail=icon,
        folder=True )
     
    plugintools.add_item( 
        #action="", 
        title="UNESCO/NHK",
        url="plugin://plugin.video.youtube/playlist/PLWuYED1WVJIPKU_tUlzLTfkbNnAtkDOhS/",
        thumbnail=icon,
        folder=True )
        
    addDir('More Shows', '', 'youtube2', icon)
    
def IDX_YOUTUBE2():
    plugintools.log("nhkworld2.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list2(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Youtube menu
def main_list2(params):
    plugintools.log("nhkworld2.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="NHK Documentary - Silk Road",
        url="plugin://plugin.video.youtube/playlist/PLB8KCZnnrFKmP6CPynDrFVheEt9VOBPk4/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="NHK Documentary - Silk Road II",
        url="plugin://plugin.video.youtube/playlist/PLdwCuEoZ_6l7FvbsfjidxMIybBrF5jnb5/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Begin Japanology 01",
        url="plugin://plugin.video.youtube/channel/UCPMSNvTv2rgODVy0GvsMxZg/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Begin Japanology 02",
        url="plugin://plugin.video.youtube/playlist/PL8IcLS3A4sWKqf47xzXl_NIwlj_Hae5fM/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Begin Japanology 03",
        url="plugin://plugin.video.youtube/playlist/PLJ4SclxaotEijsfzIFlUcHG6huoiovh9s/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tokyo Eye",
        url="plugin://plugin.video.youtube/channel/UC5ehEXRuBeVo1gkulk5I4BQ/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="cool japan",
        url="plugin://plugin.video.youtube/playlist/PL54G12jDE7cPq7xbyEyaIf7jRvUC04TJg/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Dining with the Chef",
        url="plugin://plugin.video.youtube/playlist/PLIz8fpF_mbPSpMiJ9OHXo5Ai7dYDLXhYM/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Sports Japan",
        url="plugin://plugin.video.youtube/playlist/PLIz8fpF_mbPSjA3l8bPyYF2vYZioFl2S1/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Meet and Speak",
        url="plugin://plugin.video.youtube/playlist/PLdRCqO13zyDfQuDoZG6pHQuSJ2dbwVWQu/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="MoshiMoshi Nippon",
        url="plugin://plugin.video.youtube/playlist/PLpHD2EwLFcoQkHEP7w458jR-kSY_W4mo2/",
        thumbnail=icon,
        folder=True )

# Create media items list
def media_item_list(name,url,img):
    if mode=='f4m':
        player=f4mProxyHelper()
        player.playF4mLink(url, name)
        if not play:
            pass

    elif mode=='audio':
        file = urllib2.urlopen(url)
        data = file.read()
        file.close()
        dom = parseString(data)
        xmlTag = dom.getElementsByTagName('url')[0].toxml()
        radionews_url=xmlTag.replace('<url>','').replace('</url>','')
        addon.add_music_item({'url': radionews_url}, {'title': name}, context_replace = icon, playlist=False)

    elif mode=='vod':
        addon.add_video_item({'url': url}, {'title': name}, img = img, playlist=False)

    else:
        addon.add_video_item({'url': url}, {'title': name}, img = icon, playlist=False)
            


# Downloader
#def download_media():
#    print df

# Query play, mode, url and name
play = addon.queries.get('play', None)
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')

print "Play: " +str(play)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


# Program flow control
if play:
    addon.resolve_url(url.encode('UTF-8')) # <<< Play resolved media url

if mode=='main':
    print ""
    CATEGORIES()

elif mode=='schedule':
    print ""+url
    IDX_SCHED(url)

elif mode=='vod':
    print ""+url
    IDX_VOD(url)
    
elif mode=='f4m':
    print ""+url
    media_item_list(name,url,img)

elif mode=='youtube1':
    print ""+url
    IDX_YOUTUBE1()
    
elif mode=='youtube2':
    print ""+url
    IDX_YOUTUBE2()

elif mode=='newsroom':
    print ""+url
    IDX_NEWS(url)
    
elif mode=='topnews':
    print ""+url
    IDX_TOPNEWS(url)

elif mode=='audio':
    print ""+url
    IDX_RADIO(url)

if not play:
    addon.end_of_directory()
