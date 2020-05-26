#################################################
# config
#################################################

CHANURL = "http://www.tdtchannels.com/lists/combo_channels.m3u8"

EPGURL  = "https://www.tdtchannels.com/epg/TV.xml"

#################################################
# misc functions
#################################################

import os
import sys

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
	