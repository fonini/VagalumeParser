# -*- Mode: python; coding: utf-8; tab-width: 8; indent-tabs-mode: t; -*-
#
# Copyright (C) 2010 Jonnas Fonini <contato@fonini.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# The Rhythmbox authors hereby grant permission for non-GPL compatible
# GStreamer plugins to be used and distributed together with GStreamer
# and Rhythmbox. This permission is above and beyond the permissions granted
# by the GPL license by which Rhythmbox is covered. If you modify this code
# you may extend this exception to your version of the code, but you are not
# obligated to do so. If you do not wish to do so, delete this exception
# statement from your version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

import urllib
import re
import rb
import HTMLParser

from unicodedata import normalize


class VagalumeParser (object):
	def __init__(self, artist, title):
		self.artist = artist
		self.title = title

	
	def search(self, callback, *data):
		artist = normalize('NFKD', self.artist.decode('utf-8')).encode('ASCII','ignore')
		title = normalize('NFKD', self.title.decode('utf-8')).encode('ASCII','ignore') 

		artist = urllib.quote(artist.replace('(', '').replace(')', '').replace(' ', '-').replace('\'', ''))
		title = urllib.quote(title.replace('(', '').replace(')', '').replace(' ', '-').replace('\'', ''))

		url = 'http://vagalume.uol.com.br/%s/%s.html' % (artist, title)
			
		loader = rb.Loader()
		loader.get_url (url, self.got_lyrics, callback, *data)

	def got_lyrics(self, lyric, callback, *data):
		lyric = re.sub('<[Bb][Rr][^>]*>', '', lyric)

		if re.search('<div class="tab_original">([^<]*)', lyric) is not None:
			body = re.split('<div class="tab_original">([^<]*)', lyric)[1]

			pars = HTMLParser.HTMLParser()
			body = pars.unescape(body)
	
			title = re.split('<h1>(.*)</h1>', lyric)[1]
			artist = re.split('<h2 class="head"><a href=(.*)>(.*)</a></h2>', lyric)[2]

			title = "%s - %s\n\n" % (artist, title)
			lyric = title + body
			lyric += "\n\nLyrics provided by vagalume.com.br"
			
			callback(lyric, *data)
		else:
			callback (None, *data)
    		
