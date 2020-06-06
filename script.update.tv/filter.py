################################################################################
# Process tv channel playlists m3u8 file from:
#   https://github.com/LaQuay/TDTChannels
# Remove duplicates, creating two new playlists:
#   television-hd.m3u8 (HD channels playlist)
#   television-sd.m3u8 (SD channels playlist)
################################################################################

import os
import io
import re
try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

def L2D(list): return { list[i]:i*100 for i in range(0, len(list)) }

# TV Channels to filter (remove duplicates and select HD/SD channel if possible), non whitelisted channels are saved unmodified
channels = L2D([
	"La 1",
	"La 2",
	"Antena 3",
	"Cuatro",
	"Telecinco",
	"laSexta",
	"TVG",
	"TVG 2",
	"Neox",
	"Nova",
	"Mega",
	"Atreseries",
	"FDF",
	"Energy",
	"Divinity",
	"Be Mad",
	"Paramount Network",
	"Boing",
	"Clan",
	"mtmad 24h",
	"Teledeporte",
	"24h",
])

# TV Channels to ignore because they are not working, strings are the tvg-name last text in EXTINF line
# True = channel is removed  False = Generales group channels are moved to Alternatives group
blacklist = {
  "Antena 3 GEO":   False,
  "laSexta GEO":    False,
  "Neox": 			True,
  "Nova": 			True,
  "Mega": 			True,
  "+tdp": 			True,
  "+24":  			True,
  "Nius HD":	    True,
  "Nius SD":	    True,
  "Disney Channel": True,
}

# Extra channels to include
extrachannels =u"""
#EXTINF:-1 tvg-id="Telecinco.TV" tvg-logo="https://graph.facebook.com/tele5/picture?width=200&height=200" group-title="Generalistas" tvg-name="Telecinco",Telecinco
https://linear01-i.akamaihd.net/hls/live/837810/telecinco/master.m3u8
#EXTINF:-1 tvg-id="Cuatro.TV" tvg-logo="https://graph.facebook.com/cuatro/picture?width=200&height=200" group-title="Generalistas" tvg-name="Cuatro",Cuatro
https://linear02-i.akamaihd.net/hls/live/837811/cuatro/master.m3u8
#EXTINF:-1 tvg-id="FDF.TV" tvg-logo="https://graph.facebook.com/factoriadeficcion/picture?width=200&height=200" group-title="Generalistas" tvg-name="FDF",FDF
https://linear02-i.akamaihd.net/hls/live/837813/fdf/master.m3u8
#EXTINF:-1 tvg-id="Energy.TV" tvg-logo="https://graph.facebook.com/E.EnergyTV/picture?width=200&height=200" group-title="Generalistas" tvg-name="Energy",Energy
https://linear02-i.akamaihd.net/hls/live/837816/energy/master.m3u8
#EXTINF:-1 tvg-id="Divinity.TV" tvg-logo="https://graph.facebook.com/divinityes/picture?width=200&height=200" group-title="Generalistas" tvg-name="Divinity",Divinity
https://linear01-i.akamaihd.net/hls/live/837812/divinity/master.m3u8
#EXTINF:-1 tvg-id="Bemad.TV" tvg-logo="https://graph.facebook.com/BeMadTV/picture?width=200&height=200" group-title="Generalistas" tvg-name="Be Mad",Be Mad
https://linear02-i.akamaihd.net/hls/live/837815/bemad/master.m3u8
#EXTINF:-1 tvg-id="Boing.TV" tvg-logo="https://graph.facebook.com/boinges/picture?width=200&height=200" group-title="Generalistas" tvg-name="Boing",Boing
https://linear01-i.akamaihd.net/hls/live/837814/boing/master.m3u8
""".strip()+u"\n"

# Unicode subscripts
subscripts = u"\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089*********"

################################################################################

def unpack(t,c):
	r = (t==None and tuple(None for i in range(c))) or ('group' in dir(t) and tuple(t.group(i) for i in range(1,c+1))) or t
	return c>1 and r or r[0]

def order(key, orders, base):
	orders[key] = (orders.get(key) or 0) + 1
	return base + orders[key]

def replace(group, str):
	r = re.match('.+group\-title=(".+?")', str)
	return r and re.sub(r.group(1), group, str) or str

def run(file_src, file_dst, suffix):

	orders = {}
	result = []

	with io.open(file_src,'r',encoding='utf8') as f: fr = StringIO(extrachannels+f.read())
	fw = io.open( file_dst, "w", encoding="utf8" )

	fw.write( fr.readline() )
	fw.write( fr.readline() )

	for i in range(10000, 1000000):
		inf = fr.readline()
		url = fr.readline()
		if url and url[0:11]=="#EXTVLCOPT:": url = fr.readline()
		if not (inf and url): break
		name, desc = unpack( re.match('^.+tvg\-name="(.+)",(.+)$',inf), 2 )
		if name and blacklist.get(desc)!=True:
			if channels.get(name)!=None:
				suf = unpack(re.match('.+(HD|SD|GEO)$',desc), 1) or ''
				if (suf==suffix or (suf!='HD' and suf!='SD')) and blacklist.get(desc)==None:
					inf = replace( '"Generalistas"', re.sub( ' %s$' % suf, '', inf) )
					result.append( ( order(name,orders,channels.get(name)), name, inf, url ) )
				else:
					inf = replace('"Alternativas"',inf)
					result.append( ( i, name, inf, url ) )
			else:
				result.append( ( i, name, inf, url ) )

	result.sort( key=lambda r:r[0] )

	for idx, nam, inf, url in result:
		fw.write( (orders.get(nam) or 0)>1 and re.sub('\n$','%s\n' % subscripts[idx%100], inf) or inf )
		fw.write( url )

	fr.close()
	fw.close()
