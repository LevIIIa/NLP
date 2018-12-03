# -*- coding: utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
from datetime import datetime
import nltk
nltk.download('punkt')
import collections
import math
from nltk.tokenize import ToktokTokenizer
toktok = ToktokTokenizer()

# функция для мёрджа двух словарей
def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


# На вход идет корпус в виде списка слов
def compute_tf(corpus):
    # Считаем частотность всех терминов во входном списке
    tf_corpus = collections.Counter(corpus)
    for i in tf_corpus:
        # для каждого слова в tf_text считаем TF путём деления
        # встречаемости слова на общее количество слов в корпусе
        tf_corpus[i] = tf_corpus[i]/float(len(corpus))
    # возвращаем объект типа Counter c TF всех слов корпуса
    return tf_corpus


# На вход берется слово, для которого считаем IDF и корпус в виде списка списков слов
def compute_idf(word, corpus):
    # количество текстов, где встречается искомый термин считается как генератор списков
    return math.log10(len(corpus)/sum([1.0 for i in corpus if word in i]))


# На вход идет корпус в виде списка текстов
def compute_tfidf(corpus):
    documents_list = []
    for text in corpus:
        tf_idf_dictionary = {}
        computed_tf = compute_tf(text)
        for word in computed_tf:
            tf_idf_dictionary[word] = computed_tf[word] * compute_idf(word, corpus)
        documents_list.append(tf_idf_dictionary)
    return documents_list


# название файла, в который всё сохраняем
filename = 'Discussions_stats_result.txt'
file_to_save = open(filename, 'a')


# количество отзывов в файле
reviews_number = 0

# словарь с годами и количествами отзывов в каждом из них
reviews_by_years_counts = {}
# corpus в виде списка слов
coprus_words_list = []
# corpus в виде списка списков
corpus_texts_list = []
# количество слов в корпусе без лемматизации
corpus_words_count = 0
# уникальные слова в корпусе без лемматизации
corpus_unique_words = {}
# средняя длина отзыва
average_review_length = 0

# idf всех уникальных слов (без лемматизации)
corpus_unique_words_idf = {}

# открываем файл с отзывами
with open('../Statistik/discussions.txt') as f:
    # пробегаемся по отзывам в файле
    for review in f:
        # инкрементируем количество отзывов в файле
        reviews_number += 1

        # парсим строку в dict
        review_json = json.loads(review)

        # получаем год отзыва
        review_year = str(datetime.strptime(review_json['date'], '%d.%m.%Y, %H:%M').date().year)

        # проверяем, есть ли год отзыва в словаре
        # если есть, то инкрементируем количество отзывов этого года
        if review_year in reviews_by_years_counts:
            reviews_by_years_counts[review_year] += 1
        # если года в словаре нет, то добавляем
        else:
            reviews_by_years_counts[review_year] = 1

        # -- Считаем количество слов в корпусе без лемматизации --
        # переводим слова в lowercase
        lowercase_review_text = review_json['message'].lower()

        import re
        s = re.sub('[>"/,;~.[?*_)^#$(»0123456789•<br!=qwetyuiop{}asdfghjkl|+%—:z&xcvnm-]', '', lowercase_review_text)
        s = re.sub(']', '', s)
        lowercase_review_text = s

        # токенизируем отзыв (разбиваем на последовательность слов)
        review_tokens = toktok.tokenize(lowercase_review_text)
        # мёрджим с общим списком слов корпуса
        coprus_words_list += review_tokens
        # закидываем в виде списка в общий список текстов
        corpus_texts_list.append(review_tokens)
        # считаем, сколько слов в отзыве, прибавляем в общую переменную корпуса
        corpus_words_count += len(review_tokens)
        # оставляем в отзыве только уникальные слова (в качестве оптимизации, ускорения работы)
        unique_review_tokens = set(review_tokens)
        # заполняем словарь уникальных слов корпуса
        for word in unique_review_tokens:
            # если слово уже есть в словаре уникальных слов корпуса
            if word in corpus_unique_words:
                corpus_unique_words[word] += 1
            # если нет, то добавляем
            else:
                corpus_unique_words[word] = 1

# ======================== ВЫВОД ============================
file_to_save.write("Имя файла: " + filename)
file_to_save.write("\nКоличество отзывов в файле: %d" % reviews_number)
file_to_save.write("\nЧисло уникальных лет: %d" % len(reviews_by_years_counts))
file_to_save.write("\nЧисло отзывов по годам: " + json.dumps(reviews_by_years_counts, ensure_ascii=False))
# ===========================================================

file_to_save.write("\nКоличество слов в корпусе без лемматизации: %d" % corpus_words_count)
file_to_save.write("\nКоличество уникальных слов в корпусе без лемматизации: %d" % len(corpus_unique_words))

# считаем TF корпуса (без лемматизации)
most_popular_words_tf = compute_tf(coprus_words_list).most_common(500)
file_to_save.write("\nВЫВОДИМ ТОП 500 TF по словам (без лемматизации):")
for word in most_popular_words_tf:
    file_to_save.write("\n" + "'" + word[0] + "'" + ": " + str(word[1]))

#считаем IDF для всех уникальных слов в корпусе
for word in corpus_unique_words:
    corpus_unique_words_idf[word] = compute_idf(word, corpus_texts_list)

file_to_save.write(corpus_unique_words_idf)
   #считаем TF-IDF
file_to_save.write(compute_tfidf(corpus_texts_list))
