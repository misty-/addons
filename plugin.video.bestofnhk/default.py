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
pluginhandle = int(sys.argv[1])

# globals
#host1 = 'http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/'
host2 = 'http://www3.nhk.or.jp/'
host3 = 'http://ak.c.ooyala.com/'
host4 = 'http://player.ooyala.com/player/all/'
host5 = 'http://www.nhk.or.jp/rj/podcast/rss/'
apikey = 'apikey=EJfK8jdS57GqlupFgAfAAwr573q01y6k'
feat = 'nhkworld/rss/news/english/features_'
nhk_icon = addon01.getAddonInfo('icon') # icon.png in addon directory
jib_icon = 'http://www.jamaipanese.com/wp-content/uploads/2009/05/jibbywithfreesby.jpg'
download_path = settings.getSetting('download_folder')
Time = str(time.strftime ('%H:%M:%S%p/%Z/%c'))
str_Yr = str(time.strftime ('%Y'))
str_Mth = str(time.strftime ('%m'))
Yr = int(time.strftime ('%Y'))
Mth = int(time.strftime ('%m'))
Dy = int(time.strftime ('%d'))
Hr = str(time.strftime ('%H'))
Min = str(time.strftime ('%M'))
Date = str(time.strftime ('%m/%d/%Y'))
TimeZone = settings.getSetting('tz')
day = ''
tz_C = 0
#print "Date and time is: " + Date + " " + Time

# NHK World Schedule Time Zone and DST correction
#print "Time zone is: " + TimeZone
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
#print "isdst is: " + str(isdst)
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
        #print int(tz_corrected)
        tz_C = tz_corrected
d_atetime = datetime.datetime(Yr,Mth,Dy,00,00,00)
e_poch_midnt = calendar.timegm(d_atetime.timetuple())
start_time = int(e_poch_midnt) + int(60*tz_C) # e_poch_midnt = GMT midnight
end_time = int(start_time) + ((60*60*24)-60) # date+23:59:00

sch = 'http://api.nhk.or.jp/nhkworld/epg/v4/world/s'+str(int(start_time))+'-e'+str(int(end_time))+'.json?%s' % apikey
now = 'http://api.nhk.or.jp/nhkworld/epg/v4/world/now.json?%s' % apikey


# Main Menu
def CATEGORIES():
    addDir('NHK World Live Schedule', '', 'schedule', nhk_icon)
    addDir('NHK World Live Stream', '', 'live_strm', nhk_icon)
    addDir('NHK World On Demand', 'http://api.nhk.or.jp/nhkworld/vodesdlist/v1/all/all/all.json?%s' % apikey, 'vod', icon)
    addDir('JIBTV On Demand', 'http://jibtv.com/', 'jibtv', jib_icon)
    addDir('NHK Newsroom Tokyo - Updated daily M-F', host2+'nhkworld/newsroomtokyo/', 'newsroom', nhk_icon)
    addDir('NHK News Top Stories', host2+'nhkworld/data/en/news/all.json', 'topnews', nhk_icon)
    addDir('NHK News Feature Stories', 'http://api.nhk.or.jp/nhkworld/pg/list/v1/en/newsvideos/all/all.json?%s' % apikey, 'feature', nhk_icon)
    addDir('NHK Radio News', '', 'audio', nhk_icon)
    addDir('NHK Videos on Youtube', '', 'youtube1', nhk_icon)

# Create content list
def addDir(name,url,mode,iconimage):
    params = {'url':url, 'mode':mode, 'name':name}
    addon.add_directory(params, {'title': str(name)}, img = iconimage, fanart = 'http://www3.nhk.or.jp/nhkworld/en/calendar'+str_Yr+'/images/large/'+str_Mth+'.jpg')

def addLink(name,url,plot,img,fanart):
    addon.add_item({'url': fanart}, {'title': name, 'plot': plot}, img = img, fanart = fanart, resolved=False, total_items=0, playlist=False, item_type='video', 
                 is_folder=False)

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
        for i in range(1,4):
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
    thumbnl = pl_now['channel']['item'][0]['thumbnail']
    show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
    # menu
    if TimeZone == '(GMT+09:00) Osaka, Sapporo, Tokyo':
        media_item_list(name.encode('UTF-8') + ' - SD', 'http://nhkworldtvlive-i.akamaihd.net/hls/live/222467/dw/index_900.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
        media_item_list(name.encode('UTF-8') + ' - HD', 'http://nhkworldtvlive-i.akamaihd.net/hls/live/222468/dwstv/index_2100.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
    else:
        media_item_list(name.encode('UTF-8') + ' - SD', 'http://nhkwglobal-i.akamaihd.net/hls/live/222714/nhkwglobal/index_1180.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
        media_item_list(name.encode('UTF-8') + ' - HD', 'http://nhkwglobal-i.akamaihd.net/hls/live/225446/nhkwstv/index_2100.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
    try:
        if sub_name == "":
            addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
        else:
            addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
        for i in range(1,20):
            pubDate = int(pl_now['channel']['item'][i]['pubDate'])
            name = pl_now['channel']['item'][i]['title']
            desc = pl_now['channel']['item'][i]['description']
            sub_name = pl_now['channel']['item'][i]['subtitle']
            thumbnl = pl_now['channel']['item'][i]['thumbnail']
            show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
            if sub_name == "":
                addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
            else:
                addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

# video on demand
def IDX_VOD(url):
    req = urllib2.urlopen(url)
    vod_json = json.load(req)
    try:
        for i in range(300):
            series_ = vod_json['data']['episodes'][i]['title']
            ep_name_ = vod_json['data']['episodes'][i]['sub_title']
            plot_ = vod_json['data']['episodes'][i]['description']
            thumbnl_ = vod_json['data']['episodes'][i]['image_l']
            vid_id = vod_json['data']['episodes'][i]['vod_id']
            series = (series_).replace('[\'','').replace('\']','').replace('<br />',' ')
            ep_name = (ep_name_).replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xc3','e').replace('\\xef\\xbd\\x9e',' ~ ')
            plot = (plot_).replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xc3','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('<em>','').replace('</em>','')
            thumbnl = host2[:-1]+thumbnl_
            media_item_list(series + ' - ' + ep_name, host4 + vid_id + '.m3u8', plot, thumbnl, thumbnl)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

# jibtv
def IDX_JIBTV(url):
    addDir('Recommended', 'http://jibtv.com/', 'jib_rec', jib_icon)
    addDir('Featured Programs', 'http://jibtv.com/programs/', 'jib_feat', jib_icon)

def JIB_REC(url):
    link = net.http_GET(url).content
    match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
    for vid_page, title in match:
        try:
            link1 = net.http_GET('http://jibtv.com/%s' % vid_page).content
            desc_ = re.compile('<meta property="og:description" content="(.+?)" />').findall(link1)
            plot = ''.join(desc_)
            thumb = re.compile('<meta property="og:image" content="(.+?)" />').findall(link1)
            thumbnl = ''.join(thumb).replace('showcace','showcase')
            meta_id = re.compile('player.play\(\{ meta_id: (.+?) \}\)').findall(link1)
            vid_id = ''.join(meta_id)
            link2 = net.http_GET('http://jibtv-vcms.logica.io/api/v1/metas/%s/medias' % vid_id).content
            vid_src_ = re.compile('\[\{"format":"hls","url":"(.+?)"\}\]').findall(link2)
            vid_src = ''.join(vid_src_)
            if thumbnl == "":
                media_item_list(title, vid_src, plot, jib_icon , 'http://www3.nhk.or.jp/nhkworld/en/calendar'+str_Yr+'/images/large/'+str_Mth+'.jpg')
            else:
                media_item_list(title, vid_src, plot, thumbnl, thumbnl)
        except:
            pass
        xbmcplugin.setContent(pluginhandle, 'episodes')

def JIB_FEAT(url):
    link = net.http_GET(url).content
    match=re.compile('<a href="/programs/(.+?)">').findall(link)
    for vid_page in match:
        try:
            link1 = net.http_GET('http://jibtv.com/programs/%s' % vid_page).content
            title_ = re.compile('<meta property="og:title" content="(.+?)" />').findall(link1)
            title = ''.join(title_)
            desc_ = re.compile('<meta property="og:description" content="(.+?)" />').findall(link1)
            plot = ''.join(desc_)
            thumb = re.compile('<meta property="og:image" content="(.+?)" />').findall(link1)
            thumbnl = ''.join(thumb).replace('showcace','showcase')
            meta_id = re.compile('player.play\(\{ meta_id: (.+?) \}\)').findall(link1)
            vid_id = ''.join(meta_id)
            link2 = net.http_GET('http://jibtv-vcms.logica.io/api/v1/metas/%s/medias' % vid_id).content
            vid_src_ = re.compile('\[\{"format":"hls","url":"(.+?)"\}\]').findall(link2)
            vid_src = ''.join(vid_src_)
            if thumbnl == "":
                media_item_list(title, vid_src, plot, jib_icon , 'http://www3.nhk.or.jp/nhkworld/en/calendar'+str_Yr+'/images/large/'+str_Mth+'.jpg')
            else:
                media_item_list(title, vid_src, plot, thumbnl, thumbnl)
        except:
           pass
        xbmcplugin.setContent(pluginhandle, 'episodes')
    
# Newsroom Tokyo news broadcast updated daily M-F
def IDX_NEWS(url):
    link = net.http_GET(url).content
    match=re.compile('nw_vod_ooplayer\(\'movie-area\', \'(.+?)\', playerCallback\);</script>\n</div>\n<h2>Latest edition</h2>\n<h3></h3>\n<p class="date">(.+?)</p>\n<!--latest_end-->').findall(link)
    icon = "http://www3.nhk.or.jp/nhkworld/newsroomtokyo/img/common/logo.png"
    fanart_ = "https://www.kcet.org/sites/kl/files/atoms/article_atoms/www.kcet.org/shows/tvtalk/assets/images/NewsroomTokyo_630.jpg"
    for vid_id, d_ate in match:
        media_item_list('Newsroom Tokyo for '+ d_ate, host4 + vid_id + '.m3u8','', icon, fanart_)

# Latest top news stories
def IDX_TOPNEWS(url):
    req = urllib2.urlopen(url)
    top_json = json.load(req)
    try:
        for i in range(200):
            if top_json['data'][i]['videos']:
                xml_link = top_json['data'][i]['videos']['config']
                file = urllib2.urlopen(host2[:-1]+xml_link)
                data = file.read()
                file.close()
                dom = parseString(data)
                v_url = dom.getElementsByTagName('file.high')[0].toxml()
                image = dom.getElementsByTagName('image')[0].toxml()
                name = dom.getElementsByTagName('media.title')[0].toxml()
                vid_url = v_url.replace('<file.high><![CDATA[','').replace(']]></file.high>','')
                thumbnl = host2 + image.replace('<image><![CDATA[/','').replace(']]></image>','')
                name_ = name.replace('<media.title>','').replace('</media.title>','').replace("_#039_","'").replace('_quot_','"').replace('&quot;','"').replace('&amp;','&').replace('_amp_','&').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xc3','e').replace('\\xef\\xbd\\x9e',' ~ ')
                media_item_list(name_,vid_url,'',thumbnl,thumbnl)
    except:
        pass

# Feature news stories
def IDX_FEATURE(url):
    addDir('NHK News Feature Stories - Japan', url, 'feat_news_japan', nhk_icon)
    addDir('NHK News Feature Stories - Asia', url, 'feat_news_asia', nhk_icon)
    addDir('NHK News Feature Stories - World', url, 'feat_news_world', nhk_icon)
    addDir('NHK News Feature Stories - BizTec', url, 'feat_news_biztec', nhk_icon)

def IDX_FEAT_NEWS(url):
    req = urllib2.urlopen(url)
    feat_json = json.load(req)
    try:
        for i in range(300):
            #thumbnl = feat_json['data'][i]['thumbnails']['middle']
            xml_link = feat_json['data'][i]['videos']['config']
            #title = feat_json['data'][i]['title']
            cat = feat_json['data'][i]['categories']['name']
            if mode == 'feat_news_japan' and cat == 'JAPAN' or mode == 'feat_news_asia' and cat == 'ASIA' or mode == 'feat_news_world' and cat == 'WORLD' or mode == 'feat_news_biztec' and cat == 'BIZTCH':
                file = urllib2.urlopen(host2[:-1]+xml_link)
                data = file.read()
                file.close()
                dom = parseString(data)
                v_url = dom.getElementsByTagName('file.high')[0].toxml()
                image = dom.getElementsByTagName('image')[0].toxml()
                name = dom.getElementsByTagName('media.title')[0].toxml()
                vid_url = v_url.replace('<file.high><![CDATA[','').replace(']]></file.high>','')
                thumbnl = host2 + image.replace('<image><![CDATA[/','').replace(']]></image>','')
                name_ = name.replace('<media.title>','').replace('</media.title>','').replace("_#039_","'").replace('_quot_','"').replace('&quot;','"').replace('&amp;','&').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xc3','e').replace('\\xef\\xbd\\x9e',' ~ ')
                #print "name is: "+name_
                media_item_list(name_,vid_url,'',thumbnl,thumbnl)
    except:
        pass

# Pre-recorded NHK World Radio in 17 languages
def IDX_RADIO(url):
    media_item_list('NHK Radio News in Arabic (mp3)', host5+'arabic.xml','','','')
    media_item_list('NHK Radio News in Bengali (mp3)', host5+'bengali.xml','','','')
    media_item_list('NHK Radio News in Burmese (mp3)', host5+'burmese.xml','','','')
    media_item_list('NHK Radio News in Chinese (mp3)', host5+'chinese.xml','','','')
    media_item_list('NHK Radio News in English (mp3)', host5+'english.xml','','','')
    media_item_list('NHK Radio News in French (mp3)', host5+'french.xml','','','')
    media_item_list('NHK Radio News in Hindi (mp3)', host5+'hindi.xml','','','')
    media_item_list('NHK Radio News in Indonesian (mp3)', host5+'indonesian.xml','','','')
    media_item_list('NHK Radio News in Korean (mp3)', host5+'korean.xml','','','')
    media_item_list('NHK Radio News in Persian (mp3)', host5+'persian.xml','','','')
    media_item_list('NHK Radio News in Portuguese (mp3)', host5+'portuguese.xml','','','')
    media_item_list('NHK Radio News in Russian (mp3)', host5+'russian.xml','','','')
    media_item_list('NHK Radio News in Spanish (mp3)', host5+'spanish.xml','','','')
    media_item_list('NHK Radio News in Swahili (mp3)', host5+'swahili.xml','','','')
    media_item_list('NHK Radio News in Thai (mp3)', host5+'thai.xml','','','')
    media_item_list('NHK Radio News in Urdu (mp3)', host5+'urdu.xml','','','')
    media_item_list('NHK Radio News in Vietnamese (mp3)', host5+'vietnamese.xml','','','')

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
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Youtube Search for 'NHK World'",
        url='plugin://plugin.video.youtube/search/?q=NHK World',
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 01",
        url="plugin://plugin.video.youtube/channel/UCySEkVg1Q3QXjDvRFB0H41Q/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 02",
        url="plugin://plugin.video.youtube/channel/UCcajZR_EkvQro0ZgFX6lgtQ/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 03",
        url="plugin://plugin.video.youtube/channel/UCs8DHpkt9f61vUOZO_qwiSQ/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 04",
        url="plugin://plugin.video.youtube/channel/UC4w_dcTPt8iaLE18TB7RLtQ/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 05",
        url="plugin://plugin.video.youtube/playlist/PLKQaIKexM4LJL4GL-lfgvDdlLElTjJIUW/",
        thumbnail=nhk_icon,
        folder=True )
     
    plugintools.add_item( 
        #action="", 
        title="UNESCO/NHK",
        url="plugin://plugin.video.youtube/playlist/PLWuYED1WVJIPKU_tUlzLTfkbNnAtkDOhS/",
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Journeys in Japan",
        url='plugin://plugin.video.youtube/search/?q=intitle:"journeys in japan"',
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="J-Innovators",
        url="plugin://plugin.video.youtube/playlist/PLgpKqm4E4A9oKOHfT-CmjtIppxP0Yp71R/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Seasoning the Seasons",
        url='plugin://plugin.video.youtube/search/?q=intitle:"Seasoning the Seasons"',
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Somewhere Street",
        url="plugin://plugin.video.youtube/playlist/PLlvv-XeEWsbc7iLhLRSGRLF5TkkFf7P9x/",
        thumbnail=nhk_icon,
        folder=True )

    addDir('More Shows', '', 'youtube2', nhk_icon)
    
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
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="NHK Documentary - Silk Road II",
        url="plugin://plugin.video.youtube/playlist/PLdwCuEoZ_6l7FvbsfjidxMIybBrF5jnb5/",
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Begin Japanology 01",
        url="plugin://plugin.video.youtube/channel/UCPMSNvTv2rgODVy0GvsMxZg/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Begin Japanology 02",
        url="plugin://plugin.video.youtube/playlist/PL8IcLS3A4sWKqf47xzXl_NIwlj_Hae5fM/",
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Begin Japanology 03",
        url="plugin://plugin.video.youtube/playlist/PLJ4SclxaotEijsfzIFlUcHG6huoiovh9s/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tokyo Eye",
        url="plugin://plugin.video.youtube/channel/UC5ehEXRuBeVo1gkulk5I4BQ/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="cool japan",
        url="plugin://plugin.video.youtube/playlist/PL54G12jDE7cPq7xbyEyaIf7jRvUC04TJg/",
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Dining with the Chef",
        url="plugin://plugin.video.youtube/playlist/PLIz8fpF_mbPSpMiJ9OHXo5Ai7dYDLXhYM/",
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Sports Japan",
        url="plugin://plugin.video.youtube/playlist/PLIz8fpF_mbPSjA3l8bPyYF2vYZioFl2S1/",
        thumbnail=nhk_icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Meet and Speak",
        url="plugin://plugin.video.youtube/playlist/PLdRCqO13zyDfQuDoZG6pHQuSJ2dbwVWQu/",
        thumbnail=nhk_icon,
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="MoshiMoshi Nippon",
        url="plugin://plugin.video.youtube/playlist/PLpHD2EwLFcoQkHEP7w458jR-kSY_W4mo2/",
        thumbnail=nhk_icon,
        folder=True )

# Create media items list
def media_item_list(name,url,plot,img,fanart):
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
        xmlTag = dom.getElementsByTagName('enclosure')[0].toxml()
        url = re.compile('.+?url="(.+?)".+?').findall(xmlTag)
        radionews_url = str(url).replace("[u'", "").replace("']","")
        addon.add_music_item({'url': radionews_url}, {'title': name}, context_replace = nhk_icon, playlist=False)

    elif mode=='vod' or 'feat_news':
        addon.add_video_item({'url': url}, {'title': name, 'plot': plot}, img = img, fanart = fanart, playlist=False)

    else:
        addon.add_video_item({'url': url}, {'title': name, 'plot': plot}, img = nhk_icon, fanart = fanart, playlist=False)
            


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

elif mode=='jibtv':
    print ""+url
    IDX_JIBTV(url)

elif mode=='jib_rec':
    print ""+url
    JIB_REC(url)

elif mode=='jib_feat':
    print ""+url
    JIB_FEAT(url)

elif mode=='f4m':
    print ""+url
    media_item_list(name,url,'','','')

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
    
elif mode=='feat_news_japan':
    print ""+url
    IDX_FEAT_NEWS(url)

elif mode=='feat_news_asia':
    print ""+url
    IDX_FEAT_NEWS(url)

elif mode=='feat_news_world':
    print ""+url
    IDX_FEAT_NEWS(url)

elif mode=='feat_news_biztec':
    print ""+url
    IDX_FEAT_NEWS(url)

elif mode=='audio':
    print ""+url
    IDX_RADIO(url)

if not play:
    addon.end_of_directory()
