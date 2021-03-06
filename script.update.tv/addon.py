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

addon           = xbmcaddon.Addon()
addonName       = addon.getAddonInfo('name')
addonVersion    = addon.getAddonInfo('version')
profileFolder   = tools.getAddonFolder('profile')
chanFileInput   = os.path.join(profileFolder, 'channels_downloaded.m3u8')
chanFileOutput  = os.path.join(profileFolder, 'channels.m3u8')
lastVersionFile = os.path.join(profileFolder, 'version.txt')
addonNewVersion = addonVersion!=tools.load_file(lastVersionFile)
addonFolder     = tools.getAddonFolder('path')
filterFile      = os.path.join(addonFolder, 'filter_.py')

################################################################################

# init some stuff
if not os.path.exists(profileFolder): os.makedirs(profileFolder)
if addonNewVersion: tools.save_file(lastVersionFile, addonVersion)

# progress dialog
progress = xbmcgui.DialogProgress()

# download channels m3u8 file
progress.create(addonName,"Buscando canales actualizados en internet", '', 'Por favor espere')
time.sleep(1)

newChannels = tools.download_channels(chanFileInput)
newFilter   = tools.download_filter(filterFile)

if not ( newChannels or newFilter or addonNewVersion ):
	progress.close()
	xbmcgui.Dialog().ok(addonName, "No hay canales nuevos que actualizar.")
	exit()

# execute filter
progress.update(50,"Actualizando canales de TV y Radio")
tools.load_module('filter_').run( chanFileInput, chanFileOutput, "HD" )
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
	if pvraddon.getSetting("epgPathType")!="1":        update = pvraddon.setSetting("epgPathType","1")
	if pvraddon.getSetting("epgUrl")!=tools.EPGURL:    update = pvraddon.setSetting("epgUrl", tools.EPGURL)
#	if update:                                  	   pvraddon.setSetting("m3uPathType","0")
	tools.restart_kodi()
