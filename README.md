# Сервис рекомендаций

В процессе выполнения данного проекта разработан микросервис для получения рекомендаций в онлайн-режиме.
Он включает в себя несколько моделей. От базовых - популярное и random до более усложненных - kNN (item kNN, user kNN), LightFM, DSSM (для более репрезентативного сэмплирования используется длительность просмотра), MultiVAE. На последнем этапе была обучена двухэтапная модель LightFM, а на втором уровне LightGBM + Popular.

Реализован тюнинг гиперпараметров, например, векторного расстояния, с использованием optuna.
Для работы с холодными пользователями используются их фичи (соц.дем, для кого нет фичей - Popular).
Использованы библитеки RecTools, implicit, RecBole

## Данные
Для реализации проекта использованы данные из приложения МТС Kion по взаимодействиям пользователей с контентом за период 6 месяцев.
В представленном датасете собраны данные по пользователям и объектам (сериалы/фильмы), а также по их взаимодействиям (просмотр контента пользователем) из онлайн-кинотеатра Kion. Данные по просмотру контента собраны за ~6 месяцев, с 2021-03-13 по 2021-08-22  включительно, и разбавлены случайным шумом. ID пользователей и контента анонимизированы.

Статистика по датасету:

- 840к пользователей
- 16к объектов
- 5.5кк взаимодействий

1. users.csv
В данном файле содержится информация о пользователях:

user_id - ID пользователя
age - возрастная группа пользователя, строка вида "M_N"
sex - пол пользователя
income - доход пользователя, строка вида "M_N"
kids_flg - флаг "наличие ребенка"

2. items.csv
В данном файле содержится информация об объектах (фильмы/сериалы):

item_id - ID контента
content_type - Тип контента (фильм, сериал)
title - Название на русском
title_orig - Название оригинальное
genres - Жанры из источника (онлайн-кинотеатры)
countries - страны
for_kids - флаг "контент для детей"
age_rating - возрастной рейтинг
studios - студии
directors - директора
actors - актеры
keywords - ключевые слова
description - описание

3. interactions.csv
В данном файле содержится информация о взаимодействиях пользователей с контентом:

user_id - ID пользователя
item_id - ID контента
last_watch_dt - Дата последнего просмотра
total_dur - Общая продолжительность всех просмотров данного контента в секундах
content_type - Тип контента (фильм, сериал)

## Метрики
Метрика качества в соревновании - map@10 (Mean Average Precision at 10). На скриншоте представлены результаты работы для различных моделей.

![image](https://github.com/user-attachments/assets/b62db919-d666-4496-b15b-ea62ba200fdc)
