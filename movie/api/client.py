"""API Client: главный слой бизнес-логики.

UI вызывает только функции отсюда. Этот файл ходит в базу, во внешний API и в AI.
"""
from db.database import Session                            # фабрика сессий БД
from db.models import User, FavoriteMovie                  # модели таблиц
from external import kinopoisk                             # обёртка над Kinopoisk.dev
from ai_client import advisor                              # обёртка над Mistral


# ============================================================================
# Пользователи
# ============================================================================

def get_or_create_user(google_id, name, email):           # находит или создаёт пользователя
    """Если пользователь уже есть в БД — возвращает его. Если нет — создаёт нового."""
    session = Session()                                    # открываем сессию БД
    user = session.query(User).filter_by(google_id=google_id).first()  # ищем по google_id
    if not user:                                           # если такого нет
        user = User(google_id=google_id, name=name, email=email)  # создаём нового
        session.add(user)                                  # добавляем в сессию
        session.commit()                                   # сохраняем в БД
    user_id = user.id                                      # сохраняем id (после close объект недоступен)
    user_name = user.name                                  # сохраняем имя
    session.close()                                        # закрываем сессию
    return {"id": user_id, "name": user_name}              # возвращаем простой словарь


# ============================================================================
# Фильмы (External API + AI)
# ============================================================================

def get_movie_info(movie_name):                            # получает фильм + разбор AI по названию
    """Ищет фильм, получает данные и просит AI дать разбор. Возвращает всё одним словарём."""
    movie = kinopoisk.find_movie(movie_name)               # шаг 1: ищем фильм во внешнем API
    if movie is None:                                      # если фильм не найден
        return None                                        # возвращаем None

    review = advisor.get_review(movie)                     # шаг 2: получаем разбор от AI

    return {                                               # возвращаем всё вместе
        "movie": movie,                                    # данные о фильме
        "review": review,                                  # разбор от AI
    }


def get_movie_review_only(movie):                          # получает только разбор AI по готовым данным
    """Получает разбор AI для фильма с уже известными данными.
    Используется для избранных фильмов — поиск уже не нужен.
    """
    return advisor.get_review(movie)                       # сразу запрашиваем разбор у AI


# ============================================================================
# Избранные фильмы ("Хочу посмотреть")
# ============================================================================

def get_favorites(user_id):                                # возвращает избранные фильмы пользователя
    """Список избранных фильмов конкретного пользователя."""
    session = Session()                                    # открываем сессию
    favorites = session.query(FavoriteMovie).filter_by(user_id=user_id).all()  # достаём все
    result = [                                             # переводим в список простых словарей
        {                                                  # один фильм
            "id": f.id,                                    # id для удаления
            "name": f.name,                                # название
            "year": f.year,                                # год
            "rating": f.rating,                            # рейтинг
            "description": f.description,                  # описание
        }
        for f in favorites                                 # по каждому избранному
    ]
    session.close()                                        # закрываем сессию
    return result                                          # возвращаем список


def add_favorite(user_id, movie):                          # добавляет фильм в избранные
    """Сохраняет фильм в избранных у пользователя."""
    session = Session()                                    # открываем сессию

    # Проверяем, нет ли уже такого фильма
    existing = session.query(FavoriteMovie).filter_by(     # ищем существующий
        user_id=user_id, name=movie["name"]                # с таким же названием у этого пользователя
    ).first()

    if existing:                                           # если уже добавлен
        session.close()                                    # закрываем сессию
        return False                                       # возвращаем False — ничего не сделали

    favorite = FavoriteMovie(                              # создаём новую запись
        user_id=user_id,                                   # к какому пользователю
        name=movie["name"],                                # название
        year=movie["year"],                                # год
        rating=movie["rating"],                            # рейтинг
        description=movie["description"],                  # описание
    )
    session.add(favorite)                                  # добавляем в сессию
    session.commit()                                       # сохраняем в БД
    session.close()                                        # закрываем сессию
    return True                                            # возвращаем True — успех


def remove_favorite(favorite_id):                          # удаляет фильм из избранных
    """Удаляет фильм из избранных по его ID."""
    session = Session()                                    # открываем сессию
    favorite = session.query(FavoriteMovie).get(favorite_id)  # ищем по id
    if favorite:                                           # если нашли
        session.delete(favorite)                           # удаляем
        session.commit()                                   # сохраняем изменения
    session.close()                                        # закрываем сессию
