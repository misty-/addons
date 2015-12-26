# -*- coding: utf-8 -*-
#------------------------------------------------------------
# xivetv - youtube channel
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------
# by misty 2015
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.xivetv'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')
fan_art = local.getAddonInfo('fanart')

# Entry point
def run():
    plugintools.log("xivetv.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("xivetv.main_list "+repr(params))
        
    plugintools.add_item( 
        #action="", 
        title="XiveTV",
        url="plugin://plugin.video.youtube/channel/UC62NeTy6Ocd5Jmh_963mLFg/",
        thumbnail=icon,
        fanart=fan_art,
        folder=True )
        

run()