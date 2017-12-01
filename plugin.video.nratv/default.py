import os
import sys
import xbmc,xbmcaddon
import xbmcplugin
import xbmcgui
import plugintools

addon01 = xbmcaddon.Addon('plugin.video.nratv')
addonname = addon01.getAddonInfo('name')
addon_id = 'plugin.video.nratv'
from addon.common.addon import Addon
addon = Addon(addon_id, sys.argv)

icon = addon01.getAddonInfo('icon') # icon.png in addon directory
fanart = addon01.getAddonInfo('fanart') # fanart.jpg in addon directory


# main menu
def CATEGORIES():
    media_item_list('NRA TV Live Stream', 'https://stream1.nra.tv/nratv/ngrp:nratvall/chunklist_b2749440.m3u8','' , icon, fanart)
    IDX_YOUTUBE1()

# Create content list
def addDir(name,url,mode,iconimage):
    params = {'url':url, 'mode':mode, 'name':name}
    addon.add_directory(params, {'title': str(name)}, img = iconimage, fanart = fanart)

# Youtube videos
def IDX_YOUTUBE1():
    plugintools.log("nratv1.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list1(params)
    else:
        pass
    
    plugintools.close_item_list()

# Youtube menu
def main_list1(params):
    plugintools.log("nratv1.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="Youtube Search for 'National Rifle Association'",
        url='plugin://plugin.video.youtube/search/?q=National Rifle Association',
        thumbnail=icon,
        fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NRA TV",
        url="plugin://plugin.video.youtube/user/NRANews/",
        thumbnail="https://yt3.ggpht.com/-F2_HD0G9laQ/AAAAAAAAAAI/AAAAAAAAAAA/EqzbJJh6MuU/s288-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=fanart,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="NRA",
        url="plugin://plugin.video.youtube/user/NRAVideos/",
        thumbnail="http://www.southeastradio.ie/wp-content/uploads/2017/10/NRA.jpeg",
        fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NRA Pubs",
        url="plugin://plugin.video.youtube/user/NRApubs/",
        thumbnail="https://yt3.ggpht.com/-K7UP-3Nvibs/AAAAAAAAAAI/AAAAAAAAAAA/XbY5XdSScPg/s288-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NRA National Firearms Museum",
        url="plugin://plugin.video.youtube/user/NFMCurator/",
        thumbnail="https://yt3.ggpht.com/-FQ_ClCpa64Q/AAAAAAAAAAI/AAAAAAAAAAA/Do1Cs4h29q8/s288-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NRA Women",
        url="plugin://plugin.video.youtube/user/NRAWomen/",
        thumbnail="https://yt3.ggpht.com/-GqGKJRTuZw4/AAAAAAAAAAI/AAAAAAAAAAA/QTfGMN93j0I/s288-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NRA Freestyle",
        url="plugin://plugin.video.youtube/user/nrafreestyle/",
        thumbnail="https://yt3.ggpht.com/-mx9RJ3bJfFQ/AAAAAAAAAAI/AAAAAAAAAAA/C7N8I66dj8k/s288-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NRA General Operations",
        url="plugin://plugin.video.youtube/user/GOnraMedia/",
        thumbnail="https://yt3.ggpht.com/-c0JMaaNvfWE/AAAAAAAAAAI/AAAAAAAAAAA/PAP-cswAjPw/s288-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=fanart,
        folder=True )


# Create media items list
def media_item_list(name,url,plot,img,fanart):
    addon.add_video_item({'url': url}, {'title': name, 'plot': plot}, img = icon, fanart = fanart, playlist=False)

# Query play, mode, url and name
play = addon.queries.get('play', None)
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')

# Program flow control
if play:
    addon.resolve_url(url.encode('UTF-8')) # <<< Play resolved media url

if mode=='main':
    print ""
    CATEGORIES()

elif mode=='youtube1':
    print ""+url
    IDX_YOUTUBE1()

if not play:
    addon.end_of_directory()