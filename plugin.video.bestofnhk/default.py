# Best of NHK - by misty 2013-2016.
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
host5 = 'http://api.nhk.or.jp/nhkworld/base/x2j/v1/'
apikey = 'apikey=EJfK8jdS57GqlupFgAfAAwr573q01y6k'
feat = 'nhkworld/rss/news/english/features_'
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
tz_C = 0
print "Date and time is: " + Date + " " + Time

# NHK World Schedule Time Zone and DST correction
print "Time zone is: " + TimeZone
# TZ message box
if TimeZone == " ":
    print "TimeZone is not selected."
    line1 = "The schedule will not be correct for your time zone."
    line2 = "Please set your time zone in the Best of NHK addon settings."
    line3 = "Changes take effect after close and re-open of Best of NHK."
    xbmcgui.Dialog().ok(addonname, line1, line2, line3)
else:
    pass

# TZ and DST calc
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
start_time = int(e_poch_midnt) + int(60*tz_C) # e_poch_midnt = GMT midnight
end_time = int(start_time) + ((60*60*24)-60) # date+23:59:00

sch = 'http://api.nhk.or.jp/nhkworld/epg/v4/world/s'+str(int(start_time))+'-e'+str(int(end_time))+'.json?%s' % apikey
now = 'http://api.nhk.or.jp/nhkworld/epg/v4/world/now.json?%s' % apikey


# Main Menu
def CATEGORIES():
    addDir('NHK World Live Schedule', '', 'schedule', icon)
    addDir('NHK World Live Stream', '', 'live_strm', icon)
    addDir('NHK World On Demand', host2+'nhkworld/en/vod/vod_episodes.xml', 'vod', icon)
    addDir('NHK Newsroom Tokyo - Updated daily M-F', host2+'nhkworld/newsroomtokyo/', 'newsroom', icon)
    addDir('NHK News Top Stories', host2+'nhkworld/english/news/', 'topnews', icon)
    addDir('NHK News Feature Stories', '', 'feature', icon)
    addDir('NHK Radio News', '', 'audio', icon)
    addDir('NHK Videos on Youtube', '', 'youtube1', icon)

# Create content list
def addDir(name,url,mode,iconimage):
     params = {'url':url, 'mode':mode, 'name':name}
     addon.add_directory(params, {'title': str(name)}, img = icon)

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

# NHK World Live Schedule
def IDX_SCHED(url):
    # File write for textbox
    root = addon.get_path()
    sch_path = os.path.join(root, 'nhk_schedule.txt')
    try:
        with open (sch_path) as f: pass
        print 'File "nhk_schedule.txt" already exists.'
    except IOError as e:
        print 'Creating new file "nhk_schedule.txt".'
    req_now = urllib2.urlopen(now)
    pl_now = json.load(req_now)
    req = urllib2.urlopen(sch)
    sch_json = json.load(req)
    f = open(sch_path, 'w')
    f.write('[B]Currently streaming:[/B]' + '\n' + '\n')
    pubDate = int(pl_now['channel']['item'][0]['pubDate'])
    name = pl_now['channel']['item'][0]['title']
    desc = pl_now['channel']['item'][0]['description']
    sub_name = pl_now['channel']['item'][0]['subtitle']
    show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
    if sub_name == "":
        f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
    else:
        f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
    f.write('[B]Next:[/B]' + '\n' + '\n')
    
    try:
        for i in range(1,3):
            pubDate = int(pl_now['channel']['item'][i]['pubDate'])
            name = pl_now['channel']['item'][i]['title']
            desc = pl_now['channel']['item'][i]['description']
            sub_name = pl_now['channel']['item'][i]['subtitle']
            show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
            if sub_name == "":
                f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
            else:
                f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
    except:
        pass

    f.write('[B]Today\'s schedule:[/B]' + '\n' + '\n')

    try:
        for i in range(200):
            pubDate = int(sch_json['channel']['item'][i]['pubDate'])
            name = sch_json['channel']['item'][i]['title']
            desc = sch_json['channel']['item'][i]['description']
            sub_name = sch_json['channel']['item'][i]['subtitle']
            show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
            if sub_name == "":
                f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
            else:
                f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
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

# live streams
def IDX_LIVE_STRM():
    req_now = urllib2.urlopen(now)
    pl_now = json.load(req_now)
    pubDate = int(pl_now['channel']['item'][0]['pubDate'])
    name = pl_now['channel']['item'][0]['title']
    desc = pl_now['channel']['item'][0]['description']
    sub_name = pl_now['channel']['item'][0]['subtitle']
    show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
    # menu
    media_item_list('NHK World Live Stream SD', 'http://nhkwglobal-i.akamaihd.net/hls/live/222714/nhkwglobal/index_1180.m3u8', icon)
    media_item_list('NHK World Live Stream HD', 'http://nhkwglobal-i.akamaihd.net/hls/live/225446/nhkwstv/index_2100.m3u8', icon)
    try:
        addLink('', '', '', icon, '')
        addLink('[B]Currently streaming:[/B]', '', '', icon, '')
        if sub_name == "":
            addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]', '', '', icon, '')
        else:
            addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]', '', '', icon, '')
        addLink('[B]Next:[/B]', '', '', icon, '')
        for i in range(1,3):
            pubDate = int(pl_now['channel']['item'][i]['pubDate'])
            name = pl_now['channel']['item'][i]['title']
            desc = pl_now['channel']['item'][i]['description']
            sub_name = pl_now['channel']['item'][i]['subtitle']
            show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
            if sub_name == "":
                addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]', '', '', icon, '')
            else:
                addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]', '', '', icon, '')
    except:
        pass

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
        ep_name = str(match3).replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xc3','e').replace('\\xef\\xbd\\x9e',' ~ ')
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
            media_item_list(name,xmlData,icon)
            
# Feature news stories
def IDX_FEATURE(url):
    addDir('NHK News Feature Stories - Japan', host2+feat+'japan.xml', 'feat_news', icon)
    addDir('NHK News Feature Stories - Asia', host2+feat+'asia.xml', 'feat_news', icon)
    addDir('NHK News Feature Stories - World', host2+feat+'world.xml', 'feat_news', icon)
    addDir('NHK News Feature Stories - BizTec', host2+feat+'biztec.xml', 'feat_news', icon)
    addDir('NHK News Feature Stories - Nuclear & Energy', host2+feat+'post311.xml', 'feat_news', icon)
    
def IDX_FEAT_NEWS(url):
    feat_xml = urllib2.urlopen(url)
    data = feat_xml.read()
    feat_xml.close()
    dom = parseString(data)

    try:
        for i in range(1,200):
            title = dom.getElementsByTagName('title')[i].toxml()
            html = dom.getElementsByTagName('link')[i].toxml()
            title_ = title.replace('<title><![CDATA[','').replace(']]></title>','').replace('&quot;','"').replace('&amp;','&').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xc3','e').replace('\\xef\\xbd\\x9e',' ~ ')
            html_ = html.replace('<link>','').replace('</link>','')
            IDX_FEAT_NEWS_1(html_, title_)
    except:
        pass

def IDX_FEAT_NEWS_1(url, name):
    link = net.http_GET(url).content
    match = re.compile("movie_play\('(.+?)',").findall(link)
    for xml_link in match:
        file = urllib2.urlopen(host2[:-1]+xml_link)
        data = file.read()
        file.close()
        dom = parseString(data)
        v_url = dom.getElementsByTagName('file.high')[0].toxml()
        image = dom.getElementsByTagName('image')[0].toxml()
        vid_url = v_url.replace('<file.high><![CDATA[','').replace(']]></file.high>','')
        thumbnl = host2 + image.replace('<image><![CDATA[/','').replace(']]></image>','')
        media_item_list(name,vid_url,thumbnl)

# Pre-recorded NHK World Radio in 18 languages
def IDX_RADIO(url):
    media_item_list('NHK Radio News in Arabic', host5+'arabic_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Bengali', host5+'bengali_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Burmese', host5+'burmese_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Chinese', host5+'chinese_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in English', host5+'english_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in French', host5+'french_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Hindi', host5+'hindi_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Indonesian', host5+'indonesian_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Japanese', host5+'japanese_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Korean', host5+'korean_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Persian', host5+'persian_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Portuguese', host5+'portuguese_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Russian', host5+'russian_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Spanish', host5+'spanish_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Swahili', host5+'swahili_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Thai', host5+'thai_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Urdu', host5+'urdu_news.xml?'+apikey,'')
    media_item_list('NHK Radio News in Vietnamese', host5+'vietnamese_news.xml?'+apikey,'')

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

    elif mode=='vod' or 'feat_news':
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

elif mode=='live_strm':
    print ""+url
    IDX_LIVE_STRM()

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
    
elif mode=='feature':
    print ""+url
    IDX_FEATURE(url)
    
elif mode=='feat_news':
    print ""+url
    IDX_FEAT_NEWS(url)

elif mode=='audio':
    print ""+url
    IDX_RADIO(url)

if not play:
    addon.end_of_directory()
