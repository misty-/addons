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
import string
import sys
import os
import time
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
radio = 'rj/podcast/mp3/'
icon = addon01.getAddonInfo('icon') # icon.png in addon directory
download_path = settings.getSetting('download_folder')
Time = str(time.strftime ('%H:%M:%S%p/%Z/%c'))
Yr = str(time.strftime ('%Y'))
Mth = str(time.strftime ('%m'))
Dy = str(time.strftime ('%d'))
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
        tz_C = str(int(tz_corrected))
    except:
        t = tz_gmt[4:]
        (H,M) = t.split(':')
        result = int(H) + int(M)/60.0
        if isdst == int(1) and tz_gmt[3:4] == '-':
            tz_corrected = (result - 1) * 60
        elif isdst == int(0) and tz_gmt[3:4] == '-':
            tz_corrected = result * 60
        elif isdst == int(1) and tz_gmt[3:4] == '+':
            tz_corrected = (result + 1) * -60
        elif isdst == int(0) and tz_gmt[3:4] == '+':
            tz_corrected = result * -60
        print int(tz_corrected)
        tz_C = str(int(tz_corrected))


sch = 'http://www.jibtv.com/schedule/getjson.php?mode=schedule&y='+Yr+'&a='+Mth+'&d='+Dy+'&h='+Hr+'&m='+Min+'&jisa='+tz_C+'&innd=0&print=false'


# Main Menu
def CATEGORIES():
    addDir('NHK World Live Schedule', sch, 'schedule', icon)
    media_item_list('NHK World Live Stream', 'http://nhkwglobal-i.akamaihd.net/hls/live/222714/nhkwglobal/index_1180.m3u8')
    addDir('NHK World On Demand', host2+'nhkworld/en/vod/vod_episodes.xml', 'vod', icon)
    addDir('NHK Newsroom Tokyo - Updated daily M-F', host2+'nhkworld/newsroomtokyo/', 'newsroom', icon)
    addDir('NHK News Top Stories', host2+'nhkworld/english/news/', 'topnews', icon)
    addDir('NHK Radio News', host2, 'audio', icon)
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
    try:
        link = net.http_GET(url).content
        f = open(sch_path, 'w')
        match1 = re.compile('<div class="sche_now_on_air">(.+?)\n<span class="sche_now_on_air_mark"><img src="img/sche_oa.png" width="70" height="20" alt="now on air" /></span>\n</div>\n<div class="sche_program_ad">\n<p class="sche_program_title" span style="">(.+?)</p>\n<p class="sche_program_txt">(.+?)<!--').findall(link)
        match2 = re.compile('<div class="sche_now_on_air">(.+?)\n</div>\n<div class="sche_program_ad">\n<p class="sche_program_title" span style="">(.+?)</p>\n<p class="sche_program_txt">(.+?)<!--').findall(link)
        for time,name,desc in match1 + match2:
            f.write('[COLOR blue][B]' + time + ' - ' + name + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc + '[/COLOR]' + '\n' + '\n')
        f.close()
    except:
        pass
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
    #media_item_list('NHK World Live 512',host1+'nhkworld-live-512.f4m')
    vod_xml = urllib2.urlopen(url)
    tree = ET.parse(vod_xml)
    #print tree
    root = tree.getroot()
    for item in root.findall('item'):
        vod_url = item.find('epi_url').text
        #print vod_url
        od_url = ''.join(vod_url)
        link = net.http_GET(host2[:-1]+od_url).content
        match1 = re.compile('<h2 class="detail-top-player-title__h"><a href="/nhkworld/en/vod/.+?/">(.+?)</a></h2>').findall(link)
        match2 = re.compile("<script>nw_vod_ooplayer\('movie-area', '(.+?)'\)").findall(link)
        match3 = re.compile('<div class="episode-detail">\n.+?<h3>(.+?)</h3>').findall(link)
        series = str(match1).replace('[\'','').replace('\']','')
        ep_name = str(match3).replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e')
        vid_id = str(match2).replace('[\'','').replace('\']','')
        media_item_list(series + ' - ' + ep_name, host4 + vid_id + '.m3u8')
    
# Newsroom Tokyo news broadcast updated daily M-F
def IDX_NEWS(url):
    link = net.http_GET(url).content
    #print link
    match=re.compile('<!--latest_start-->\n<script>nw_vod_ooplayer\(\'movie-area\', \'(.+?)\'\);</script>\n</div>\n<h2>Latest edition</h2>\n<h3></h3>\n<p class="date">(.+?)</p>\n<!--latest_end-->').findall(link)
    for vid_id, d_ate in match:
        media_item_list('Newsroom Tokyo for '+ d_ate, host4 + vid_id + '.m3u8')

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
            #print xmlTag
            #print xmlData
            media_item_list(name,xmlData)

# Pre-recorded NHK World Radio in 17 languages
def IDX_RADIO(url):
    media_item_list('NHK Radio News in Arabic',host2+radio+'arabic.mp3')
    media_item_list('NHK Radio News in Bengali',host2+radio+'bengali.mp3')
    media_item_list('NHK Radio News in Burmese',host2+radio+'burmese.mp3')
    media_item_list('NHK Radio News in Chinese',host2+radio+'chinese.mp3')
    media_item_list('NHK Radio News in English',host2+radio+'english.mp3')
    media_item_list('NHK Radio News in French',host2+radio+'french.mp3')
    media_item_list('NHK Radio News in Hindi',host2+radio+'hindi.mp3')
    media_item_list('NHK Radio News in Indonesian',host2+radio+'indonesian.mp3')
    media_item_list('NHK Radio News in Japanese','mms://wm.nhk.or.jp/rj/on_demand/wma/japanese.wma')
    media_item_list('NHK Radio News in Korean',host2+radio+'korean.mp3')
    media_item_list('NHK Radio News in Persian',host2+radio+'persian.mp3')
    media_item_list('NHK Radio News in Portugese',host2+radio+'portugese.mp3')
    media_item_list('NHK Radio News in Russian',host2+radio+'russian.mp3')
    media_item_list('NHK Radio News in Spanish',host2+radio+'spanish.mp3')
    media_item_list('NHK Radio News in Swahili',host2+radio+'swahili.mp3')
    media_item_list('NHK Radio News in Thai',host2+radio+'thai.mp3')
    media_item_list('NHK Radio News in Urdu',host2+radio+'urdu.mp3')
    media_item_list('NHK Radio News in Vietnamese',host2+radio+'vietnamese.mp3')

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
        url="plugin://plugin.video.youtube/channel/UCqKxEjL3beC6urT_B41Iq1g/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 04",
        url="plugin://plugin.video.youtube/channel/UCs8DHpkt9f61vUOZO_qwiSQ/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 05",
        url="plugin://plugin.video.youtube/channel/UC4w_dcTPt8iaLE18TB7RLtQ/",
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
        url="plugin://plugin.video.youtube.plus/channel/UCnx4tq4meIIDdszdtl8gu5A/",
        thumbnail=icon,
        folder=True )
     
    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 08",
        url="plugin://plugin.video.youtube/playlist/PLKQaIKexM4LJL4GL-lfgvDdlLElTjJIUW/",
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
def media_item_list(name,url):
    if mode=='f4m':
        player=f4mProxyHelper()
        player.playF4mLink(url, name)
        if not play:
            pass

    elif mode=='audio':
        addon.add_music_item({'url': url}, {'title': name}, context_replace = icon, playlist=False)

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
    media_item_list(name,url)

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
