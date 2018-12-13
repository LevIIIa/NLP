# -*- coding: utf-8 -*-

import sys
# import pandas as pd
# import seaborn as sns
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime
import nltk
nltk.download('punkt')
import collections
import math
from nltk.tokenize import ToktokTokenizer
toktok = ToktokTokenizer()


# функция для построения диаграммы для ТОП n
def draw_chart(categories, reviews_count, name):
    index = np.arange(len(categories))
    plt.bar(index, reviews_count)
    plt.xlabel(name, fontsize=5)
    plt.ylabel('Count', fontsize=5)
    plt.xticks(index, categories, fontsize=4, rotation=90)
    plt.title(name + ' comparison')
    plt.savefig(name + '.png', dpi=600)


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
filename = 'all_reviews_texts_result.txt'
file_to_save = open(filename, 'a')


# количество отзывов в файле
reviews_number = 0

# словарь с годами и количествами отзывов в каждом из них
reviews_by_years_counts = {}

# число отзывов по уникальным rating 1
unique_rating_1 = {}
# число отзывов по уникальным rating 2
unique_rating_2 = {}
# число отзывов по уникальным rating 3
unique_rating_3 = {}
# число отзывов по уникальным rating 4
unique_rating_4 = {}
# число отзывов по уникальным rating 5
unique_rating_5 = {}

# число отзывов по уникальным cat 1
unique_cat_1 = {}
# число отзывов по уникальным cat 2
unique_cat_2 = {}
# число отзывов по уникальным cat 3
unique_cat_3 = {}
# число отзывов по уникальным cat 4
unique_cat_4 = {}

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
with open('../all_reviews_texts/alt_reviews_texts.txt') as f:
    # пробегаемся по отзывам в файле
    for review in f:
        # инкрементируем количество отзывов в файле
        reviews_number += 1

        # парсим строку в dict
        review_json = json.loads(review)

        # получаем год отзыва
        review_year = str(datetime.strptime(review_json['review_date'], '%d.%m.%Y').date().year)

        # проверяем, есть ли год отзыва в словаре
        # если есть, то инкрементируем количество отзывов этого года
        if review_year in reviews_by_years_counts:
            reviews_by_years_counts[review_year] += 1
        # если года в словаре нет, то добавляем
        else:
            reviews_by_years_counts[review_year] = 1

        # считаем количества отзывов по уникальным рейтингам (rating_ 1-5)
        if review_json['rating_1'] in unique_rating_1:
            unique_rating_1[review_json['rating_1']] += 1
        else:
            unique_rating_1[review_json['rating_1']] = 1
        if review_json['rating_2'] in unique_rating_2:
            unique_rating_2[review_json['rating_2']] += 1
        else:
            unique_rating_2[review_json['rating_2']] = 1
        if review_json['rating_3'] in unique_rating_3:
            unique_rating_3[review_json['rating_3']] += 1
        else:
            unique_rating_3[review_json['rating_3']] = 1
        if review_json['rating_4'] in unique_rating_4:
            unique_rating_4[review_json['rating_4']] += 1
        else:
            unique_rating_4[review_json['rating_4']] = 1
        if review_json['rating_5'] in unique_rating_5:
            unique_rating_5[review_json['rating_5']] += 1
        else:
            unique_rating_5[review_json['rating_5']] = 1

        # считаем количества отзывов по уникальным категориям (cat 1-4)
        if review_json['cat1'] in unique_cat_1:
            unique_cat_1[review_json['cat1']] += 1
        else:
            unique_cat_1[review_json['cat1']] = 1
        if review_json['cat2'] in unique_cat_2:
            unique_cat_2[review_json['cat2']] += 1
        else:
            unique_cat_2[review_json['cat2']] = 1
        if review_json['cat3'] in unique_cat_3:
            unique_cat_3[review_json['cat3']] += 1
        else:
            unique_cat_3[review_json['cat3']] = 1
        if review_json['cat4'] in unique_cat_4:
            unique_cat_4[review_json['cat4']] += 1
        else:
            unique_cat_4[review_json['cat4']] = 1

        # -- Считаем количество слов в корпусе без лемматизации --
        # переводим слова в lowercase
        lowercase_review_text = review_json['description'].lower()
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

# считаем среднюю длину отзыва (без лемматизации)
average_review_length = corpus_words_count / reviews_number

# ======================== ВЫВОД ============================
file_to_save.write("Имя файла: " + filename)
file_to_save.write("\n===============================")
file_to_save.write("\n====== Всё по пункту 1: =======")
file_to_save.write("\n===============================")
file_to_save.write("\nКоличество отзывов в файле: %d" % reviews_number)
file_to_save.write("\nЧисло уникальных лет: %d" % len(reviews_by_years_counts))
file_to_save.write("\nЧисло отзывов по годам: " + json.dumps(reviews_by_years_counts, ensure_ascii=False))

file_to_save.write("\nЧисло уникальных рейтингов rating1: %d" % len(unique_rating_1))
file_to_save.write("\nЧисло отзывов по уникальным rating1: " + json.dumps(unique_rating_1))
file_to_save.write("\nЧисло уникальных рейтингов rating2: %d" % len(unique_rating_2))
file_to_save.write("\nЧисло отзывов по уникальным rating2: " + json.dumps(unique_rating_2))
file_to_save.write("\nЧисло уникальных рейтингов rating3: %d" % len(unique_rating_3))
file_to_save.write("\nЧисло отзывов по уникальным rating3: " + json.dumps(unique_rating_3))
file_to_save.write("\nЧисло уникальных рейтингов rating4: %d" % len(unique_rating_4))
file_to_save.write("\nЧисло отзывов по уникальным rating4: " + json.dumps(unique_rating_4))
file_to_save.write("\nЧисло уникальных рейтингов rating5: %d" % len(unique_rating_5))
file_to_save.write("\nЧисло отзывов по уникальным rating5: " + json.dumps(unique_rating_5))

file_to_save.write("\nЧисло уникальных отзывов cat1: %d" % len(unique_cat_1))
file_to_save.write("\nЧисло отзывов по уникальным cat1: " + json.dumps(unique_cat_1, ensure_ascii=False))
file_to_save.write("\nЧисло уникальных отзывов cat2: %d" % len(unique_cat_2))
file_to_save.write("\nЧисло отзывов по уникальным cat2: " + json.dumps(unique_cat_2, ensure_ascii=False))
file_to_save.write("\nЧисло уникальных отзывов cat3: %d" % len(unique_cat_3))
file_to_save.write("\nЧисло отзывов по уникальным cat3: " + json.dumps(unique_cat_3, ensure_ascii=False))
file_to_save.write("\nЧисло уникальных отзывов cat4: %d" % len(unique_cat_4))
file_to_save.write("\nЧисло отзывов по уникальным cat4: " + json.dumps(unique_cat_4, ensure_ascii=False))
# ===========================================================
# ищем ТОП 20 популярных рейтингов
rating1_and_rating2 = merge_two_dicts(unique_rating_1, unique_rating_2)
rating3_and_rating4 = merge_two_dicts(unique_rating_3, unique_rating_4)
all_unique_ratings = merge_two_dicts(rating1_and_rating2, rating3_and_rating4)
popular_rating = list(sorted(all_unique_ratings, key=all_unique_ratings.get, reverse=True))
reviews_counts = []
for rating in all_unique_ratings:
    reviews_counts.append(all_unique_ratings[rating])
file_to_save.write("\nГенерируем график TOP 20 по отзывам среди всех рейтингов")
draw_chart(popular_rating, reviews_counts, 'ratings')

# ищем ТОП 20 популярных категорий
cat1_and_cat2 = merge_two_dicts(unique_cat_1, unique_cat_2)
cat3_and_cat4 = merge_two_dicts(unique_cat_3, unique_cat_4)
all_unique_categories = merge_two_dicts(cat1_and_cat2, cat3_and_cat4)
popular_categories = list(sorted(all_unique_categories, key=all_unique_categories.get, reverse=True))
reviews_counts = []
for category in popular_categories[0:20]:
    reviews_counts.append(all_unique_categories[category])
file_to_save.write("\nГенерируем график TOP 20 по отзывам среди всех категорий")
draw_chart(popular_categories[0:20], reviews_counts, 'categories')

file_to_save.write("\n===============================")
file_to_save.write("\n====== Всё по пункту 2: =======")
file_to_save.write("\n===============================")

file_to_save.write("\nКоличество слов в корпусе без лемматизации: %d" % corpus_words_count)
file_to_save.write("\nКоличество уникальных слов в корпусе без лемматизации: %d" % len(corpus_unique_words))
file_to_save.write("\nСредняя длина отзыва без лемматизации: %d" % average_review_length)

# считаем TF корпуса (без лемматизации)
most_popular_words_tf = compute_tf(coprus_words_list).most_common(100)
file_to_save.write("\nВЫВОДИМ ТОП 100 TF по словам (без лемматизации):")
for word in most_popular_words_tf:
    file_to_save.write("\n" + "'" + word[0] + "'" + ": " + str(word[1]))

# считаем IDF для всех уникальных слов в корпусе
# for word in corpus_unique_words:
#     corpus_unique_words_idf[word] = compute_idf(word, corpus_texts_list)

# print(corpus_unique_words_idf)

# считаем TF-IDF
# print(compute_tfidf(corpus_texts_list))
