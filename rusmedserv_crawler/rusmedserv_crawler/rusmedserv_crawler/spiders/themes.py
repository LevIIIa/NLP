# -*- coding: utf-8 -*-
import json
import os
import re
import scrapy


# Темы
class ThemesSpider(scrapy.Spider):
    name = 'themes'
    allowed_domains = ['forums.rusmedserv.com']
    start_urls = ['https://forums.rusmedserv.com/']

    def start_requests(self):
        # для начала проверим,
        # если темы уже спарсены, то удалим старый файл
        if os.path.exists("themes.txt"):
            os.remove("themes.txt")
        # открываем файл с разделами
        f = open('sections.txt')
        # пробегаемся по каждому разделу
        for line in f.read().split("\n"):
            # если строка не пустая
            if len(line) > 0:
                # берем url раздела и делаем запрос на парсинг тем
                url = json.loads(line)['url']
                yield scrapy.Request(url=url)
        f.close()

    def parse(self, response):
        html = response.body.decode('windows-1251')
        matches = re.findall(
            r'href=\"([a-zA-Z0-9_\?\.=]+?)\"\sid=\"(thread_title_\d+)\".*?>(.+?)</a>',
            html,
            flags=re.S
        )
        output = open('themes.txt', 'a')
        for elem in matches:
            section = {'section_url': response.request.url, 'theme_name': elem[2].encode('utf8'), 'theme_id': elem[1], 'theme_url': self.start_urls[0] + elem[0]}
            output.write('{}\n'.format(json.dumps(section, ensure_ascii=False)))
        output.close()
