################################################################################
# Download and process tv channel playlists m3u8 file from:
#   https://github.com/LaQuay/TDTChannels
# Creates a new channels.m3u8 playlist and configure PVR IPTV Simple Client Addon 
# to use the new playlist
################################################################################

import os
import time
import xbmc
import xbmcgui
import xbmcaddon
import tools
import filter

def translatePath(path): return xbmc.translatePath(path) if sys.version_info[0]>=3 else xbmc.translatePath(path).decode('utf-8')

addon           = xbmcaddon.Addon()
addonName       = addon.getAddonInfo('name')
addonVersion    = addon.getAddonInfo('version')
addonFolder     = translatePath( addon.getAddonInfo('path') )
profileFolder   = translatePath( addon.getAddonInfo('profile') )
chanFileInput   = profileFolder+'channels_downloaded.m3u8'
chanFileOutput  = profileFolder+'channels.m3u8'
lastVersionFile = profileFolder+'version.txt'
addonNewVersion = addonVersion!=tools.load_file(lastVersionFile)

################################################################################

# init some stuff
if addonNewVersion: tools.save_file(lastVersionFile, addonVersion)
if not os.path.exists(profileFolder): os.makedirs(profileFolder)

# progress dialog
progress = xbmcgui.DialogProgress()

# download channels m3u8 file
progress.create(addonName,"Buscando canales actualizados en internet", '', 'Por favor espere')
time.sleep(1)
if not tools.download_channels(chanFileInput) and not addonNewVersion:
	progress.close()
	xbmcgui.Dialog().ok(addonName, "No hay canales nuevos que actualizar.")
	exit()

# execute filter
progress.update(50,"Actualizando canales de TV y Radio")
filter.run( chanFileInput, chanFileOutput, True )
time.sleep(1)

# update pvr addon settings
progress.update(100,"Configurando nuevos canales en PVR IPTV Simple addon")
time.sleep(1)
progress.close()
pvraddon = xbmcaddon.Addon('pvr.iptvsimple')
if pvraddon:
	update = True
	if pvraddon.getSetting("m3uPathType")!="0":        update = pvraddon.setSetting("m3uPathType","0")
	if pvraddon.getSetting("m3uPath")!=chanFileOutput: update = pvraddon.setSetting("m3uPath", chanFileOutput)
	if update:                                  	   pvraddon.setSetting("m3uPathType","0")