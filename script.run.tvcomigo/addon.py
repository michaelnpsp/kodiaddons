###################################################################################
# Little kodi script to execute TVComigo in Chrome Browser
# The script also runs WifiMouseServer.exe to control TVComigo from a mobile phone
###################################################################################

import os
import sys
import subprocess

try:
	import xbmc
	xbmc.Player().stop()
except: pass

###################################################################################

def find_file(*args):
    for file in args:
		if os.path.exists(file): return file

###################################################################################

MUNDOR_URL     = "http://ott.mundo-r.com/nmp_app.html"

CHROME_BROWSER = find_file( 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe' )

CHROME_COMMAND = '"%s" --start-maximized --disable-translate --disable-new-tab-first-run --no-default-browser-check --no-first-run --kiosk "%s"'

MOUSE_SERVER   = find_file( 'C:\\WifiMouseServer\\WifiMouseServer.exe', 'C:\\Program Files (x86)\\WifiMouseServer.exe' )

###################################################################################

if CHROME_BROWSER==None: sys.exit()

# Start WifiMouseServer
if MOUSE_SERVER: subprocess.Popen( MOUSE_SERVER )

# Execute TVComigo in Chrome
subprocess.call( CHROME_COMMAND % (CHROME_BROWSER,MUNDOR_URL) )

# Kill WifiMouseServer
if MOUSE_SERVER: os.system("taskkill /im WifiMouseServer.exe")
