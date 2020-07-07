###################################################################################
# Little kodi script to execute TVComigo in Chrome Browser
# The script also runs WifiMouseServer.exe to control TVComigo from a mobile phone
###################################################################################

import os
import sys
import subprocess
import xbmc
import xbmcaddon

###################################################################################

def translatePath(path):
	return xbmc.translatePath(path) if sys.version_info[0]>=3 else xbmc.translatePath(path).decode('utf-8')

def getAddonFolder(key):
	return translatePath( xbmcaddon.Addon().getAddonInfo(key) )

###################################################################################

xbmc.Player().stop()

subprocess.Popen(['wscript', os.path.join(getAddonFolder('path'),'runtv.vbs')],close_fds=True, creationflags=0x00000208)
