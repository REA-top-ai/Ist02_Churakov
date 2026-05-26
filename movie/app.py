"""Главный файл приложения. Запускать командой: streamlit run app.py"""
import streamlit as st                                     # фреймворк для UI

import auth                                                # модуль входа через Google
from api import client                                     # API Client с бизнес-логикой
from db.database import init_db                            # инициализация БД
from external.kinopoisk import MovieError                  # исключение от внешнего API


init_db()                                                  # создаём таблицы в БД при первом запуске

st.title("Гид по фильмам с AI")                            # заголовок приложения


# ============================================================================
# Шаг 1: проверяем, залогинен ли пользователь
# ============================================================================

# Если в URL есть параметр code от Google — пользователь только что вернулся со страницы логина
code = st.query_params.get("code")                         # читаем параметр code из URL
if code and "user" not in st.session_state:                # если код есть и мы ещё не залогинены
    user_info = auth.get_user_info(code)                   # обмениваем код на данные пользователя
    user = client.get_or_create_user(                      # сохраняем пользователя в БД (или находим)
        user_info["google_id"],
        user_info["name"],
        user_info["email"],
    )
    st.session_state["user"] = user                        # запоминаем пользователя в сессии Streamlit
    st.query_params.clear()                                # чистим URL от code
    st.rerun()                                             # перерисовываем страницу

# Если пользователь не залогинен — показываем кнопку входа
if "user" not in st.session_state:                         # проверяем сессию
    st.write("Войди через Google, чтобы пользоваться приложением.")  # пояснение
    login_url = auth.get_login_url()                       # получаем URL для входа
    st.link_button("Войти через Google", login_url)        # кнопка-ссылка на Google
    st.stop()                                              # дальше код не выполняем


# ============================================================================
# Шаг 2: пользователь залогинен, показываем основной интерфейс
# ============================================================================

user = st.session_state["user"]                            # достаём данные пользователя из сессии

# Шапка: приветствие + кнопка выхода
st.write(f"Привет, {user['name']}!")                       # приветствие
if st.button("Выйти"):                                     # кнопка выхода
    st.session_state.clear()                               # очищаем сессию
    st.rerun()                                             # перерисовываем


# ============================================================================
# Делим интерфейс на две вкладки
# ============================================================================

tab_search, tab_favorites = st.tabs(["Поиск фильма", "Хочу посмотреть"])  # две вкладки

# ============================================================================
# Вкладка 1: поиск фильма
# ============================================================================

with tab_search:                                           # содержимое первой вкладки
    movie_input = st.text_input("Введи название фильма", placeholder="Матрица")  # поле ввода

    if st.button("Найти фильм") and movie_input:           # кнопка поиска
        with st.spinner("Ищу фильм и спрашиваю AI..."):    # спиннер
            try:                                           # пробуем получить фильм
                result = client.get_movie_info(movie_input)  # запрашиваем фильм + разбор
            except MovieError as e:                        # если ошибка сети/API
                st.error(str(e))                           # показываем понятное сообщение
                st.session_state.pop("last_movie", None)   # убираем старый результат
                result = "ERROR"                           # помечаем, что произошла ошибка

        if result is None:                                 # если фильм не найден
            st.error("Фильм не найден. Попробуй другое название.")
            st.session_state.pop("last_movie", None)       # убираем старый результат
        elif result != "ERROR":                            # если всё хорошо
            st.session_state["last_movie"] = result        # сохраняем в сессии

    # Показываем результат, если он есть в сессии
    if "last_movie" in st.session_state:                   # если уже искали фильм
        result = st.session_state["last_movie"]            # достаём результат
        movie = result["movie"]                            # данные о фильме
        review = result["review"]                          # разбор от AI

        st.write("---")                                    # разделитель

        # Постер и основная информация в двух колонках
        col_poster, col_info = st.columns([1, 2])          # колонка постера + колонка инфо
        with col_poster:                                   # левая колонка — постер
            if movie["poster"]:                            # если ссылка на постер есть
                st.image(movie["poster"], width=150)       # показываем картинку
        with col_info:                                     # правая колонка — данные
            st.write(f"Название: {movie['name']}")         # название
            st.write(f"Год: {movie['year']}")              # год
            st.write(f"Рейтинг: {movie['rating']}")        # рейтинг
            st.write(f"Жанры: {movie['genres']}")          # жанры
            st.write(f"Страны: {movie['countries']}")      # страны

        st.write("Описание:")                              # подпись
        st.write(movie["description"])                     # описание из Кинопоиска

        st.write("---")                                    # разделитель
        st.write("Что говорит AI:")                        # заголовок секции разбора
        st.write(review)                                   # сам разбор

        # Кнопка добавления в "Хочу посмотреть"
        if st.button("Добавить в «Хочу посмотреть»"):      # клик по кнопке
            added = client.add_favorite(user["id"], movie)  # пробуем добавить
            if added:                                      # если добавили
                st.success(f"Фильм «{movie['name']}» добавлен в список")
            else:                                          # если уже есть
                st.info(f"Фильм «{movie['name']}» уже в списке")


# ============================================================================
# Вкладка 2: список "Хочу посмотреть"
# ============================================================================

with tab_favorites:                                        # содержимое второй вкладки
    favorites = client.get_favorites(user["id"])           # загружаем избранные

    if not favorites:                                      # если список пуст
        st.write("Твой список пуст. Найди фильм на вкладке «Поиск фильма».")  # подсказка
    else:                                                  # если есть фильмы
        # Перебираем каждый фильм в списке
        for fav in favorites:                              # для каждого фильма
            col1, col2, col3 = st.columns([3, 2, 1])       # три колонки: название, кнопка AI, удаление
            with col1:                                     # колонка с названием
                st.write(f"• {fav['name']} ({fav['year']}), рейтинг {fav['rating']}")  # название, год, рейтинг
            with col2:                                     # колонка с кнопкой "Что говорит AI"
                if st.button("Что говорит AI", key=f"ai_{fav['id']}"):  # клик
                    with st.spinner(f"Спрашиваю AI про «{fav['name']}»..."):  # спиннер
                        # Запрашиваем разбор AI (передаём данные фильма из БД)
                        review = client.get_movie_review_only(fav)  # получаем разбор
                        # Сохраняем результат в сессии под ID этого фильма
                        st.session_state[f"fav_review_{fav['id']}"] = review
            with col3:                                     # колонка с кнопкой удаления
                if st.button("Удалить", key=f"del_{fav['id']}"):  # клик
                    client.remove_favorite(fav["id"])      # удаляем из БД
                    # Заодно чистим разбор этого фильма из сессии, если он там есть
                    st.session_state.pop(f"fav_review_{fav['id']}", None)
                    st.rerun()                             # перерисовываем

            # Если для этого фильма уже загружен разбор AI — показываем его
            review_key = f"fav_review_{fav['id']}"         # ключ в сессии для этого фильма
            if review_key in st.session_state:             # если разбор есть
                st.write(f"  Описание: {fav['description']}")  # описание из БД
                st.write(f"  Что говорит AI: {st.session_state[review_key]}")  # разбор AI

                # Кнопка "Скрыть" — убирает разбор из видимости
                if st.button("Скрыть", key=f"hide_{fav['id']}"):  # клик
                    st.session_state.pop(review_key, None)  # удаляем из сессии
                    st.rerun()                             # перерисовываем

            st.write("---")                                # разделитель между фильмами
