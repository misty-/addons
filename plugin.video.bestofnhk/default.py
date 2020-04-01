# Best of NHK - by misty 2013-2020.
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
from random import randrange
#print(randrange(10))
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
host8 = 'https://api.nhk.or.jp/nhkworld/vodesdlist/v7a/'
host9 = 'https://www3.nhk.or.jp/nhkworld/assets/images/vod/icon/png320/'
host10 = 'https://api.nhk.or.jp/nhkworld/pg/v6a/'
host11 = 'https://www3.nhk.or.jp/nhkworld/upld/thumbnails/en/news/programs/'
host12 = 'https://api.nhk.or.jp/nhkworld/vodcliplist/v7a/'
host13 = 'https://api.nhk.or.jp/nhkworld/rdonews/v6a/'
host14 = 'https://api.nhk.or.jp/nhkworld/vodplaylist/v7a/'
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
lang = { 0:'Arabic', 1:'Bengali', 2:'Burmese', 3:'Chinese', 4:'English', 5:'French', 6:'Hindi',
         7:'Indonesia', 8:'Japanese', 9:'Korean', 10:'Persian', 11:'Portuguese', 12:'Russian',
         13:'Spanish', 14:'Swahili', 15:'Thai', 16:'Urdu', 17:'Vietnamese' }
lang_key = { 0:'ar', 1:'bn', 2:'my', 3:'zh', 4:'en', 5:'fr', 6:'hi', 7:'id', 8:'ja',
            9:'ko', 10:'fa', 11:'pt', 12:'ru', 13:'es', 14:'sw', 15:'th', 16:'ur', 17:'vi' }
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
       
s_dict={}; e_dict={}; v_dict={}; p_dict={}; t_dict={}; req1_dict={}; link_dict={}

z = randrange(133)

img = {0:'video/2053171/images/O0YyXBlk2CyLbEjZZFPyrl7dpA4jknc0bhYu9iWl.jpeg', 1:'video/2079016/images/Taf9c2PrMleSaB7DdYE6YX5acL9y6b6ywddV57tG.jpeg', 
        2:'video/3019104/images/U8ftOKW2BDqmlqgXLm2P5vSomn7Pj4MhPkh17I6g.jpeg', 3:'video/2079012/images/uUdt6pekz0KBANhUhV9uA1KJWYfgFO1yRUC8EC3r.jpeg',
        4:'video/2064032/images/SL3FKzFGgrte1t78Ncs0uGnPHhIZor4sfTHhSShu.jpeg', 5:'video/2053166/images/Bk575HEqWeQQtCAxdoCFLxcgHd4nKYj3Lsb7OAIj.jpeg',
        6:'video/9111005/images/QRBsV1cIdplD4mt87yjNc5X9VlhHAwP4XE4gA56R.jpeg', 7:'video/2029117/images/96a53dfd1b6e98e048d17d01899b3ee53eb26a31.jpg',
        8:'video/3019073/images/RTpidoWBkKSMN7KPvXKFkTJ0hGn4caxfelZxkqId.jpeg', 9:'video/2007398/images/pYmhSPIcfIgcMHkp7Aos6PJyocFkwPPCdSDnBaVf.jpeg',
        10:'video/2064028/images/FcblA0xVQcIrmChpDhMPXlzzcDYNVRIhWu0uBHIT.jpeg', 11:'video/3004615/images/kijkIzg7gcFqjUKcw78vmbCdwMH54C7qXIxP4ZJC.jpeg',
        12:'video/2029125/images/1sBRY2CltpgNfNobToUXbd8J2jXwgi5ouDW98ae5.jpeg', 13:'video/2007390/images/MOwAz7U062d8vtllEdXmx59nkRyDySRjnPNF6Un2.jpeg',
        14:'video/2029123/images/Kjn122N5bKfqjkHUvCOZnoXpn7mXs62S0oM5bDuA.jpeg', 15:'video/2029111/images/b22ba676282bb4922538ef23e3516624b9537266.jpg',
        16:'video/2059049/images/e96bcf43c15390d21a21514372a0cdc2a32b78ec.jpg', 17:'video/2007150/images/ZPDvrpcvYW4zXNRwxQCOa57pYB1tKp6obtWVcoSc.jpeg',
        18:'video/2046073/images/e3ac6115be9d6ff77816168850fa89a47f85c320.jpg', 19:'video/6119006/images/rbP8zsNXShZKpOmdBx4hbmvXnjMXZiNzti3yk3Iy.jpeg',
        20:'video/2059076/images/bW5X1HuzEQpGwdEh8T2bqk4JAnrPzZXyFELkUICM.jpeg', 21:'video/2029106/images/422641daa78a4651c2263214f85b38dfaa66f76b.jpg',
        22:'video/2064011/images/4d7bc151e9017385078a6686eed9c546dfc4fd7b.jpg', 23:'video/2032183/images/GVK4GGPV0aScRCsR7g2MmqauK6BAFDIl7CTQ6Wuz.jpeg',
        24:'video/2064009/images/0f4dc9f98599c3187279a9f16cef5ef2d5f6e964.jpg', 25:'video/3004582/images/fNvoGcevk9GKYVtUvPWHrjrZlI60BKhVB89EMc01.jpeg',
        26:'video/2066020/images/uw3jRuNpdqXiffNPt0jV7j2DT7B8hjzRdFMVg4Gs.jpeg', 27:'video/6023026/images/BLdfRUgKQzluaZ1NHVWKRvsjFzBLwb0XmzluQTKH.jpeg',
        28:'video/6024014/images/BtNgodMdLv8x8zA7zxtxvaFjVp7yYx7yp4UGgqaV.jpeg', 29:'video/2046084/images/2c8aa6a76b36041de06ee0811388aaaad0455b6c.jpg',
        30:'video/3004513/images/dfe21def666d8e6edd836448d193b24352748753.jpg', 31:'video/2029110/images/a832fbe4dffe156ae0ee2c39ba17f8b56a2a43f0.jpg',
        32:'video/3004454/images/JvKM3qNkjHwNstK962ZFg8CJj6EdIdfpOPU8s05J.jpeg', 33:'video/3019109/images/kWsJOoQf3c0N1ZfehhmqOoTlZdV9mYr7k6i29X7J.jpeg',
        34:'video/2079003/images/v3MprittwgQSlIJo24sg8WihWKDrXMJzS08VXoK3.jpeg', 35:'video/5003094/images/dc4d6ed666c0a2ae39cb8088d72a30b5845ef001.jpg',
        36:'video/6121002/images/7BKeV3WZz2RigltNN9tyehK4jZmaSwp67Um0VkAp.jpeg', 37:'video/6121001/images/1t9R5PktLQFjTwnHLgBTp3fh38kJjm3siHQI6gh4.jpeg',
        38:'video/6120002/images/DlurEdgrWEfSocwkpeRFKo1N3bqMHUQ6ELgT78yK.jpeg', 39:'video/2061342/images/1omTb6Ed1z3VNPG9ch0j61avgSubEYQMPXAolFXi.jpeg',
        40:'video/2029104/images/55bc04d408b7cab74b50097c8faf699d09f8c7f8.jpg', 41:'video/2061340/images/kRokNUDEb1hl5pd05moiZxUMyavYfysvEsgCNzB1.jpeg',
        42:'video/2061339/images/7RXc1jtahLNWS9Fkj4Pam94aTqwoeCNhpu0yQr11.jpeg', 43:'video/2079017/images/RnyYCYFvjp7stAb2cxNfCgbMoVCTT79olm1s0DrZ.jpeg',
        44:'video/2061336/images/6ZzrtTySligelx9MPrMw74eGoJRmlWHHSbiAVTso.jpeg', 45:'video/2004351/images/WOtHa3l8JjwQVu2wyKe9QSTlGDvDpfcNRILTqUbr.jpeg',
        46:'video/2079005/images/gs2C2vYUzDsM5VHxYHNXLhPnS2QV6OvqmjFT3S7Z.jpeg', 47:'video/3004649/images/B19jqkG9OdtB0fokEBONKqKkcO1rQQL8eCTFlONN.jpeg',
        48:'video/2068019/images/f8iZwgghpyRckVqwWDsLICyJgLin0aOpT6tRA12H.jpeg', 49:'video/2029133/images/0zqSOqrKdxl6xvnR6A02RdEmoMyMuCLeCMStFDXD.jpeg',
        50:'video/2032193/images/rrwDGEq4ezLP9sEDjfXnlO5hvsbeQPnI1UyQ8dcH.jpeg', 51:'video/2029130/images/UWs2eFqi0ZA2gJwNltyNRZtlTEdxPw87qUhgVeX2.jpeg',
        52:'video/2029101/images/jyaxRwRUi0tX7roRDDMdhjbksA270Puwt2yRIrrr.jpeg', 53:'video/3019098/images/l4OSOiFVsQTCrUPMnPsVDFfUoF6p1M4nnZYKsMCa.jpeg',
        54:'video/3019022/images/RtS14vWB3k8hqPNDbvL1lb3AbeT0YztV9j5TzluY.jpeg', 55:'video/2029129/images/YDWoSvV5N2jbhLocflS2Re679cOwrd2nGCkrHXkT.jpeg',
        56:'video/6119005/images/lqgxlgys9FYYaoPN1wZVvtdX5Yyon1L7qs7y5UNz.jpeg', 57:'video/2004348/images/LKPkufOawbxnLU4W7rvuA5hulI6qfcrrC9VL6yff.jpeg',
        58:'video/2064037/images/TWFLdKetLMscu1r2AggZvtfADHER63BFxgLlq69C.jpeg', 59:'video/2077009/images/JWsKAGlGXZmGU40FVqhacdgNSLmAY1326RWwT0iP.jpeg',
        60:'video/2068005/images/32123c4f569adc22d474221774161fb060c95f6b.jpg', 61:'video/2049081/images/RnR1rQGVFYPAaImzvQb4TWrPTYsd2vK83yu63BHJ.jpeg',
        62:'video/2029096/images/gMa8UPu7mlHneaSymkUK8kxuGR5uRsP9fH6SJlL8.jpeg', 63:'video/2079014/images/TlMDcaIyXA9cLR8E8qKeeEB0XN0ysdagbRhKW4g6.jpeg',
        64:'video/3004627/images/f9sGULvKDDXpsnd5i9R1azA5WzAAD9Pw97AMMSWQ.jpeg', 65:'video/2064044/images/EXDDHFml3l4j8grDxG1RnpuqVOQ90dq9q9V0xYtt.jpeg',
        66:'video/3019094/images/teN6LhiVrbnn3AzU0qsKddVqWB2WPIH0GGXMx0qc.jpeg', 67:'video/5006021/images/GQGMOVB4zU5TGuyuvexIRq3DcpYjbfqzHhN6ms9E.jpeg',
        68:'video/2046110/images/mWVIYrEdxFgJ56lEjzHXO9ZnihsAA5353mQy1sH6.jpeg', 69:'video/2029126/images/4adqaDqA6DYygeog5Lkbcff0ikdhVb5oLDmabtbg.jpeg',
        70:'video/2007400/images/qI57eZb8qVW8mIZwiKRbKj1O90ljgOm0EmAWQLxG.jpeg', 71:'video/2059068/images/KXYNyzYI2wzoZsonH5vIjnXNZdV0njeiVTIpYMzL.jpeg',
        72:'video/2049078/images/famGpHlgLEKMNYHjmWFgfST7Bqf5Ligcdgawa5Ss.jpeg', 73:'video/3019074/images/ND398dFbHryGO6kfDSLbiV58luvEVlUr4LZYHqkA.jpeg',
        74:'video/2059067/images/f127ca6bbeb6731c8cafe65607a4de64f84fc313.jpg', 75:'video/6028012/images/LL9A0yzYNb6fCfIjK7BAVVuXjDPaaKglQhvPpMbm.jpeg',
        76:'video/2019246/images/NJtK3bQSubIeuNgVreVoDslOJNfD3DUWpmvv7v3g.jpeg', 77:'video/2068013/images/239a78e4e1fd4d8be718216dae8d0345024ea386.jpg',
        78:'video/2069041/images/tyoGF0aKVEso7sWKKIIaNkxAZ1sqI8GUsJg2W4WS.jpeg', 79:'video/2064033/images/CsB3KuplnwlZcryK12wZ53F1PAomEOx3aIedMzn4.jpeg',
        80:'video/2032196/images/1LvUl0VER2KP6L10DaoDp1P29oBMEKIPaW4q1uBH.jpeg', 81:'video/3019090/images/2ALyiUoFOirRTHkhwNbjs4VU11nvjs2nJL8T4ORe.jpeg',
        82:'video/2007395/images/FfOFVZcD5RAcuPel2c3hWy6YNhAFiVeAUaf3mMSh.jpeg', 83:'video/2007392/images/ifHYXp1n4d9qOeLNYXnX9JPvY5Ck7w3GKH1j37BI.jpeg',
        84:'video/2064026/images/1FYeggnqyeD6YuvjhOg9vDq0PsIazcJEJWBXNobe.jpeg', 85:'video/2049073/images/xWeutxOXmXYbaPTCj9A7lSEEqQCu47VpyuUxxZ7e.jpeg',
        86:'video/2059057/images/bfdc4c4facd1529b3af6a201c6f2296f16e3bc25.jpg', 87:'video/2068012/images/35cae975434fa2665422df87e0be145031c05de6.jpg',
        88:'video/2029082/images/5dd7424f8379756e4a8451c3bc7afb024738c107.jpg', 89:'video/3019047/images/197d33a607e9d3a5d2496f33a8d4ba258f2cfcac.jpg',
        90:'video/2032192/images/vYc2DH6YojWdHFRpeBtBmGs7Ju0futMz2q2VwZs9.jpeg', 91:'video/2059022/images/c1e92ccc362ac6bd2e7ae83a124f302c246aed54.jpg',
        92:'video/2049067/images/4NvPbRuPgfF5hUF20h9B5JBqbc1XGH6d4IvVS7P6.jpeg', 93:'video/3004602/images/4btVByLuOUkVUG1oH7H4Fo1z3KRm4GAvUkiVgWeH.jpeg',
        94:'video/2049072/images/I6enwJ36WjnMWFYCiytaeyGaY896iC1PawnMxRTA.jpeg', 95:'video/2032188/images/uoMw0pOirBZ9zCDobxVcZg7grp8Vfeam7atLyCyl.jpeg',
        96:'video/2049070/images/WgQ6hvh8JdEN4qCmQZgDMjTFcZa2mUkbUND3n6kt.jpeg', 97:'video/2053152/images/uhoKqmORsWlrNb55Zl4mD7kawbAREl1AimIusNlP.jpeg',
        98:'video/2059078/images/HchRYMxthJoLr6ffPzB5cUARoSSmK7ql0OCLNziv.jpeg', 99:'video/2069031/images/636be35e59212946c5347c767b15a35d66376c53.jpg',
        100:'video/2066022/images/byk6FKVsUQTednDtfFCbgIDA77RSnfbrIAmBbRMN.jpeg', 101:'video/2007332/images/508a921cdbf4f6db1bb99830dd82f5aacd9dda73.jpg',
        102:'video/2058493/images/py3WqcNHgyxLxSPJdXGbUnRhLUOh0qShTjlZJnAu.jpeg', 103:'video/2064013/images/c79dab82b8c5e1f41761e016e9293add4b15577d.jpg',
        104:'video/2064007/images/9e8737acfa9c31fd1dbcb233169fc954d46bcf54.jpg', 105:'video/2029122/images/Jr4nJXlNYNQP4uYqyFneQRP57AhXT65143YKwrKz.jpeg',
        106:'video/6024002/images/lFG6zaUl4S02uBrj1f2LDNlbSACmS0LfcArn0dYz.jpeg', 107:'video/6024001/images/ITMzW2Gy6tEPDImwqUISTBojEp7GQUqqeIoMm858.jpeg',
        108:'video/2029118/images/pU2ZuIUfJRMmlNk0gfzdG469zMjUtLaNfF9rIUeO.jpeg', 109:'video/2007318/images/123e3cae17b12efe83e4b38daec8547f08599235.jpg',
        110:'video/3004536/images/0fda24c5880fed5dbdc4e7426c749e87651bd0ec.jpg', 111:'video/2007346/images/701d1b40d4f1b7c0289d1a522894afc8813f4bff.jpg',
        112:'video/2007326/images/12a25a21f641af5f113b7f54f749be2fb4b346d9.jpg', 113:'special/fukushima/images/A0x2Rq7Ojwqs1t3FfrBL2VFSLrv7g3MtZjGiQP0e.jpeg',
        114:'special/fukushima/images/ywoBGITSx4BaZ6188SIk4lOspfdv1OBaRC6fUjSx.jpeg', 115:'special/nagano/images/EU6h6X8Fo8xrJ9QDNcLNlVIv9M6AeVrAJiK2DXk4.jpeg',
        116:'special/mie/images/olQ5Hvn5hD4cAtgIbu3zoGIPTpp2soPgHI8INb5j.jpeg', 117:'special/wakayama/images/JmKwKWVFYPJy4mXSKcYMnAwoutcpBDfo5wEQ7iwO.jpeg',
        118:'special/nara/images/AxLkpaG1qvqeVRrq4XXegascly15Ro3zOv2TbSak.jpeg', 119:'special/nara/images/UhBehrFRqUPtQYeO5V3ZIYS0wyHvHwFNjfOnPJoz.jpeg',
        120:'special/tokushima/images/wBuFKSZepjzTKAYbK4iTa9CVRvnPELSCmNclZgfY.jpeg', 121:'video/9999047/images/wRqD9soSv5Y6qLWlWQz8PArEZEdwlCPfZ70N1QG0.jpeg',
        122:'video/5001288/images/3fcYxSufUgJO1WLnY4i1wpGQqUUbTRK41pvFFgFB.jpeg', 123:'video/2088002/images/6ChBBGG155obtxNbtER3yWzCZm4Vm4Nxd9Z8TVfS.jpeg',
        124:'video/9999531/images/vOLpDIarmpojU3y19WN6SsugpsGAqCwnltD42VBF.jpeg', 125:'video/9999418/images/JVLcrYw8swn65XEDuyaHBNxlaobLWoh4YtlYKmiO.jpeg',
        126:'video/9999191/images/c1HyNwXrF5dG0x0E1G7UPvMTjioaHzekHt2sCGUg.jpeg', 127:'video/9999147/images/8gdGgpy5DrQh2kj8NlkOVwPmC6cBTeb4O0etaYr4.jpeg',
        128:'video/9999131/images/Bpo4ViEOlwZ15faYJTo51KQcThgfInyr8rSTQnIu.jpeg', 129:'video/9999116/images/mXeye2lD9XIGULOuST1HAlH06U2UtuY9RN7jprsc.jpeg',
        130:'video/9999083/images/6MYzRXETwdnpdxwS4VnAI56OAYir4KDlTDCk1Nfh.jpeg', 131:'video/9999061/images/Y3RWptbrnVyFXIZJTWzWncPp7elOU8vrj3vfXgiq.jpeg',
        132:'video/9999074/images/gR2x5A8J3ra1NsytdCemK59Kd8Mfzeg3k181MqOJ.jpeg'}

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

sch = 'https://api.nhk.or.jp/nhkworld/epg/v7a/world/s'+str(int(start_time))+'-e'+str(int(end_time))+'.json?%s' % apikey
now = 'https://api.nhk.or.jp/nhkworld/epg/v7a/world/now.json?%s' % apikey


# Main Menu
def CATEGORIES():
    addDir('NHK World Live Schedule', '', 'schedule', nhk_icon)
    addDir('NHK World Live Stream', '', 'live_strm', nhk_icon)
    addDir('NHK World Chinese Language Stream', '', 'other_live_strm', nhk_icon)
    addDir('NHK World On Demand', '', 'vod_cats', nhk_icon)
    addDir('JIBTV On Demand', 'https://www.jibtv.com/programs/', 'jibtv', jib_icon)
    addDir('NHK World News', '', 'news', nhk_icon)
    addDir('NHK Radio News', '', 'audio', nhk_icon)
    addDir('NHK Videos on Youtube', '', 'youtube1', nhk_icon)

# Create content list
def addDir(name,url,mode,iconimage):
    params = {'url':url, 'mode':mode, 'name':name}
    addon.add_directory(params, {'title': str(name)}, img = iconimage, fanart = 'https://www3.nhk.or.jp/nhkworld/en/ondemand/'+img[z])
    #addon.add_directory(params, {'title': str(name)}, img = iconimage, fanart = 'https://www.jnto.go.jp/eng/wallpaper/'+str_Yr+'/img/type-a/1920-1080/'+month[Mth]+'.jpg')

def addDir1(name,url,mode,iconimage):
    params = {'url':url, 'mode':mode, 'name':name, 'iconimage':iconimage}
    addon.add_directory(params, {'title': str(name)}, img = iconimage, fanart = iconimage)

def addDir2(name,url,mode,plot,iconimage):
    params = {'url':url, 'mode':mode, 'name':name, 'plot':plot, 'iconimage':iconimage}
    addon.add_directory(params, {'title': str(name), 'plot': plot}, img = iconimage, fanart = iconimage)

def addLink(name,url,plot,img,fanart):
    addon.add_item({'url': fanart}, {'title': name, 'plot': plot}, img = img, fanart = fanart, resolved=False, total_items=0, playlist=False, item_type='video', 
                 is_folder=False)

def addDirYT(title, url):
    liz=xbmcgui.ListItem(title)
    liz.setProperty('IsPlayable', 'false')
    liz.setInfo(type="Video", infoLabels={"label":title,"title":title} )
    liz.setArt({'thumb':nhk_icon,'fanart':'https://www3.nhk.or.jp/nhkworld/en/ondemand/'+img[z]})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)

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
        media_item_list(name.encode('UTF-8') + ' - 720', 'https://nhkwlive-ojp.akamaized.net/hls/live/2003459/nhkwlive-ojp/index_2M.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
        media_item_list(name.encode('UTF-8') + ' - 1080', 'https://nhkwlive-ojp.akamaized.net/hls/live/2003459/nhkwlive-ojp/index_4M.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
    else:
        media_item_list(name.encode('UTF-8') + ' - 720', 'https://nhkwlive-xjp.akamaized.net/hls/live/2003458/nhkwlive-xjp/index_2M.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
        media_item_list(name.encode('UTF-8') + ' - 1080', 'https://nhkwlive-ojp.akamaized.net/hls/live/2003459/nhkwlive-ojp/index_4M.m3u8', desc.encode('UTF-8'), thumbnl, thumbnl)
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

def IDX_OTHER_LIVE_STRM():
    fanart = 'https://www3.nhk.or.jp/nhkworld/en/ondemand/'+img[z]
    media_item_list('NHK Live - Chinese', 'https://nhkw-zh-hlscomp.akamaized.net/8thz5iufork8wjip/playlist.m3u8', '', nhk_icon, fanart)

def IDX_VOD_CATS(url):
    addDir('On Demand Full Listing', host8+'all/all/en/all/all.json?%s' % apikey, 'vod', nhk_icon)
    addDir('Latest Episodes', host8+'all/all/en/all/12.json?%s' % apikey, 'vod', nhk_icon)
    addDir('Most Watched', host8+'mostwatch/all/en/all/12.json?%s' % apikey, 'vod', nhk_icon)
    addDir('Playlists', host14+'en/all.json?%s' % apikey, 'p_lists', nhk_icon)
    addDir('Video Clips', host12+'all/all/en/all/all.json?%s' % apikey, 'vod', nhk_icon)
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
    addDir('NHK World News', '', 'news', host9+'11.png')
    #addDir('News', host8+'category/11/en/all/all.json?%s' % apikey, 'vod', host9+'11.png')
    addDir('Pop Culture & Fashion', host8+'category/22/en/all/all.json?%s' % apikey, 'vod', host9+'22.png')
    addDir('Science & Nature', host8+'category/23/en/all/all.json?%s' % apikey, 'vod', host9+'23.png')
    addDir('Sport', host8+'category/25/en/all/all.json?%s' % apikey, 'vod', host9+'25.png')
    addDir('Travel', host8+'category/18/en/all/all.json?%s' % apikey, 'vod', host9+'18.png')

# video on demand
def IDX_VOD(url,mode):
    req = urllib2.urlopen(url)
    vod_json = json.load(req)
    try:
        for i in range(5000):
            series_ = vod_json['data']['episodes'][i]['title']
            ep_name_ = vod_json['data']['episodes'][i]['sub_title']
            plot_ = vod_json['data']['episodes'][i]['description']
            thumbnl_ = vod_json['data']['episodes'][i]['image_l']
            vid_id = vod_json['data']['episodes'][i]['vod_id']
            series = (series_).encode('UTF-8').replace('[\'','').replace('\']','').replace('<br />',' ').replace('<span style="font-style: italic;">', '').replace('</span>','')
            ep_name = (ep_name_).encode('UTF-8').replace('<br>',' ').replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('\\xd7','x').replace('\\xc3\\x97','x').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','').replace('<b>','').replace('</b>','')
            plot = (plot_).encode('UTF-8').replace('<br>',' ').replace('&#9825;',' ').replace('[\'','').replace('\']','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('<em>','').replace('</em>','').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','').replace('<b>','').replace('</b>','')#.replace('["','').replace('"]','')
            thumbnl = host2[:-1]+thumbnl_
            if series == '':
                addDir2(ep_name, vid_id, 'vod_resolve', plot, thumbnl)
            elif ep_name == '':
                addDir2(series, vid_id, 'vod_resolve', plot, thumbnl)
            else:
                addDir2(series + ' - ' + ep_name, vid_id, 'vod_resolve', plot, thumbnl)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

def VOD_RESOLVE(name,url,plot,iconimage):
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
        try:
            v1 = vod_json['response']['WsProgramResponse']['program']['asset']['assetFiles'][0]['rtmp']['play_path']
            vlink_1 = v1.split('?')
            vlink1 = 'https://nhkw-mzvod.akamaized.net/www60/mz-nhk10/definst/' + vlink_1[0] + '/chunklist.m3u8'
            media_item_list('720: '+ name, vlink1, plot, iconimage, iconimage)
        except:
            pass
        try:
            v2 = vod_json['response']['WsProgramResponse']['program']['asset']['referenceFile']['rtmp']['play_path']
            vlink_2 = v2.split('?')
            vlink2 = 'https://nhkw-mzvod.akamaized.net/www60/mz-nhk10/definst/' + vlink_2[0] + '/chunklist.m3u8'
            media_item_list('1080: '+ name, vlink2, plot, iconimage, iconimage)
        except:
            pass
        xbmcplugin.setContent(pluginhandle, 'episodes')

#playlists
def IDX_P_LISTS(url):
    req = urllib2.urlopen(url)
    plists_json = json.load(req)
    try:
        for i in range(100):
            p_list_id_ = plists_json['data']['playlist'][i]['playlist_id']
            series_ = plists_json['data']['playlist'][i]['title']
            thumbnl_ = plists_json['data']['playlist'][i]['image_original']
            c_type = plists_json['data']['playlist'][i]['content_type']
            p_list_id = host14+'en/'+p_list_id_+'.json?%s' % apikey
            series = (series_).encode('UTF-8').replace('[\'','').replace('\']','').replace('<br />',' ').replace('\\xd7','x').replace('\\xc3\\x97','x').replace('\\xc3','').replace('<span style="font-style: italic;">', '').replace('</span>','')
            thumbnl = host2[:-1]+thumbnl_
            addDir2(series, p_list_id, 'p_resolve', '', thumbnl)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

def P_RESOLVE(name,url,mode,plot,iconimage):
    req = urllib2.urlopen(url)
    vod_json = json.load(req)
    try:
        for i in range(100):
            series_ = vod_json['data']['playlist'][0]['track'][i]['title_clean']
            ep_name_ = vod_json['data']['playlist'][0]['track'][i]['sub_title_clean']
            plot_ = vod_json['data']['playlist'][0]['track'][i]['description_clean']
            thumbnl_ = vod_json['data']['playlist'][0]['track'][i]['image_l']
            vid_id = vod_json['data']['playlist'][0]['track'][i]['vod_id']
            series = (series_).encode('UTF-8').replace('[\'','').replace('\']','').replace('<br />',' ').replace('\\xd7','x').replace('\\xc3\\x97','x').replace('\\xc3','').replace('<span style="font-style: italic;">', '').replace('</span>','').replace('\\xc3\\xa9','e')
            ep_name = (ep_name_).encode('UTF-8').replace('<br>',' ').replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('\\xd7','x').replace('\\xc3\\x97','x').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','').replace('<b>','').replace('</b>','')
            plot = (plot_).encode('UTF-8').replace('<br>',' ').replace('&#9825;',' ').replace('[\'','').replace('\']','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('<em>','').replace('</em>','').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','').replace('<b>','').replace('</b>','')#.replace('["','').replace('"]','')
            thumbnl = host2[:-1]+thumbnl_
            s_dict[i]=series; e_dict[i]=ep_name; v_dict[i]=vid_id; p_dict[i]=plot; t_dict[i]=thumbnl
            req1_dict[i] = 'https://movie-s.nhk.or.jp/v/refid/nhkworld/prefid/'+v_dict[i]+'?embed=js&targetId=videoplayer&de-responsive=true&de-callback-method=nwCustomCallback&de-appid='+v_dict[i]+'&de-subtitle-on=false'
            req1 = urllib2.Request(req1_dict[i], headers=hdr)
            response = urllib2.urlopen(req1)
            link=response.read()
            response.close()
            link_dict[i]=link
            if s_dict[i] == '':
                addDir2(e_dict[i],req1_dict[i],'p_resolve2',p_dict[i],t_dict[i])
            elif e_dict[i] == '':
                addDir2(s_dict[i],req1_dict[i],'p_resolve2',p_dict[i],t_dict[i])
            else:
                addDir2(s_dict[i]+' - '+e_dict[i],req1_dict[i],'p_resolve2',p_dict[i],t_dict[i])
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

def P_RESOLVE2(name,url,mode,plot,iconimage):
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match = re.compile("'data-de-program-uuid','(.+?)'").findall(link)
    for p_uuid_ in match:
        p_uuid = str(p_uuid_).replace("['" , "").replace("']" , "")
        req = urllib2.urlopen('https://movie-s.nhk.or.jp/ws/ws_program/api/67f5b750-b419-11e9-8a16-0e45e8988f42/apiv/5/mode/json?v='+p_uuid)
        vod_json = json.load(req)
        try:
            v1 = vod_json['response']['WsProgramResponse']['program']['asset']['assetFiles'][0]['rtmp']['play_path']
            vlink_1 = v1.split('?')
            vlink1 = 'https://nhkw-mzvod.akamaized.net/www60/mz-nhk10/definst/' + vlink_1[0] + '/chunklist.m3u8'
            media_item_list('720: '+ name, vlink1, plot, iconimage, iconimage)
        except:
            pass
        try:
            v2 = vod_json['response']['WsProgramResponse']['program']['asset']['referenceFile']['rtmp']['play_path']
            vlink_2 = v2.split('?')
            vlink2 = 'https://nhkw-mzvod.akamaized.net/www60/mz-nhk10/definst/' + vlink_2[0] + '/chunklist.m3u8'
            media_item_list('1080: '+ name, vlink2, plot, iconimage, iconimage)
        except:
            pass
    xbmcplugin.setContent(pluginhandle, 'episodes')


# jibtv
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
    addDir('News At a Glance', host2+'nhkworld/en/news/ataglance/index.json', 'glance', nhk_icon)
    addDir('News Videos', host10+'list/en/newsvideos/all/all.json?%s' % apikey, 'topnews', nhk_icon)
    try:
        media_item_list('Newsline', host2+'nhkworld/data/en/news/programs/1001.xml','',host11+'1001.jpg',host11+'1001.jpg')
    except:
        pass
    try:
        media_item_list('Newsroom Tokyo', host2+'nhkworld/data/en/news/programs/1002.xml','',host11+'1002.jpg',host11+'1002.jpg')
    except:
        pass
    try:
        media_item_list('Newsline Asia 24', host2+'nhkworld/data/en/news/programs/1003.xml','',host11+'1003.jpg',host11+'1003.jpg')
    except:
        pass
    try:
        media_item_list('Newsline Biz', host2+'nhkworld/data/en/news/programs/1004.xml','',host11+'1004.jpg',host11+'1004.jpg')
    except:
        pass
    try:
        media_item_list('Newsline In Depth', host2+'nhkworld/data/en/news/programs/1005.xml','',host11+'1005.jpg',host11+'1005.jpg')
    except:
        pass
    try:
        media_item_list('Biz Stream', host2+'nhkworld/data/en/news/programs/2074.xml','',host11+'2074_2.jpg',host11+'2074_2.jpg')
    except:
        pass
'''
def THE_NEWS(url):
    req = urllib2.Request(url, headers=hdr)
    file = urllib2.urlopen(req)
    data = file.read()
    file.close()
    dom = parseString(data)
    v_url = dom.getElementsByTagName('file.high')[0].toxml()
    image = dom.getElementsByTagName('image')[0].toxml()
    name = dom.getElementsByTagName('media.title')[0].toxml()
    vid_url = v_url.replace('<file.high><![CDATA[','').replace(']]></file.high>','').replace('rtmp://flv.nhk.or.jp/ondemand/flv','https://nhkworld-vh.akamaihd.net/i').replace('hq.mp4',',l,h,q.mp4.csmil/master.m3u8')
    thumbnl = host2 + image.replace('<image><![CDATA[/','').replace(']]></image>','')
    name_ = name.replace('<media.title>','').replace('</media.title>','').replace("_#039_","'").replace('_quot_','"')
    media_item_list(name_,vid_url,'',thumbnl,thumbnl)
'''
# Latest top news stories
def IDX_TOPNEWS(url):
    req = urllib2.Request(url, headers=hdr)
    file = urllib2.urlopen(req)
    top_json = json.load(file)
    try:
        for i in range(500):
            if top_json['data'][i]['videos']:
                ep_name_ = top_json['data'][i]['title']
                plot_ = top_json['data'][i]['description']
                thumbnl_ = top_json['data'][i]['thumbnails']['middle']
                xml_link = top_json['data'][i]['videos']['config']
                ep_name = (ep_name_).encode('UTF-8').replace('<br>',' ').replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('\\xd7','x').replace('\\xc3\\x97','x').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','')
                plot = (plot_).encode('UTF-8').replace('<br>',' ').replace('&#9825;',' ').replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('<em>','').replace('</em>','').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','')
                thumbnl = host2[:-1]+thumbnl_
                addDir2(ep_name, xml_link, 'tn_resolve', plot, thumbnl)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

# News at a glance
def IDX_GLANCE(url):
    req = urllib2.Request(url, headers=hdr)
    file = urllib2.urlopen(req)
    g_json = json.load(file)
    try:
        for i in range(5000):
            if g_json['data'][i]['video']:
                ep_name_ = g_json['data'][i]['title']
                plot_ = g_json['data'][i]['description']
                thumbnl_ = g_json['data'][i]['image']['main_pc']
                xml_link = g_json['data'][i]['video']['config']
                ep_name = (ep_name_).encode('UTF-8').replace('<br>',' ').replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('\\xd7','x').replace('\\xc3\\x97','x').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','')
                plot = (plot_).encode('UTF-8').replace('<br>',' ').replace('&#9825;',' ').replace('[\'','').replace('\']','').replace('["','').replace('"]','').replace("\\\'","'").replace('<br />',' ').replace('&amp;','&').replace('<span style="font-style: italic;">','').replace('</span>','').replace('\\xe0','a').replace('\\xc3\\x89','E').replace('\\xe9','e').replace('\\xef\\xbd\\x9e',' ~ ').replace('<em>','').replace('</em>','').replace('\\xc3','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','')
                thumbnl = host2[:-1]+thumbnl_
                addDir2(ep_name, xml_link, 'g_resolve', plot, thumbnl)
    except:
        pass
    xbmcplugin.setContent(pluginhandle, 'episodes')

def RESOLVE(name,url,mode,plot,iconimage):
    req = urllib2.Request((host2[:-1]+url), headers=hdr)
    file = urllib2.urlopen(req)
    data = file.read()
    file.close()
    dom = parseString(data)
    v_url = dom.getElementsByTagName('file.high')[0].toxml()
    if mode == 'tn_resolve':
        vid_url = v_url.replace('<file.high><![CDATA[','').replace(']]></file.high>','').replace('rtmp://flv.nhk.or.jp/ondemand/flv','https://nhkworld-vh.akamaihd.net/i').replace('HQ.mp4',',L,H,Q.mp4.csmil/master.m3u8')
    else:
        vid_url = v_url.replace('<file.high>','').replace('</file.high>','').replace('rtmp://flv.nhk.or.jp/ondemand/flv','https://nhkworld-vh.akamaihd.net/i').replace('mp4','mp4/master.m3u8')
    media_item_list(name,vid_url,plot,iconimage,iconimage)
    xbmcplugin.setContent(pluginhandle, 'episodes')

# Pre-recorded NHK World Radio in 17 languages
def IDX_RADIO(url):
    fanart = 'https://www3.nhk.or.jp/nhkworld/en/ondemand/'+img[z]
    for i in range(17):
        media_item_list('NHK Radio News in '+lang[i], host13+lang_key[i]+'/news.json?%s' % apikey,'','',fanart)

def IDX_YOUTUBE1():
    addDirYT(title="NHK World Channel",
        url="plugin://plugin.video.youtube/user/NHKWorld/")
               
    addDirYT(title="Youtube Search for 'NHK World'",
        url='plugin://plugin.video.youtube/search/?q=NHK World')

    addDirYT(title="NHK Videos - Select Playlists in next menu",
               url="plugin://plugin.video.youtube/channel/UCMsBttS0NCgp7HXuAeN22QQ/")
               
    addDirYT(title="NHK Online",
        url='plugin://plugin.video.youtube/user/NHKonline/')
               
    addDirYT(title="UNESCO/NHK",
        url="plugin://plugin.video.youtube/playlist/PLWuYED1WVJIPKU_tUlzLTfkbNnAtkDOhS/")
               
    addDirYT(title="Core Kyoto",
        url="plugin://plugin.video.youtube/search/?q='Core Kyoto'+NHK")

    addDirYT(title="Cycle Around Japan",
        url="plugin://plugin.video.youtube/search/?q='Cycle Around Japan'+NHK")

    addDirYT(title="Japan Railway Journal",
        url="plugin://plugin.video.youtube/search/?q=NHK Japan Railway Journal")
               
    addDirYT(title="J-Trip Plan",
        url="plugin://plugin.video.youtube/search/?q=NHK J-Trip Plan")

    addDirYT(title="NHK Documentary",
        url='plugin://plugin.video.youtube/search/?q=NHK Documentary')
               
    addDirYT(title="Japan's Top Inventions",
        url='plugin://plugin.video.youtube/search/?q=intitle:"Japan\'s Top Inventions"')
               
    addDirYT(title="Japanology",
        url='plugin://plugin.video.youtube/search/?q=intitle:"Japanology"')

    addDirYT(title="Begin Japanology",
        url="plugin://plugin.video.youtube/search/?q=Begin Japanology")
               
    addDirYT(title="Japanology Plus",
        url="plugin://plugin.video.youtube/search/?q=Japanology Plus")

    addDirYT(title="Seasoning the Seasons",
        url='plugin://plugin.video.youtube/search/?q=intitle:"Seasoning the Seasons"')
   
    addDirYT(title="Tokyo Eye",
        url="plugin://plugin.video.youtube/search/?q=Tokyo Eye")
               
    addDirYT(title="Trails to Tsukiji",
        url="plugin://plugin.video.youtube/search/?q=Trails to Tsukiji")
               
    addDirYT(title="Trails to Oishii Tokyo",
        url="plugin://plugin.video.youtube/search/?q=Trails to Oishii Tokyo")
               
    addDirYT(title="Dining with the Chef",
        url="plugin://plugin.video.youtube/search/?q=Dining with the chef")
           
    addDirYT(title="Journeys in Japan",
        url='plugin://plugin.video.youtube/search/?q=intitle:"journeys in japan"')

    addDirYT(title="Train Cruise",
        url="plugin://plugin.video.youtube/search/?q='Train Cruise'+NHK")
               
    addDirYT(title="Cool Japan",
        url='plugin://plugin.video.youtube/search/?q=intitle:"cool japan"')
               
    addDirYT(title="At Home with Venetia in Kyoto",
        url="plugin://plugin.video.youtube/search/?q=At Home with Venetia in Kyoto")
               
    addDirYT(title="Japan from Above",
        url='plugin://plugin.video.youtube/search/?q=Japan from above')
               
    addDirYT(title="Blends",
        url="plugin://plugin.video.youtube/search/?q=NHK Blends")

    addDirYT(title="Somewhere Street",
        url="plugin://plugin.video.youtube/search/?q=NHK Somewhere Street")

    addDirYT(title="Supreme Skils",
        url="plugin://plugin.video.youtube/search/?q='Supreme Skills'+NHK")
        
    addDirYT(title="NHK Documentary - Silk Road",
        url="plugin://plugin.video.youtube/playlist/PLB8KCZnnrFKmP6CPynDrFVheEt9VOBPk4/")
               
    addDirYT(title="NHK Documentary - Silk Road II",
        url="plugin://plugin.video.youtube/playlist/PLdwCuEoZ_6l7FvbsfjidxMIybBrF5jnb5/")

# Create media items list
def media_item_list(name,url,plot,img,fanart):
    if mode=='audio':
        req = urllib2.Request(url, headers=hdr)
        file = urllib2.urlopen(req)
        radio_json = json.load(file)
        a_link = radio_json['data']['audio']
        radionews_url = 'https://nhkworld-vh.akamaihd.net/i'+a_link+'/master.m3u8'
        addon.add_music_item({'url': radionews_url}, {'title': name}, context_replace = nhk_icon, fanart = fanart, playlist=False)

    elif mode=='news':
        req = urllib2.Request(url, headers=hdr)
        file = urllib2.urlopen(req)
        data = file.read()
        file.close()
        dom = parseString(data)
        v_url = dom.getElementsByTagName('file.high')[0].toxml()
        image = dom.getElementsByTagName('image')[0].toxml()
        vid_url = v_url.replace('<file.high><![CDATA[','').replace(']]></file.high>','').replace('rtmp://flv.nhk.or.jp/ondemand/flv','https://nhkworld-vh.akamaihd.net/i').replace('hq.mp4',',l,h,q.mp4.csmil/master.m3u8')
        thumbnl = host2 + image.replace('<image><![CDATA[/','').replace(']]></image>','')
        addon.add_video_item({'url': vid_url}, {'title': name, 'plot': plot}, img = thumbnl, fanart = thumbnl, playlist=False)

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

elif mode=='other_live_strm':
    print ""+url
    IDX_OTHER_LIVE_STRM()

elif mode=='p_lists':
    print ""+url
    IDX_P_LISTS(url)

elif mode=='p_resolve':
    print ""+url
    P_RESOLVE(name,url,mode,plot,iconimage)

elif mode=='p_resolve2':
    print ""+url
    P_RESOLVE2(name,url,mode,plot,iconimage)

elif mode=='vod':
    print ""+url
    IDX_VOD(url,mode)

elif mode=='vod_cats':
    print ""+url
    IDX_VOD_CATS(url)

elif mode=='vod_resolve':
    print ""+url
    VOD_RESOLVE(name,url,plot,iconimage)

elif mode=='jibtv':
    print ""+url
    IDX_JIBTV(url)

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

elif mode=='tn_resolve':
    print ""+url
    RESOLVE(name,url,mode,plot,iconimage)

elif mode=='glance':
    print ""+url
    IDX_GLANCE(url)

elif mode=='g_resolve':
    print ""+url
    RESOLVE(name,url,mode,plot,iconimage)

elif mode=='audio':
    print ""+url
    IDX_RADIO(url)

if not play:
    addon.end_of_directory()