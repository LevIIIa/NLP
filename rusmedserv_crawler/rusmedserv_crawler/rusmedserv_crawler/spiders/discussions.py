# -*- coding: utf-8 -*-
import json
import os
import regex
import scrapy


# Дискуссии
class DiscussionsSpider(scrapy.Spider):
    name = 'discussions'
    allowed_domains = ['forums.rusmedserv.com']
    start_urls = ['https://forums.rusmedserv.com/']

    @staticmethod
    def check_equal(iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)

    def start_requests(self):
        # для начала проверим,
        # если дискуссии уже спарсены, то удалим старый файл
        if os.path.exists("discussions.txt"):
            os.remove("discussions.txt")
        f = open('themes.txt')
        for line in f.read().split("\n"):
            # если строка не пустая
            if len(line) > 0:
                url = json.loads(line)['theme_url']
                yield scrapy.Request(url=url)
        f.close()

    def parse(self, response):
        html = response.body.decode('windows-1251')

        dates_regex = r'\d{2}\.\d{2}\.\d{4},\s\d{' \
                      r'2}:\d{2}'
        # group2
        names_regex = r'<a\sclass=\"bigusername\"\shref=\"member\.php.+?>(<b><font\scolor=.*?>)*(.+?)(<\/font><\/b>)*<\/a>'
        # здесь group1 (ranks) и group2 (ratings)
        ranks_and_ratings_regex = r'<div\sclass=\"smallfont\">([а-яА-Я\s]+)<\/div>\s*<div\sclass=\"smallfont\">(.+?)<\/div>'.decode('utf-8')
        # данные авторов:
        # group1 (дата регистрации);
        # group2 (адрес);
        # group3 (кол-во сообщений);
        # group5 (сказал(а) спасибо), group6 (поблагодарили) | group7 (поблагодарили)
        authors_data_regex = r'<div\sclass=\"smallfont\">\s*<div>Регистрация:\s(.*?)<\/div>\s*<div>Адрес:\s(.*?)<\/div>\s*<div>\s*Сообщений:\s(.*?)\s*<\/div>\s*(<div>\s*Сказал\(а\)\sспасибо:\s*(.*?)\s*<\/div>\s*<div>\s*Поблагодарили\s*(.*?)\s*<\/div>|<div>\s*Поблагодарили\s*(.*?)\s*<\/div>)'.decode('utf-8')
        # group1
        message_regex = r'<td\sclass=\"alt1\"\sid=\"td_post.+?\">\s*([.\s\S]*?)<\/td>'

        dates_matches = regex.findall(dates_regex, html, flags=regex.S)
        names_matches = regex.findall(names_regex, html, flags=regex.S)
        ranks_and_ratings_matches = regex.findall(ranks_and_ratings_regex, html, flags=regex.S)
        authors_data_matches = regex.findall(authors_data_regex, html, flags=regex.S)
        message_matches = regex.findall(message_regex, html, flags=regex.S)
        # если по регулярным выражениям найдены равные значения
        if self.check_equal([len(dates_matches), len(names_matches), len(ranks_and_ratings_matches), len(authors_data_matches), len(message_matches)]):
            # открываем файл
            output = open('discussions.txt', 'a')
            # пробегаемся циклом, количество итераций получаем от любого списка *_matches
            for i in range(0, len(names_matches)):
                discussion = {}
                discussion['discussion_url'] = response.request.url
                discussion['date'] = dates_matches[i]
                discussion['name'] = names_matches[i][1]
                discussion['rank'] = ranks_and_ratings_matches[i][0]
                discussion['rating'] = ranks_and_ratings_matches[i][1]
                discussion['registration_date'] = authors_data_matches[i][0]
                discussion['address'] = authors_data_matches[i][1]
                discussion['messages_number'] = authors_data_matches[i][2]
                # проверяем, есть ли 7 группа в списке authors_data_matches
                try:
                    discussion['thanked'] = authors_data_matches[i][6]
                # если 7 группы в списке authors_data_matches нет
                except IndexError:
                    discussion['said_thank_you'] = authors_data_matches[i][4]
                    discussion['thanked'] = authors_data_matches[i][5]
                discussion['message'] = message_matches[i]
                output.write('{}\n'.format(json.dumps(discussion, ensure_ascii=False)))
            output.close()
