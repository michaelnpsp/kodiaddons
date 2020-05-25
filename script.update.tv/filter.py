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

def L2D(list): return { list[i]: i for i in range(0, len(list)) }

# TV Channels to filter (remove duplicates and select HD/SD channel if possible), non whitelisted channels are saved unmodified
whitelist = L2D([
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
	"Teledeporte",
	"24h",
])

# TV Channels to ignore because they are not working, strings are the tvg-name last text in EXTINF line
blacklist = L2D([
  "Neox",
  "Nova",
  "Mega",
  "Atreseries",
  "Disney Channel",
  "+tdp",
  "+24",
  "Nius HD",
  "Nius SD",
])

# custom filter priorities for some channels
filter_nogeo = { '':2, 'GEO':3 }

filters = {
	"La 1":     filter_nogeo,
	"La 2":     filter_nogeo,
	"Antena 3": filter_nogeo,
	"laSexta":  filter_nogeo,
}

################################################################################

def onematch( pat, str ):
	r = re.match(pat, str)
	return r and r.group(1) or None

def replacegroup( group, str ):
	return re.sub( onematch('.+group\-title=(".+?")',str), group, str )

def run(file_src, file_dst, quality):

	result = []
	saved  = { 'name':None }
	filter = quality and {'HD':1,'GEO':2,'':3,'SD':4} or {'SD':1,'GEO':2,'':3,'HD':4}
	
	fr = io.open(file_src,"r", encoding="utf8")
	fw = io.open(file_dst,"w", encoding="utf8")
	
	fw.write( fr.readline() )
	fw.write( fr.readline() )
	
	for i in range(1000,100000):
		inf = fr.readline()
		url = fr.readline()
		if url and url[0:11]=="#EXTVLCOPT:": url = fr.readline()
		if not (inf and url): break
		m = re.match( '^.+tvg\-name="(.+)",(.+)$', inf )
		if m:
			name, desc = m.groups()
			if not (desc in blacklist):
				if saved['name'] and name!=saved['name']:
					result.append(saved)
					saved = { 'name':None }
				if name in whitelist:
					typ = onematch('.+(HD)$',desc) or onematch('.+(SD)$',desc) or onematch('.+(GEO)$',desc) or ''
					fil = filters.get(name)
					pri = (fil and fil.get(typ)) or filter.get(typ) or 100000
					data = { 'inf':re.sub(' '+typ+'$','',inf), 'url':url, 'name':name, 'priority':pri, 'index':i, 'pinf':inf }
					if pri<(saved.get('priority') or 100000):
						data['inf']   = replacegroup( '"Generalistas"', data['inf'] )
						data['order'] = whitelist[name]
						saved, data = data, saved
					if data['name']:
						data['inf']   = replacegroup( '"Alternativas"', data['pinf'] )
						data['order'] = data['index']
						result.append(data)
				else:
					result.append( { 'inf':inf, 'url':url, 'name':name, 'order':i } )
	
	if saved['name']:
		result.append(saved)
	
	result.sort( key=lambda r:r['order'] )
	
	for item in result:
		fw.write(item['inf'])
		fw.write(item['url'])
	
	fr.close()
	fw.close()

