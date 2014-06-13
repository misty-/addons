# Best of NHK - by misty 2013/2014.
# import python libraries
import urllib
import urllib2
import re
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

# globals
host = 'http://bestofnhk.tv/'
host2 = 'http://www3.nhk.or.jp/'
radio = 'rj/podcast/mp3/'
shows = 'http://bestofnhk.tv/shows/'
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
    media_item_list('NHK World Live Stream 1','http://plslive-w1.nhk.or.jp/http-live/nhkworld-ios-live1/delivery/index_high.m3u8')
    media_item_list('NHK World Live Stream 2','http://www.widih.com/widih-tv/s-3/nhk.m3u8')
    addDir('NHK Radio News', host2, 'audio', icon)
    addDir('Latest Shows', host, 'latest', icon)
    addDir('Shows by Name', host, 'by_name', icon)
    addDir('Random Show', host, 'by_random', icon)


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


# Simple website scrape for content list
def IDX_LATEST_SHOWS(url):
    link = net.http_GET(url).content
    match=re.compile('<option value="(.+?).flv" >(.+?)&nbsp;&nbsp;&nbsp;(.+?)</option>').findall(link)
    for url,date,name in match:
        media_item_list(url.encode('UTF-8'),shows+url+'.flv')


# Simple website scrape for content list
def IDX_SHOWS_BY_NAME(url):
    link = net.http_GET(url).content
    match=re.compile('<option value="(.+?).flv" >(.+?)&nbsp;&nbsp;&nbsp;(.+?)</option>').findall(link)
    match.sort()
    for url,name,date in match:
        media_item_list(url.encode('UTF-8'),shows+url+'.flv')


# Play a random video
def IDX_RANDOM_SHOW(url):
    link = net.http_GET(host).content
    match=re.compile('<option value="(.+?).flv" >(.+?)&nbsp;&nbsp;&nbsp;(.+?)</option>').findall(link)
    rnd_match = random.choice(match)
    for url in rnd_match:
        addon.add_video_item({'url': shows+url+'.flv'}, {'title': url}, img = icon, playlist=False)
        addon.resolve_url(url.encode('UTF-8'))
        addon.end_of_directory()

        
# Create media items list
def media_item_list(name,url):
    if mode=='audio':
        addon.add_music_item({'url': url}, {'title': name}, context_replace = icon, playlist=False)
    elif mode!='audio':    
        addon.add_video_item({'url': url}, {'title': name}, img = icon, playlist=False)


# Downloader
def download_media():
    print df

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

elif mode=='audio':
    print ""+url
    IDX_RADIO(url)

elif mode=='latest':
    print ""+url
    IDX_LATEST_SHOWS(url)

elif mode=='by_name':
    print ""+url
    IDX_SHOWS_BY_NAME(url)
    
elif mode=='by_random':
    print ""+url
    IDX_RANDOM_SHOW(url)    

if not play:
    addon.end_of_directory()
