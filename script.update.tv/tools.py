#################################################
# config
#################################################

CHANURL = "http://www.tdtchannels.com/lists/combo_channels.m3u8"

FILURL  = "https://raw.githubusercontent.com/michaelnpsp/kodiaddons/master/script.update.tv/filter.py"

EPGURL  = "https://www.tdtchannels.com/epg/TV.xml"

KODICMD = "c:\kodi\kodi.exe -p"

#################################################
# misc functions
#################################################

import os
import sys
import platform
import importlib
import subprocess
try: # in standalone mode there are no xbmc modules
	import xbmc
	import xbmcaddon
except:	pass

def translatePath(path):
	return xbmc.translatePath(path) if sys.version_info[0]>=3 else xbmc.translatePath(path).decode('utf-8')

def getAddonFolder(key):
	return translatePath( xbmcaddon.Addon().getAddonInfo(key) )

def load_module(name):
	if name in sys.modules:
		return importlib.reload(sys.modules[name]) if sys.version_info[0]>=3 else reload(sys.modules[name])
	else:
		return importlib.import_module(name)

def load_file(filename):
	if not os.path.exists(filename): return None
	f = open(filename, "rb")
	d = f.read()
	f.close()
	return d

def save_file(filename, content):
	f = open(filename, "wb")
	f.write(content)
	f.close()

def download_url(url, dstfile=None):
	if sys.version_info[0]<3:
		from urllib2 import urlopen
	else:
		from urllib.request import urlopen
	data = urlopen(url).read()
	if dstfile:
		if data == load_file(dstfile): return None
		save_file(dstfile,data)
	return data

def download_channels(dstfile):
	return download_url(CHANURL, dstfile)

def download_filter(dstfile):
	return download_url(FILURL, dstfile)

def restart_kodi(cmd=None):
	if platform.system() == 'Windows':
		subprocess.Popen(['cscript', os.path.join(getAddonFolder('path'),'waitexec.vbs'), cmd or KODICMD],close_fds=True, creationflags=0x00000208)
		xbmc.executebuiltin('XBMC.Quit()')
	else:
		xbmc.executebuiltin('XBMC.RestartApp()')
