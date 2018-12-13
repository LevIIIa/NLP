1)
Для работы rusmedserv_cravler необходимо просто запустить файл consistent_spider_runner.py

Пауки будут последовательно работать, сначала будет собран на вывод файл sections.txt
Далее по этому файлу пройдёт второй паук и выведет themes.txt
И Аналогично третий выведет данные в файл discussions.txt 

2)
Для работы statistics_calculation/all_reviews_texts/all_reviews_texts_processor.py необходимо загрузить следующие файлы из ТЗ и поместить их в соответствующие папки:

https://cimm.kpfu.ru/seafile/f/32cffc93caec4a068c5c/
Добавить в statistics_calculation/all_reviews_texts/alt_reviews_texts_processor.txt

https://cimm.kpfu.ru/seafile/f/3de4bee6c2344347bed2/
Добавить в statistics_calculation/hosp_reviews_texts/hosp_reviews_texts.txt

https://cimm.kpfu.ru/seafile/f/cf558054df6c45f8aca5/
Добавить в statistics_calculation/reviews_texts/reviews_texts.txt

https://cimm.kpfu.ru/seafile/f/d9bd6385f8724f498484/
Разархивировать и добавить в statistics_calculation/comments/comments.json

Далее просто запустить all_reviews_texts_processor.py
Вывод статистики произойдёт в консоль.