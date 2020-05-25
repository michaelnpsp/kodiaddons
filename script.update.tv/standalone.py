################################################################################
# Download and process tv channel playlists m3u8 file from:
#   https://github.com/LaQuay/TDTChannels
# Remove duplicates, creating two new playlists:
#   television-hd.m3u8 (HD channels playlist)
#   television-sd.m3u8 (SD channels playlist)
################################################################################

URLCHANNELS = "http://www.tdtchannels.com/lists/combo_channels.m3u8"

########################################################

import os
import tools
import filter

########################################################

addonFolder   = os.path.dirname(os.path.abspath(__file__))
profileFolder = os.path.join( os.path.expanduser("~"), "Television" )

m3uFile   = os.path.join( profileFolder, 'channels.m3u8')
m3uFileHD = os.path.join( profileFolder, 'television-hd.m3u8')
m3uFileSD = os.path.join( profileFolder, 'television-sd.m3u8')

#######################################################

if not os.path.exists(profileFolder): os.makedirs(profileFolder)

newdata = tools.download_url(URLCHANNELS, m3uFile)

print( newdata and "New internet playlist downloaded!" or "Playlist already updated nothing to download!" )

if newdata or not os.path.exists(m3uFileHD): 
	filter.run( m3uFile, m3uFileHD, True )
	print( "New HD m3u8 file created: " + m3uFileHD )
if newdata or not os.path.exists(m3uFileSD): 
	filter.run( m3uFile, m3uFileSD, False )
	print( "New SD m3u8 file created: " + m3uFileSD )
