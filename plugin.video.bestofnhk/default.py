# Best of NHK - by misty 2013-2015.
# import python libraries
import urllib
import urllib2
import re
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import random
import string
import sys
import os
import time

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

# globals
host1 = 'http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/'
host2 = 'http://www3.nhk.or.jp/'
#host3 = 'http://www3.nhk.or.jp/nhkworld/newsroomtokyo/'
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
    #BROKEN LINK addDir('NHK World Live Stream 1', host1, 'video', icon)
    #BROKEN LINK media_item_list('NHK World Live Stream 2', 'http://plslive-w.nhk.or.jp/nhkworld/app-mainp/live.m3u8')
    addDir('NHK Newsroom Tokyo - Updated daily M-F', host2+'nhkworld/newsroomtokyo/', 'newsroom', icon)
    addDir('NHK Radio News', host2, 'audio', icon)

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

# F4m video
def IDX_VIDEO(url):
    media_item_list('NHK World Live 512',host1+'nhkworld-live-512.f4m')
    
# Newsroom Tokyo news broadcast updated daily M-F
def IDX_NEWS(url):
    link = net.http_GET(url).content
    #print link
    match=re.compile('xml/latest_(.+?).xml').findall(link)
    for name in match:
        print name
        media_item_list('Newsroom Tokyo '+name,'rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld-mov/newsroomtokyo/latest_'+name+'.mp4')
        

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
    media_item_list('NHK Radio News in Korean',host2+radio+'korean.mp3')
    media_item_list('NHK Radio News in Persian',host2+radio+'persian.mp3')
    media_item_list('NHK Radio News in Portugese',host2+radio+'portugese.mp3')
    media_item_list('NHK Radio News in Russian',host2+radio+'russian.mp3')
    media_item_list('NHK Radio News in Spanish',host2+radio+'spanish.mp3')
    media_item_list('NHK Radio News in Swahili',host2+radio+'swahili.mp3')
    media_item_list('NHK Radio News in Thai',host2+radio+'thai.mp3')
    media_item_list('NHK Radio News in Urdu',host2+radio+'urdu.mp3')
    media_item_list('NHK Radio News in Vietnamese',host2+radio+'vietnamese.mp3')

        
# Create media items list
def media_item_list(name,url):
    if mode=='video':
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

elif mode=='video':
    print ""+url
    IDX_VIDEO(url)

elif mode=='newsroom':
    print ""+url
    IDX_NEWS(url)
    
elif mode=='audio':
    print ""+url
    IDX_RADIO(url)

if not play:
    addon.end_of_directory()
