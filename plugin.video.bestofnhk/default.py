# Best of NHK - by misty 2013-2018.
# import python libraries
import urllib
import urllib2
import re
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
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
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
pluginhandle = int(sys.argv[1])

# globals
#host1 = 'http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/'
host2 = 'https://www3.nhk.or.jp/'
host3 = 'https://ak.c.ooyala.com/'
host4 = 'https://player.ooyala.com/player/all/'
host5 = 'https://www.nhk.or.jp/rj/podcast/rss/'
host6 = 'https://www.jibtv.com'
host7 = ''
host8 = 'https://api.nhk.or.jp/nhkworld/vodesdlist/v7/'
host9 = 'https://www3.nhk.or.jp/nhkworld/assets/images/vod/icon/png320/'
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
use_color = settings.getSetting('usecolor')
month = { 1:'01_jan', 2:'02_feb', 3:'03_mar', 4:'04_apr', 5:'05_may', 6:'06_jun',
          7:'07_jul', 8:'08_aug', 9:'09_sep', 10:'10_oct', 11:'11_nov', 12:'12_dec' }
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

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

sch = 'https://api.nhk.or.jp/nhkworld/epg/v7/world/s'+str(int(start_time))+'-e'+str(int(end_time))+'.json?%s' % apikey
now = 'https://api.nhk.or.jp/nhkworld/epg/v7/world/now.json?%s' % apikey


# Main Menu
def CATEGORIES():
    addDir('NHK World Live Schedule', '', 'schedule', nhk_icon)
    addDir('NHK World Live Stream', '', 'live_strm', nhk_icon)
    addDir('NHK World On Demand', '', 'vod_cats', nhk_icon)
    addDir('JIBTV On Demand', 'https://www.jibtv.com/programs/', 'jibtv', jib_icon)
    addDir('NHK World News', '', 'news', nhk_icon)
    addDir('NHK Radio News', '', 'audio', nhk_icon)
    addDir('NHK Videos on Youtube', '', 'youtube1', nhk_icon)

# Create content list
def addDir(name,url,mode,iconimage):
    params = {'url':url, 'mode':mode, 'name':name}
    addon.add_directory(params, {'title': str(name)}, img = iconimage, fanart = 'https://www.jnto.go.jp/eng/wallpaper/'+str_Yr+'/img/type-a/1920-1080/'+month[Mth]+'.jpg')

def addDir1(name,url,mode,iconimage):
    params = {'url':url, 'mode':mode, 'name':name, 'iconimage':iconimage}
    addon.add_directory(params, {'title': str(name)}, img = iconimage, fanart = iconimage)

def addDir2(name,url,mode,plot,iconimage):
    params = {'url':url, 'mode':mode, 'name':name, 'plot':plot, 'iconimage':iconimage}
    addon.add_directory(params, {'title': str(name), 'plot': plot}, img = iconimage, fanart = iconimage)

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
        if use_color == "true":
            f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
        else:
            f.write('[B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B]' + '  -  ' + desc.encode('UTF-8') + '\n' + '\n')
    else:
        if use_color == "true":
            f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
        else:
            f.write('[B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B]' + '  -  ' + desc.encode('UTF-8') + '\n' + '\n')
    f.write('[B]Next:[/B]' + '\n' + '\n')
    
    try:
        for i in range(1,4):
            pubDate = int(pl_now['channel']['item'][i]['pubDate'])
            name = pl_now['channel']['item'][i]['title']
            desc = pl_now['channel']['item'][i]['description']
            sub_name = pl_now['channel']['item'][i]['subtitle']
            show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
            if sub_name == "":
                if use_color == "true":
                    f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
                else:
                    f.write('[B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B]' + '  -  ' + desc.encode('UTF-8') + '\n' + '\n')
            else:
                if use_color == "true":
                    f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
                else:
                    f.write('[B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B]' + '  -  ' + desc.encode('UTF-8') + '\n' + '\n')
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
                if use_color == "true":
                    f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
                else:
                    f.write('[B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B]' + '  -  ' + desc.encode('UTF-8') + '\n' + '\n')
            else:
                if use_color == "true":
                    f.write('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]' + '  -  ' + '[COLOR green]' + desc.encode('UTF-8') + '[/COLOR]' + '\n' + '\n')
                else:
                    f.write('[B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B]' + '  -  ' + desc.encode('UTF-8') + '\n' + '\n')
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
    thumbnl_ = pl_now['channel']['item'][0]['thumbnail']
    thumbnl = host2[:-1]+thumbnl_
    show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
    # menu
    if TimeZone == '(GMT+09:00) Osaka, Sapporo, Tokyo':
        media_item_list(name.encode('UTF-8') + ' - 720', 'https://nhkwlive-xjp.akamaized.net/hls/live/2003458/nhkwlive-xjp/index_2M.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
        media_item_list(name.encode('UTF-8') + ' - 1080', 'https://nhkwlive-xjp.akamaized.net/hls/live/2003458/nhkwlive-xjp/index_4M.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
    else:
        media_item_list(name.encode('UTF-8') + ' - 720', 'https://nhkwlive-xjp.akamaized.net/hls/live/2003458/nhkwlive-xjp/index_2M.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
        media_item_list(name.encode('UTF-8') + ' - 1080', 'https://nhkwlive-xjp.akamaized.net/hls/live/2003458/nhkwlive-xjp/index_4M.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
    try:
        if sub_name == "":
            if use_color == "true":
                addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
            else:
                addLink('[B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
        else:
            if use_color == "true":
                addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
            else:
                addLink('[B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
        for i in range(1,20):
            pubDate = int(pl_now['channel']['item'][i]['pubDate'])
            name = pl_now['channel']['item'][i]['title']
            desc = pl_now['channel']['item'][i]['description']
            sub_name = pl_now['channel']['item'][i]['subtitle']
            thumbnl_ = pl_now['channel']['item'][i]['thumbnail']
            thumbnl = host2[:-1]+thumbnl_
            show_time = str(datetime.datetime.fromtimestamp(pubDate/1000).strftime('%H:%M'))
            if sub_name == "":
                if use_color == "true":
                    addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B][/COLOR]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
                else:
                    addLink('[B]' + show_time + ' - ' + name.encode('UTF-8') + '[/B]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
            else:
                if use_color == "true":
                    addLink('[COLOR blue][B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B][/COLOR]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
                else:
                    addLink('[B]' + show_time + ' - ' + name.encode('UTF-8') + ' - ' + sub_name.encode('UTF-8') + '[/B]', '', desc.encode('UTF-8'), thumbnl, thumbnl)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

def IDX_VOD_CATS(url):
    addDir('On Demand Full Listing', host8+'all/all/en/all/all.json?%s' % apikey, 'vod', nhk_icon)
    addDir('Latest Episodes', host8+'all/all/en/all/12.json?%s' % apikey, 'vod', nhk_icon)
    addDir('Most Watched', host8+'mostwatch/all/en/all/12.json?%s' % apikey, 'vod', nhk_icon)
    addDir('Art & Design', host8+'category/19/en/all/all.json?%s' % apikey, 'vod', host9+'19.png')
    addDir('Biz/Tech', host8+'category/14/en/all/all.json?%s' % apikey, 'vod', host9+'14.png')
    addDir('Culture & Lifestyle', host8+'category/20/en/all/all.json?%s' % apikey, 'vod', host9+'20.png')
    addDir('Current Affairs', host8+'category/12/en/all/all.json?%s' % apikey, 'vod', host9+'12.png')
    addDir('Debate', host8+'category/13/en/all/all.json?%s' % apikey, 'vod', host9+'13.png')
    addDir('Disaster Preparedness', host8+'category/29/en/all/all.json?%s' % apikey, 'vod', host9+'29.png')
    addDir('Documentary', host8+'category/15/en/all/all.json?%s' % apikey, 'vod', host9+'15.png')
    addDir('Drama', host8+'category/26/en/all/all.json?%s' % apikey, 'vod', host9+'26.png')
    addDir('Entertainment', host8+'category/21/en/all/all.json?%s' % apikey, 'vod', host9+'21.png')
    addDir('Food', host8+'category/17/en/all/all.json?%s' % apikey, 'vod', host9+'17.png')
    #addDir('Interactive', host8+'category/27/en/all/all.json?%s' % apikey, 'vod', host9+'27.png')
    addDir('Interview', host8+'category/16/en/all/all.json?%s' % apikey, 'vod', host9+'16.png')
    addDir('Learn Japanese', host8+'category/28/en/all/all.json?%s' % apikey, 'vod', host9+'28.png')
    addDir('News', host8+'category/11/en/all/all.json?%s' % apikey, 'vod', host9+'11.png')
    addDir('Pop Culture & Fashion', host8+'category/22/en/all/all.json?%s' % apikey, 'vod', host9+'22.png')
    addDir('Science & Nature', host8+'category/23/en/all/all.json?%s' % apikey, 'vod', host9+'23.png')
    addDir('Sport', host8+'category/25/en/all/all.json?%s' % apikey, 'vod', host9+'25.png')
    addDir('Travel', host8+'category/18/en/all/all.json?%s' % apikey, 'vod', host9+'18.png')

# video on demand
def IDX_VOD(url):
    req = urllib2.urlopen(url)
    vod_json = json.load(req)
    try:
        for i in range(3000):
            series_ = vod_json['data']['episodes'][i]['title']
            ep_name_ = vod_json['data']['episodes'][i]['sub_title']
            plot_ = vod_json['data']['episodes'][i]['description']
            thumbnl_ = vod_json['data']['episodes'][i]['image_l']
            vid_id = vod_json['data']['episodes'][i]['vod_id']
            series = (series_).encode('UTF-8').replace('[\'','').replace('\']','').replace('<br />',' ').replace('<span style="font-style: italic;">', '').replace('</span>','')
            ep_name = (ep_name_).encode('UTF-8').replace('<br>',' ').replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('\\xd7','x').replace('\\xc3\\x97','x').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','')
            plot = (plot_).encode('UTF-8').replace('<br>',' ').replace('&#9825;',' ').replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('<em>','').replace('</em>','').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','')
            thumbnl = host2[:-1]+thumbnl_
            addDir2(series + ' - ' + ep_name, vid_id, 'vod_resolve', plot, thumbnl)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

def VOD_RESOLVE(name,url,plot,iconimage):
    if url[0:4] == 'nw_v':
        vid_id = str(url)
        req = urllib2.Request('https://movie-s.nhk.or.jp/v/refid/nhkworld/prefid/'+vid_id+'?embed=js&targetId=videoplayer&de-responsive=true&de-callback-method=nwCustomCallback&de-appid='+vid_id+'&de-subtitle-on=false', headers=hdr)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match = re.compile("'data-de-program-uuid','(.+?)'").findall(link)
        for p_uuid_ in match:
            p_uuid = str(p_uuid_).replace("['" , "").replace("']" , "")
            req = urllib2.urlopen('https://movie-s.nhk.or.jp/ws/ws_program/api/67f5b750-b419-11e9-8a16-0e45e8988f42/apiv/5/mode/json?v='+p_uuid)
            vod_json = json.load(req)
            vlink = vod_json['response']['WsProgramResponse']['program']['asset']['ipadM3u8Url']
            media_item_list(name, vlink, plot, iconimage, iconimage)
    elif url[0:6] != 'nw_vod':
        vid_id = str(url)
        media_item_list(name, host4 + vid_id + '.m3u8', plot, iconimage, iconimage)

# jibtv
'''
def IDX_JIBTV(url):
    addDir('Recommended', 'http://jibtv.com/', 'jib_rec', jib_icon)
    addDir('Featured Programs', 'http://jibtv.com/programs/', 'jib_feat', jib_icon)
'''
def IDX_JIBTV(url):
    link = net.http_GET(url).content
    match1 = re.compile('<tr data-href="(.+?)">\r\n\t*<td class="text-center w-40"><img src="(.+?)" class="img-responsive img-rounded" width="100%" /></td>\r\n\t*<td><span class="font-500">(.+?)</span><span ').findall(link)
    match2 = re.compile('<tr data-href="(.+?)">\r\n\t*<td class="text-center w-40"><img src="(.+?)" class="img-responsive img-rounded" width="100%" /></td>\r\n\t*<td><span class="font-500">(.+?)\r\n</span><span ').findall(link)
    match3 = re.compile('<tr data-href="(.+?)">\n\t*<td class="text-center w-40"><img src="(.+?)" class="img-responsive img-rounded" width="100%" /></td>\n\t*<td><span class="font-500">(.+?)</span><span ').findall(link)
    match4 = re.compile('<tr data-href="(.+?)">\n\t*<td class="text-center w-40"><img src="(.+?)" class="img-responsive img-rounded" width="100%" /></td>\n\t*<td><span class="font-500">(.+?)\n</span><span ').findall(link)
    for vid_page_, thumbnl_, title_ in match1 + match2 + match3 + match4:
        vid_page = host6+vid_page_
        thumbnl = host6+thumbnl_
        title = (title_).encode('UTF-8').replace('<br>',' - ').replace('<br />',' - ')
        addDir1(title, vid_page, 'jib_feat', thumbnl)
'''
def JIB_REC(url):
    link = net.http_GET(url).content
    match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
    #thumb_=re.compile('<img src="programs/(.+?)"').findall(link)
    for vid_page, title_ in match:
        try:
            link1 = net.http_GET('http://jibtv.com/%s' % vid_page).content
            desc_ = re.compile('<meta property="og:description" content="(.+?)" />').findall(link1)
            plot = ''.join(desc_)
            thumb = re.compile('<meta property="og:image" content="(.+?)"').findall(link1)
            thumb1 = re.compile('<meta content="(.+?)" property="og:image"').findall(link1)
            thumbnl = ''.join(thumb).replace('showcace','showcase')
            thumbnl1 = ''.join(thumb1).replace('showcace','showcase')
            meta_id = re.compile('player.play\(\{ meta_id: (.+?) \}\)').findall(link1)
            vid_id = ''.join(meta_id)
            link2 = net.http_GET('http://jibtv-vcms.logica.bz/api/v1/metas/%s/medias' % vid_id).content
            vid_src_ = re.compile('"url":"(.+?)"').findall(link2)
            vid_src = ''.join(vid_src_)
            title = (title_).encode('UTF-8').replace('<br />',' - ')
            if thumbnl == "":
                media_item_list(title, vid_src, plot, thumbnl1, thumbnl1)
            elif thumbnl1 == "":
                media_item_list(title, vid_src, plot, thumbnl, thumbnl)
            elif thumbnl and thumbnl1 == "":
                media_item_list(title, vid_src, plot, jib_icon , 'http://www3.nhk.or.jp/nhkworld/en/calendar'+str_Yr+'/images/large/'+str_Mth+'.jpg')
        except:
            pass
        xbmcplugin.setContent(pluginhandle, 'episodes')
'''
def JIB_FEAT(url,iconimage): 
    link = net.http_GET(url).content
    try:
        title_ = re.compile('<meta property="og:title" content="(.+?)"').findall(link)
        titl_e = ''.join(title_)
        title = (titl_e).encode('UTF-8').replace('<br />',' - ')
        desc_ = re.compile('<meta property="og:description" content="(.+?)"').findall(link)
        plot = ''.join(desc_)
        meta_id = re.compile('play\(\{ meta_id: (.+?) \}\)').findall(link)
        vid_id_ = ''.join(meta_id)
        vid_id = vid_id_[0:3]
        try:
            link2 = net.http_GET('https://jibtv-vcms.logica.io/api/v1/metas/%s/medias' % vid_id).content
            vid_src_ = re.compile('"url":"(.+?)"').findall(link2)
            vid_src = ''.join(vid_src_)
            media_item_list(title, vid_src, plot, iconimage, iconimage)
        except:
            link2 = net.http_GET('https://jibtv-vcms.logica.io/api/v1/metas/%s/playlist' % vid_id).content
            match1=re.compile('"metas":\[\{"meta_id":(.+?),"name":"(.+?)".+?,\{"meta_id":(.+?),"name":"(.+?)"').findall(link2)
            for vid_id1, title1, vid_id2, title2 in match1:
                link3 = net.http_GET('https://jibtv-vcms.logica.io/api/v1/metas/%s/medias' % vid_id1).content
                link4 = net.http_GET('https://jibtv-vcms.logica.io/api/v1/metas/%s/medias' % vid_id2).content
                vid_src1_ = re.compile('"url":"(.+?)"').findall(link3)
                vid_src1 = ''.join(vid_src1_)
                media_item_list(title1, vid_src1, plot, iconimage, iconimage)
                vid_src2_ = re.compile('"url":"(.+?)"').findall(link4)
                vid_src2 = ''.join(vid_src2_)
                media_item_list(title2, vid_src2, plot, iconimage, iconimage)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

# New NHK News
def IDX_NEWS(url):
    addDir('NHK Top Stories', host2+'nhkworld/data/en/news/all.json', 'topnews', nhk_icon)
    addDir('Newsline', host2+'nhkworld/data/en/news/programs/1001.xml', 'the_news', nhk_icon)
    addDir('Newsroom Tokyo', host2+'nhkworld/data/en/news/programs/1002.xml', 'the_news', nhk_icon)
    addDir('Newsline Asia 24', host2+'nhkworld/data/en/news/programs/1003.xml', 'the_news', nhk_icon)
    addDir('Newsline Biz', host2+'nhkworld/data/en/news/programs/1004.xml', 'the_news', nhk_icon)
    addDir('Newsline In Depth', host2+'nhkworld/data/en/news/programs/1005.xml', 'the_news', nhk_icon)

def THE_NEWS(url):
    req = urllib2.Request(url, headers=hdr)
    file = urllib2.urlopen(req)
    data = file.read()
    file.close()
    dom = parseString(data)
    v_url = dom.getElementsByTagName('file.high')[0].toxml()
    image = dom.getElementsByTagName('image')[0].toxml()
    name = dom.getElementsByTagName('media.title')[0].toxml()
    vid_url = v_url.replace('<file.high><![CDATA[','').replace(']]></file.high>','')
    thumbnl = host2 + image.replace('<image><![CDATA[/','').replace(']]></image>','')
    name_ = name.replace('<media.title>','').replace('</media.title>','').replace("_#039_","'").replace('_quot_','"')
    media_item_list(name_,vid_url,'',thumbnl,thumbnl)

'''
# Newsroom Tokyo news broadcast updated daily M-F
def IDX_NEWS(url):
    link = net.http_GET(url).content
    match1=re.compile('nw_addPlayer\(\'movie-area\', \{lang: \'en\', media: \'tv\', type: \'vod\', source: \'(.+?)\', callback: playerCallback\}\)').findall(link)
    match2=re.compile('<h3></h3>\n.+?<p class="date">(.+?)</p>').findall(link)
    vid_id = str(match1).replace("['","").replace("']","")
    d_ate = str(match2).replace("['","").replace("']","")
    icon = "https://www3.nhk.or.jp/nhkworld/newsroomtokyo/img/common/logo.png"
    fanart_ = "https://www3.nhk.or.jp/nhkworld/newsroomtokyo/img/top/our_team.jpg"
    media_item_list('Newsroom Tokyo for '+ d_ate, host4 + vid_id + '.m3u8','', icon, fanart_)
'''
# Latest top news stories
def IDX_TOPNEWS(url):
    
    req = urllib2.Request(url, headers=hdr)
    file = urllib2.urlopen(req)
    top_json = json.load(file)
    try:
        for i in range(200):
            if top_json['data'][i]['videos']:
                xml_link = top_json['data'][i]['videos']['config']
                req = urllib2.Request((host2[:-1]+xml_link), headers=hdr)
                file = urllib2.urlopen(req)
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
'''
# Feature news stories
def IDX_FEATURE(url):
    addDir('NHK News Feature Stories - Japan', url, 'feat_news_japan', nhk_icon)
    addDir('NHK News Feature Stories - Asia', url, 'feat_news_asia', nhk_icon)
    addDir('NHK News Feature Stories - World', url, 'feat_news_world', nhk_icon)
    addDir('NHK News Feature Stories - BizTec', url, 'feat_news_biztec', nhk_icon)

def IDX_FEAT_NEWS(url):
    req = urllib2.Request(url, headers=hdr)
    file = urllib2.urlopen(req)
    feat_json = json.load(file)
    try:
        for i in range(300):
            #thumbnl = feat_json['data'][i]['thumbnails']['middle']
            xml_link = feat_json['data'][i]['videos']['config']
            #title = feat_json['data'][i]['title']
            cat = feat_json['data'][i]['categories']['name']
            if mode == 'feat_news_japan' and cat == 'JAPAN' or mode == 'feat_news_asia' and cat == 'ASIA' or mode == 'feat_news_world' and cat == 'WORLD' or mode == 'feat_news_biztec' and cat == 'BIZTCH':
                req = urllib2.Request((host2[:-1]+xml_link), headers=hdr)
                file = urllib2.urlopen(req)
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
'''
# Pre-recorded NHK World Radio in 17 languages
def IDX_RADIO(url):
    fanart = 'https://www.jnto.go.jp/eng/wallpaper/'+str_Yr+'/img/type-a/1920-1080/'+month[Mth]+'.jpg'
    media_item_list('NHK Radio News in Arabic (mp3)', host5+'arabic.xml','','',fanart)
    media_item_list('NHK Radio News in Bengali (mp3)', host5+'bengali.xml','','',fanart)
    media_item_list('NHK Radio News in Burmese (mp3)', host5+'burmese.xml','','',fanart)
    media_item_list('NHK Radio News in Chinese (mp3)', host5+'chinese.xml','','',fanart)
    media_item_list('NHK Radio News in English (mp3)', host5+'english.xml','','',fanart)
    media_item_list('NHK Radio News in French (mp3)', host5+'french.xml','','',fanart)
    media_item_list('NHK Radio News in Hindi (mp3)', host5+'hindi.xml','','',fanart)
    media_item_list('NHK Radio News in Indonesian (mp3)', host5+'indonesian.xml','','',fanart)
    media_item_list('NHK Radio News in Korean (mp3)', host5+'korean.xml','','',fanart)
    media_item_list('NHK Radio News in Persian (mp3)', host5+'persian.xml','','',fanart)
    media_item_list('NHK Radio News in Portuguese (mp3)', host5+'portuguese.xml','','',fanart)
    media_item_list('NHK Radio News in Russian (mp3)', host5+'russian.xml','','',fanart)
    media_item_list('NHK Radio News in Spanish (mp3)', host5+'spanish.xml','','',fanart)
    media_item_list('NHK Radio News in Swahili (mp3)', host5+'swahili.xml','','',fanart)
    media_item_list('NHK Radio News in Thai (mp3)', host5+'thai.xml','','',fanart)
    media_item_list('NHK Radio News in Urdu (mp3)', host5+'urdu.xml','','',fanart)
    media_item_list('NHK Radio News in Vietnamese (mp3)', host5+'vietnamese.xml','','',fanart)

def IDX_YOUTUBE1():
    plugintools.log("nhkworld1.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list1(params)
    else:
        #action = params.get("action")
        #exec action+"(params)"
        pass
    
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
        title="Youtube Search for 'NHK BS'",
        url='plugin://plugin.video.youtube/search/?q=NHK BS',
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
        title="NHK Documentary",
        url='plugin://plugin.video.youtube/search/?q=NHK Documentary',
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Begin Japanology",
        url="plugin://plugin.video.youtube/search/?q=Begin Japanology",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Japanology Plus",
        url="plugin://plugin.video.youtube/search/?q=Japanology Plus",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tokyo Eye",
        url="plugin://plugin.video.youtube/search/?q=Tokyo Eye",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Trails to Tsukiji",
        url="plugin://plugin.video.youtube/search/?q=Trails to Tsukiji",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dining with the Chef",
        url="plugin://plugin.video.youtube/search/?q=Dining with the chef",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Document 72 Hours",
        url="plugin://plugin.video.youtube/search/?q=Document 72 hours",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Blends",
        url="plugin://plugin.video.youtube/search/?q=NHK Blends",
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
        title="Core Kyoto",
        url="plugin://plugin.video.youtube/search/?q=NHK Core Kyoto",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Japan Railway Journal",
        url="plugin://plugin.video.youtube/search/?q=NHK Japan Railway Journal",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="J-Trip Plan",
        url="plugin://plugin.video.youtube/search/?q=NHK J-Trip Plan",
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
        url="plugin://plugin.video.youtube/search/?q=NHK Somewhere Street",
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
        #action = params.get("action")
        #exec action+"(params)"
        pass
    
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
        title="NHK World Shows 01",
        url="plugin://plugin.video.youtube/channel/UCs8DHpkt9f61vUOZO_qwiSQ/",
        thumbnail=nhk_icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NHK World Shows 02",
        url="plugin://plugin.video.youtube/playlist/PLKQaIKexM4LJL4GL-lfgvDdlLElTjJIUW/",
        thumbnail=nhk_icon,
        folder=True )
       
    plugintools.add_item( 
        #action="", 
        title="Begin Japanology",
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
        title="Japan-easy",
        url="plugin://plugin.video.youtube/playlist/PLLbOFqwYMFi9scMpmRKU-a8260EG7R_bJ/",
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
    if mode=='audio':
        req = urllib2.Request(url, headers=hdr)
        file = urllib2.urlopen(req)
        data = file.read()
        file.close()
        dom = parseString(data)
        xmlTag = dom.getElementsByTagName('enclosure')[0].toxml()
        url = re.compile('.+?url="(.+?)".+?').findall(xmlTag)
        radionews_url = str(url).replace("[u'", "").replace("']","")
        addon.add_music_item({'url': radionews_url}, {'title': name}, context_replace = nhk_icon, fanart = fanart, playlist=False)
        
    else:
        addon.add_video_item({'url': url}, {'title': name, 'plot': plot}, img = img, fanart = fanart, playlist=False)


# Downloader
#def download_media():
#    print df

# Query play, mode, url and name
play = addon.queries.get('play', None)
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
iconimage = addon.queries.get('iconimage', '')
plot = addon.queries.get('plot', '')

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

elif mode=='vod_cats':
    print ""+url
    IDX_VOD_CATS(url)

elif mode=='vod_resolve':
    print ""+url
    VOD_RESOLVE(name,url,plot,iconimage)

elif mode=='jibtv':
    print ""+url
    IDX_JIBTV(url)

elif mode=='jib_rec':
    print ""+url
    JIB_REC(url)

elif mode=='jib_feat':
    print ""+url
    JIB_FEAT(url,iconimage)

elif mode=='youtube1':
    print ""+url
    IDX_YOUTUBE1()
    
elif mode=='youtube2':
    print ""+url
    IDX_YOUTUBE2()

elif mode=='news':
    print ""+url
    IDX_NEWS(url)

elif mode=='the_news':
    print ""+url
    THE_NEWS(url)

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