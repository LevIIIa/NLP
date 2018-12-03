# -*- coding: utf-8 -*-
import re
import scrapy
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# Разделы
class SectionsSpider(scrapy.Spider):
    name = 'sections'
    allowed_domains = ['forums.rusmedserv.com']
    start_urls = ['https://forums.rusmedserv.com/']

    def parse(self, response):
        html = response.body.decode('windows-1251')
        matches = re.findall(
            r"<td\sclass=\"alt1Active\".+?>.+?<div>.+?<a\shref=\"(.+?)\"><strong>(.+?)<\/strong>",
            html,
            flags=re.S
        )
        output = open('sections.txt', 'w')
        for elem in matches:
            section = {'section': elem[1].encode('utf8'), 'url': self.start_urls[0] + re.sub("s=.+&amp;", "", elem[0])}
            output.write('{}\n'.format(json.dumps(section, ensure_ascii=False)))
        output.close()
