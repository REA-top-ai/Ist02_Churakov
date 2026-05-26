"""External API: работа с Kinopoisk.dev (поиск фильмов)."""
import requests                                            # библиотека для HTTP-запросов

from config import KINOPOISK_API_KEY                       # ключ от Kinopoisk.dev из настроек


# Своё исключение, чтобы UI мог отличить ошибку сети от "фильм не найден"
class MovieError(Exception):                               # класс для ошибок этого модуля
    """Ошибка при работе с Kinopoisk.dev API."""


def find_movie(movie_name):                                # ищет фильм по названию
    """Находит фильм по названию. Возвращает словарь или None, если фильм не найден."""
    url = "https://api.kinopoisk.dev/v1.4/movie/search"    # endpoint поиска фильмов
    params = {                                             # параметры запроса
        "query": movie_name,                               # название фильма (русский работает)
        "limit": 1,                                        # возвращаем 1 результат (самый релевантный)
    }
    headers = {                                            # заголовки запроса
        "X-API-KEY": KINOPOISK_API_KEY,                    # ключ передаётся в заголовке (не в URL)
        "accept": "application/json",                      # просим ответ в формате JSON
    }

    try:                                                   # пытаемся отправить запрос
        response = requests.get(url, params=params, headers=headers, timeout=10)  # GET с таймаутом 10 сек
        response.raise_for_status()                        # бросает исключение при HTTP 4xx/5xx
    except requests.Timeout:                               # сервер не ответил за 10 сек
        raise MovieError(
            "Kinopoisk.dev не отвечает (превышено время ожидания). "
            "Проверь интернет или VPN."
        )
    except requests.ConnectionError:                       # вообще не удалось подключиться
        raise MovieError(
            "Не удалось подключиться к Kinopoisk.dev. "
            "Проверь интернет или VPN."
        )
    except requests.HTTPError as e:                        # сервер ответил ошибкой 4xx/5xx
        raise MovieError(f"Kinopoisk.dev вернул ошибку: {e}")

    data = response.json()                                 # парсим ответ как JSON
    movies = data.get("docs", [])                          # достаём массив найденных фильмов (ключ "docs")

    if not movies:                                         # если массив пустой — фильм не найден
        return None                                        # возвращаем None (это не ошибка)

    movie = movies[0]                                      # берём первый (самый релевантный) фильм
    return _parse_movie(movie)                             # парсим его в наш формат


def _parse_movie(movie):                                   # извлекает нужные поля из ответа API
    """Превращает сырой ответ Kinopoisk в простой словарь."""
    # Название: сначала русское, если нет — английское (alternativeName)
    name = movie.get("name") or movie.get("alternativeName") or "Без названия"

    # Рейтинг хранится во вложенном объекте rating, берём оценку Кинопоиска
    rating_obj = movie.get("rating", {})                   # объект с рейтингами
    rating = rating_obj.get("kp", 0)                       # оценка Кинопоиска (kp), 0 если нет

    # Жанры — массив объектов вида {"name": "драма"}, собираем их названия в строку
    genres_list = movie.get("genres", [])                  # массив жанров
    genres = ", ".join(g.get("name", "") for g in genres_list)  # склеиваем через запятую

    # Страны — тоже массив объектов {"name": "США"}
    countries_list = movie.get("countries", [])            # массив стран
    countries = ", ".join(c.get("name", "") for c in countries_list)  # склеиваем

    return {                                               # возвращаем чистый словарь
        "name": name,                                      # название
        "year": movie.get("year", 0),                      # год выхода
        "rating": round(rating, 1),                        # рейтинг, округлённый до 1 знака
        "genres": genres,                                  # жанры строкой
        "countries": countries,                            # страны строкой
        "description": movie.get("description") or "Описание отсутствует.",  # описание
        "poster": movie.get("poster", {}).get("url", ""),  # ссылка на постер (может быть пустой)
    }
