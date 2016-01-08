#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collection import Collection
import re,sys
import json
tagre = re.compile(r"<[^>]+>");
class Coccoc(Collection):
	def filter(self,ttag="h2",ctag="p"):
		try:
			search = json.loads(self.content)
		except:
			search = None
		if not search and not search['search']['search_results']:
			return ''
		search_results = search['search']['search_results']
		strings = ""
		for i in search_results:
			head = "<%s>%s</%s>"%(ttag,tagre.sub("",i['title']),ttag)
			content = "<%s>%s</%s>"%(ctag,tagre.sub("",i['content']),ctag)
			strings +=("\r\n"+head+"\r\n"+content)
		return strings
