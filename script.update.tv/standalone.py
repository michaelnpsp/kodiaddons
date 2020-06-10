################################################################################
# Download and process tv channel playlists m3u8 file from:
#   https://github.com/LaQuay/TDTChannels
# Remove duplicates, creating two new playlists:
#   television-hd.m3u8 (HD channels playlist)
#   television-sd.m3u8 (SD channels playlist)
################################################################################

import os
import sys
import tools

########################################################

profileFolder = sys.argv[1] if len(sys.argv)>1 else os.path.join( os.path.expanduser("~"), "Television" )
m3uFile   = os.path.join( profileFolder, 'channels.m3u8' )
m3uFileHD = os.path.join( profileFolder, 'television-hd.m3u8' )
m3uFileSD = os.path.join( profileFolder, 'television-sd.m3u8' )

addonFolder = os.path.dirname(os.path.abspath(__file__))
filterFile = os.path.join( addonFolder, 'filter_.py' )

#######################################################

if not os.path.exists(profileFolder): os.makedirs(profileFolder)

newdata = tools.download_channels(m3uFile)
print( newdata and "New playlist downloaded!" or "Playlist is up to date!" )

# In standalone mode always use the local filter
# newfilter = tools.download_filter(filterFile)
# print( newfilter and "New filter downloaded!" or "Filter is up to date!" )
newfilter = True

if newdata or newfilter or not os.path.exists(m3uFileHD):
	tools.load_module('filter').run( m3uFile, m3uFileHD, 'HD' )
	print( "New HD m3u8 file created: " + m3uFileHD )
if newdata or newfilter or not os.path.exists(m3uFileSD):
	tools.load_module('filter').run( m3uFile, m3uFileSD, 'SD' )
	print( "New SD m3u8 file created: " + m3uFileSD )
